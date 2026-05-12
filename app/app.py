"""
Detection of Fake Undergraduate Admission/SMS Alerts
Streamlit Web Application
"""

import os
import sys
import streamlit as st
import joblib

# Add project root to path so src/ imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.preprocessor import preprocess

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Admission/SMS Fraud Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Load model and vectoriser ─────────────────────────────────────────────────
@st.cache_resource
def load_model():
    base = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base, '..', 'models', 'model.pkl')
    vec_path   = os.path.join(base, '..', 'models', 'vectoriser.pkl')
    rf  = joblib.load(model_path)
    vec = joblib.load(vec_path)
    return rf, vec

rf, vectoriser = load_model()

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f9f9f9; }
    .title-box {
        background-color: #1a3a5c;
        padding: 1.5rem 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .title-box h1 {
        color: white;
        font-size: 1.6rem;
        margin: 0;
        font-family: 'Times New Roman', serif;
    }
    .title-box p {
        color: #a8c4e0;
        font-size: 0.9rem;
        margin: 0.4rem 0 0 0;
        font-family: 'Times New Roman', serif;
    }
    .result-fraud {
        background-color: #fdecea;
        border-left: 6px solid #b85450;
        padding: 1.2rem 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .result-legit {
        background-color: #eaf4ea;
        border-left: 6px solid #82b366;
        padding: 1.2rem 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .result-title {
        font-size: 1.3rem;
        font-weight: bold;
        font-family: 'Times New Roman', serif;
        margin-bottom: 0.3rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 6px solid #d6b656;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-family: 'Times New Roman', serif;
        font-size: 0.9rem;
    }
    .info-box {
        background-color: #e8f0fb;
        border-left: 6px solid #6c8ebf;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-family: 'Times New Roman', serif;
        font-size: 0.9rem;
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.78rem;
        margin-top: 2.5rem;
        font-family: 'Times New Roman', serif;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-box">
    <h1>SMS Fraud Detection System</h1>
    <p>Detection of Fake Undergraduate Admission & SMS Alerts in Nigerian Universities</p>
    <p>Powered by Random Forest + Nigerian Pidgin Normalisation | ExAIS_SMS Corpus</p>
</div>
""", unsafe_allow_html=True)

# ── How to use ────────────────────────────────────────────────────────────────
with st.expander("How to use this tool"):
    st.markdown("""
    1. **Paste** the suspicious SMS message into the text box below.
    2. Optionally enter the **Sender ID** shown on the message.
    3. Click **Verify Message**.
    4. The system will classify the message as **Legitimate** or **Fraudulent**
       and display a confidence score.
    
    > **Important:** If a message is flagged as fraudulent, do **not** respond,
    > click any links, or make any payments. Verify your admission status directly at
    > [www.jamb.gov.ng](https://www.jamb.gov.ng) or through your institution's official portal.
    """)

# ── Input form ────────────────────────────────────────────────────────────────
st.markdown("### Enter the SMS Message")

sender_id = st.text_input(
    "Sender ID (optional)",
    placeholder="e.g. JAMB, 55019, MTN, or a phone number",
    help="The name or number shown as the sender of the SMS"
)

message_input = st.text_area(
    "SMS Message Content",
    placeholder="Paste the full SMS message here...",
    height=160,
    help="Paste the complete text of the suspicious SMS message"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    verify_btn = st.button("Verify Message", use_container_width=True)

# ── Prediction ────────────────────────────────────────────────────────────────
if verify_btn:
    if not message_input.strip():
        st.error("Please enter a message before clicking Verify.")
    else:
        with st.spinner("Analysing message..."):
            # Preprocessing pipeline
            cleaned   = preprocess(message_input)
            vector    = vectoriser.transform([cleaned])
            pred      = rf.predict(vector)[0]
            prob      = rf.predict_proba(vector)[0]
            fraud_prob = prob[1] * 100
            legit_prob = prob[0] * 100
            confidence = prob[pred] * 100

        st.markdown("---")
        st.markdown("### Classification Result")

        if pred == 1:
            # FRAUDULENT
            st.markdown(f"""
            <div class="result-fraud">
                <div class="result-title">FRAUDULENT MESSAGE DETECTED</div>
                <p style="font-family: Times New Roman; margin:0;">
                    This message has been classified as a <strong>fraudulent/spam SMS</strong>
                    with <strong>{confidence:.1f}% confidence</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(fraud_prob))
            st.caption(f"Fraud probability: {fraud_prob:.1f}%  |  Legitimate probability: {legit_prob:.1f}%")

            st.markdown("""
            <div class="warning-box">
                <strong>Do not respond to this message.</strong><br>
                Do not click any links, call any numbers, or make any payments based on this SMS.<br><br>
                <strong>To verify your admission status officially:</strong><br>
                • Visit <a href="https://www.jamb.gov.ng" target="_blank">www.jamb.gov.ng</a> and log in to CAPS<br>
                • Contact your institution's admissions office directly<br>
                • Call the JAMB helpline: <strong>09-7400000-9</strong><br>
                • Report the fraudulent message to JAMB or the Nigerian Communications Commission (NCC)
            </div>
            """, unsafe_allow_html=True)

        else:
            # LEGITIMATE
            st.markdown(f"""
            <div class="result-legit">
                <div class="result-title">LEGITIMATE MESSAGE</div>
                <p style="font-family: Times New Roman; margin:0;">
                    This message has been classified as <strong>legitimate (ham)</strong>
                    with <strong>{confidence:.1f}% confidence</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(legit_prob))
            st.caption(f"Legitimate probability: {legit_prob:.1f}%  |  Fraud probability: {fraud_prob:.1f}%")

            if confidence < 70:
                st.markdown("""
                <div class="info-box">
                    <strong>Note:</strong> The confidence score for this prediction is below 70%.
                    Even though the message appears legitimate, please verify your admission status
                    directly at <a href="https://www.jamb.gov.ng" target="_blank">www.jamb.gov.ng</a>
                    before taking any action.
                </div>
                """, unsafe_allow_html=True)

        # Show preprocessed text (expandable)
        with st.expander("View preprocessing details"):
            st.markdown("**Original message:**")
            st.code(message_input, language=None)
            st.markdown("**After Pidgin normalisation and cleaning:**")
            st.code(cleaned, language=None)
            st.markdown("**Sender ID provided:**")
            st.code(sender_id if sender_id.strip() else "(none provided)", language=None)

# ── Sidebar — About ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### About This System")
    st.markdown("""
    This tool was developed as a final year computer science project at the
    **Federal University of Lafia**.

    **Author:** Clement Neko Promise

    **Model:** Random Forest Classifier
    
    **Dataset:** ExAIS_SMS Corpus  
    (Abayomi-Alli et al., 2022)  
    3,886 Nigerian SMS messages

    **Performance:**
    - Accuracy: **87.40%**
    - Precision: **83.74%**
    - Recall: **82.59%**
    - F1-Score: **83.16%**
    
    **Key feature:** Nigerian Pidgin  
    normalisation using a custom  
    lexicon
    
    ---
    
    This tool is for educational  
    purposes. Always verify admission  
    status through official JAMB channels.
    """)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Detection of Fake Undergraduate Admission/SMS Alerts in Nigerian Universities
    Using Machine Learning Techniques<br>
    Clement Neko Promise | Computer Science | Federal University of Lafia | 2026
</div>
""", unsafe_allow_html=True)