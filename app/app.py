"""
Detection of Fake Undergraduate Admission/SMS Alerts
Streamlit Web Application
Upgraded UI/UX Design & Logic (No Emojis, Professional Layout)
"""

import os
import sys
import re
import streamlit as st
import joblib

# Add project root to path so src/ imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.preprocessor import preprocess

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Admission/SMS Fraud Detector",
    page_icon=None,
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

# ── Heuristic logic & Helper functions ────────────────────────────────────────

def verify_sender_id(sender: str, message: str) -> dict:
    """
    Heuristic check for Sender ID context.
    Returns a dict with state ('VERIFIED', 'SUSPICIOUS', 'UNVERIFIED'), label, and styling.
    """
    sender = str(sender).strip().upper()
    message_lower = message.lower()
    
    # Official white-listed senders (Verified)
    verified_keywords = {'JAMB', 'CAPS', '55019', 'FULAFIAPORTAL', 'FULAFIASMS', 'FULAFIADVC', 'FULAFIA'}
    
    # Check if the sender format resembles a standard Nigerian mobile number
    is_mobile_number = False
    clean_sender = re.sub(r'\s+', '', sender)
    if re.match(r'^(\+234|0)[789][01]\d{8}$', clean_sender):
        is_mobile_number = True
        
    # Heuristics:
    # 1. Match verified whitelist keywords
    if any(k in sender for k in verified_keywords):
        return {
            'state': 'VERIFIED',
            'label': 'Verified Source',
            'color': '#16a34a',
            'bg': '#f0fdf4',
            'border': '1px solid #bbf7d0',
            'desc': 'Recognized official communication channel.'
        }
        
    # 2. Match standard mobile number claiming official context (Highly Suspicious)
    scam_context_words = {'jamb', 'caps', 'admission', 'portal', 'pay', 'upgrade', 'result', 'sorting', 'runs'}
    if is_mobile_number and any(w in message_lower for w in scam_context_words):
        return {
            'state': 'SUSPICIOUS',
            'label': 'Suspicious Source',
            'color': '#dc2626',
            'bg': '#fef2f2',
            'border': '1px solid #fecaca',
            'desc': 'Warning: A private mobile number is claiming to send official admission details. This is highly characteristic of fraud.'
        }
        
    if is_mobile_number:
        return {
            'state': 'UNVERIFIED',
            'label': 'Private Sender',
            'color': '#2563eb',
            'bg': '#eff6ff',
            'border': '1px solid #bfdbfe',
            'desc': 'Sent from a private mobile number.'
        }
        
    if not sender:
        return {
            'state': 'UNVERIFIED',
            'label': 'No Sender ID',
            'color': '#64748b',
            'bg': '#f8fafc',
            'border': '1px solid #cbd5e1',
            'desc': 'No Sender ID was provided for validation.'
        }
        
    return {
        'state': 'UNVERIFIED',
        'label': 'Unverified Sender',
        'color': '#475569',
        'bg': '#f1f5f9',
        'border': '1px solid #cbd5e1',
        'desc': 'Unverified sender ID. Always cross-check alerts on the official university portal.'
    }


def highlight_keywords(text: str) -> str:
    """
    Highlight critical spam words and admission keywords in HTML spans.
    """
    high_risk = {
        'free', 'urgent', 'pay', 'send', 'account', 'acct', 'n50', 'n100', 'bal', 
        'upgrade', 'wash', 'runz', 'runs', 'sorting', 'expo', 'miracle', 'special', 
        'click', 'link', 'portal', 'verify', 'confirm', 'win', 'won', 'dial', 'call', 
        'money', 'expire', 'expired'
    }
    
    admission_terms = {
        'jamb', 'caps', 'admission', 'result', 'offer', 'congratulations', 'mtn', 
        'airtel', 'glo', 'etisalat', 'orange', 'mobile', 'official', 'university', 'helpline'
    }
    
    tokens = text.split()
    highlighted = []
    
    for token in tokens:
        # Strip punctuation to extract the root word
        word = re.sub(r'[^a-zA-Z0-9]', '', token).lower()
        if word in high_risk:
            start_idx = token.lower().find(word)
            end_idx = start_idx + len(word)
            prefix = token[:start_idx]
            suffix = token[end_idx:]
            highlighted.append(f'{prefix}<span class="highlight-risk">{token[start_idx:end_idx]}</span>{suffix}')
        elif word in admission_terms:
            start_idx = token.lower().find(word)
            end_idx = start_idx + len(word)
            prefix = token[:start_idx]
            suffix = token[end_idx:]
            highlighted.append(f'{prefix}<span class="highlight-info">{token[start_idx:end_idx]}</span>{suffix}')
        else:
            highlighted.append(token)
            
    return " ".join(highlighted)


# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* Font styling targeted to avoid Streamlit internal icons and layouts */
    html, body, [data-testid="stAppViewContainer"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, div.stButton button, textarea, input {
        font-family: 'Outfit', sans-serif !important;
    }
    
    body {
        background-color: #f8fafc;
    }

    /* Hide Streamlit header to remove empty top space */
    header, [data-testid="stHeader"] {
        display: none !important;
    }

    /* Reduce top padding of the main block container to eliminate empty space */
    .block-container, [data-testid="block-container"] {
        padding-top: 0.5rem !important;
        padding-bottom: 1.5rem !important;
    }

    /* Reduce top padding of the sidebar to make it fit without scrolling */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
    }

    /* Minimalist & Professional Header Styling (No Dark Banner) */
    .title-box {
        text-align: center;
        margin-bottom: 2.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .title-box h1 {
        color: #0f172a;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .title-box p.subtitle {
        color: #475569;
        font-size: 1.05rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    .title-box p.tagline {
        color: #2563eb;
        font-size: 0.85rem;
        margin: 0.5rem 0 0 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Inputs styling */
    textarea, input {
        border-radius: 10px !important;
    }

    /* Upgraded Verify Button */
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px -3px rgba(79, 70, 229, 0.4) !important;
        width: 100%;
        margin-top: 0.5rem;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px -5px rgba(79, 70, 229, 0.6) !important;
        background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%) !important;
    }
    div.stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Result Cards */
    .result-card {
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border: 1px solid rgba(0, 0, 0, 0.03);
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
        transition: all 0.4s ease;
    }
    .result-card.fraud {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe3e3 100%);
        border-left: 8px solid #dc2626;
    }
    .result-card.legit {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 8px solid #16a34a;
    }
    .result-title {
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.01em;
    }
    .result-card.fraud .result-title {
        color: #991b1b;
    }
    .result-card.legit .result-title {
        color: #166534;
    }

    /* Badge tags */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.65rem;
        font-size: 0.75rem;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }

    /* Keyword Highlights */
    .highlight-risk {
        background-color: #fee2e2;
        color: #dc2626;
        border: 1px solid #fca5a5;
        padding: 1px 5px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9em;
        margin: 0 1px;
    }
    .highlight-info {
        background-color: #e0f2fe;
        color: #0284c7;
        border: 1px solid #7dd3fc;
        padding: 1px 5px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9em;
        margin: 0 1px;
    }

    /* Metric Containers */
    .metric-container {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    .metric-card {
        flex: 1;
        background: white;
        padding: 1rem 0.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        text-align: center;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.1rem;
    }
    .metric-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    /* Advice/Info Boxes */
    .advice-box {
        border-radius: 12px;
        padding: 1.2rem;
        margin-top: 1.5rem;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .advice-box.fraud {
        background-color: #fffbeb;
        border-left: 6px solid #d97706;
        color: #78350f;
    }
    .advice-box.legit {
        background-color: #f8fafc;
        border-left: 6px solid #64748b;
        color: #334155;
    }
    .advice-box ul {
        margin: 0.5rem 0 0 0;
        padding-left: 1.2rem;
    }
    .advice-box li {
        margin-bottom: 0.4rem;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 3.5rem;
        border-top: 1px solid #e2e8f0;
        padding-top: 1.5rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-box">
    <h1>SMS Fraud Detection System</h1>
    <p class="subtitle">Detection of Fake Undergraduate Admission & SMS Alerts in Nigerian Universities</p>
    <p class="tagline">Random Forest + Nigerian Pidgin Lexicon | ExAIS_SMS Corpus</p>
</div>
""", unsafe_allow_html=True)

# ── How to use ────────────────────────────────────────────────────────────────
with st.expander("Read user guide"):
    st.markdown("""
    1. **Paste** the suspicious SMS message into the text box below.
    2. Optionally enter the **Sender ID** (phone number or name header) shown on your screen.
    3. Click **Verify Message**.
    4. The system will classify the message as **Legitimate** or **Fraudulent** using standard NLP normalization and display risk analytics.
    
    > **Security Alert:** If a message is flagged as suspicious or fraudulent, do **not** call any phone numbers, click any links, or make transfers. Verify admission status directly on the official JAMB CAPS e-Facility portal at [efacility.jamb.gov.ng](https://efacility.jamb.gov.ng).
    """)

# ── Input form ────────────────────────────────────────────────────────────────
st.markdown("### Verify a Suspicious SMS")

sender_id = st.text_input(
    "Sender ID (optional)",
    placeholder="e.g. JAMB, 55019, or a 11-digit phone number...",
    help="Enter the name or phone number that sent the message."
)

message_input = st.text_area(
    "SMS Alert Content",
    placeholder="Paste the complete text of the suspicious SMS message here...",
    height=160,
    help="Paste the exact text of the admission alert SMS you received."
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    verify_btn = st.button("Verify Message", use_container_width=True)

# ── Prediction ────────────────────────────────────────────────────────────────
if verify_btn:
    if not message_input.strip():
        st.error("Please enter a message before clicking Verify.")
    else:
        with st.spinner("Analyzing message text and sender ID..."):
            # Clean and vectorize
            cleaned   = preprocess(message_input)
            vector    = vectoriser.transform([cleaned])
            pred      = rf.predict(vector)[0]
            prob      = rf.predict_proba(vector)[0]
            fraud_prob = prob[1] * 100
            legit_prob = prob[0] * 100
            confidence = prob[pred] * 100
            
            # Cross-reference Sender ID heuristics
            sender_info = verify_sender_id(sender_id, message_input)

        st.markdown("---")
        st.markdown("### Risk Analysis Results")

        # Sender ID classification badge
        badge_html = f'<div class="badge" style="background-color: {sender_info["bg"]}; color: {sender_info["color"]}; border: {sender_info["border"]}">{sender_info["label"]}</div>'
        st.markdown(badge_html, unsafe_allow_html=True)
        st.caption(sender_info['desc'])

        if pred == 1:
            # FRAUDULENT
            st.markdown(f"""
            <div class="result-card fraud">
                <div class="result-title">FRAUDULENT MESSAGE DETECTED</div>
                <p style="margin:0; font-size: 0.98rem; line-height:1.5;">
                    This message has been classified as a <strong>fraudulent/spam SMS</strong> with <strong>{confidence:.1f}% confidence</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Metric Cards
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-card" style="border-top: 4px solid #dc2626;">
                    <div class="metric-val" style="color: #dc2626;">{fraud_prob:.1f}%</div>
                    <div class="metric-label">Fraud Probability</div>
                </div>
                <div class="metric-card">
                    <div class="metric-val">{legit_prob:.1f}%</div>
                    <div class="metric-label">Legitimate Probability</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Styled glowing progress bar
            st.markdown(f"""
            <div style="background-color: #e2e8f0; border-radius: 8px; height: 10px; width: 100%; margin-top: 1rem; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #f87171, #dc2626); height: 100%; width: {fraud_prob}%; border-radius: 8px; box-shadow: 0 0 8px rgba(220, 38, 38, 0.4);"></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="advice-box fraud">
                <strong>Crucial Safety Advice:</strong>
                <ul>
                    <li><strong>Do not reply:</strong> Engaging or calling numbers listed inside the message can lead to phishing.</li>
                    <li><strong>No payments:</strong> Official admission listings are verified online and do not require cash transfers to personal accounts for "runs" or "upgrading".</li>
                    <li><strong>Official Verification:</strong> Log in directly to the official JAMB e-Facility portal at <a href="https://efacility.jamb.gov.ng" target="_blank" style="color: #92400e; font-weight: 700; text-decoration: underline;">efacility.jamb.gov.ng</a>.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        else:
            # LEGITIMATE
            st.markdown(f"""
            <div class="result-card legit">
                <div class="result-title">LEGITIMATE MESSAGE</div>
                <p style="margin:0; font-size: 0.98rem; line-height:1.5;">
                    This message has been classified as <strong>legitimate (safe)</strong> with <strong>{confidence:.1f}% confidence</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Metric Cards
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-card" style="border-top: 4px solid #16a34a;">
                    <div class="metric-val" style="color: #16a34a;">{legit_prob:.1f}%</div>
                    <div class="metric-label">Legitimate Probability</div>
                </div>
                <div class="metric-card">
                    <div class="metric-val">{fraud_prob:.1f}%</div>
                    <div class="metric-label">Fraud Probability</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Styled glowing progress bar
            st.markdown(f"""
            <div style="background-color: #e2e8f0; border-radius: 8px; height: 10px; width: 100%; margin-top: 1rem; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #4ade80, #16a34a); height: 100%; width: {legit_prob}%; border-radius: 8px; box-shadow: 0 0 8px rgba(22, 163, 74, 0.4);"></div>
            </div>
            """, unsafe_allow_html=True)

            if confidence < 75:
                st.markdown("""
                <div class="advice-box fraud" style="background-color: #fffbeb; border-left: 6px solid #d97706; color: #78350f;">
                    <strong>Notice: Low Confidence Classification</strong>
                    <p style="margin-top: 0.25rem;">Even though this message appears legitimate, the model confidence is under 75%. Please verify details on your university e-portal or the JAMB CAPS website before taking action.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="advice-box legit">
                    <strong>Verification Advice:</strong>
                    <p style="margin-top: 0.25rem;">This message is verified as legitimate. However, as a precaution, always confirm official dates and payment procedures on the university's official site.</p>
                </div>
                """, unsafe_allow_html=True)

        # Show preprocessed text with highlight markers (XAI)
        with st.expander("View Preprocessing & Feature Highlighting Details"):
            st.markdown("Detected <span class='highlight-risk'>high-risk flags</span> and <span class='highlight-info'>admissions vocabulary</span> are highlighted below:", unsafe_allow_html=True)
            
            highlighted_orig = highlight_keywords(message_input)
            highlighted_cleaned = highlight_keywords(cleaned)
            
            st.markdown("**Original message (with highlighted flags):**")
            st.markdown(f'<div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 8px; font-family: monospace; font-size: 0.95rem; line-height: 1.6;">{highlighted_orig}</div>', unsafe_allow_html=True)
            
            st.markdown("**Cleaned & normalized message (retained words after TF-IDF vectorization):**")
            st.markdown(f'<div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 8px; font-family: monospace; font-size: 0.95rem; line-height: 1.6;">{highlighted_cleaned if highlighted_cleaned else "<i>(no tokens remained after pipeline cleaning)</i>"}</div>', unsafe_allow_html=True)
            
            st.markdown("**Sender ID details:**")
            st.code(sender_id if sender_id.strip() else "(none provided)", language=None)

# ── Sidebar — About ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### About This System")
    st.markdown("""
    **Model:** Random Forest Classifier  
    **Dataset:** ExAIS_SMS (3.8k Messages)  
    **Performance:** 87.4% Acc / 83.1% F1
    
    ---
    
    Educational purposes only. Verify status through official portals.
    """)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Detection of Fake Undergraduate Admission/SMS Alerts in Nigerian Universities<br>
    Clement Neko Promise | Computer Science | Federal University of Lafia | 2026
</div>
""", unsafe_allow_html=True)