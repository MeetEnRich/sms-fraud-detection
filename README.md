# Admission/SMS Fraud Detection System

An undergraduate final-year Computer Science project at the **Federal University of Lafia** (developed by Clement Neko Promise) designed to detect fraudulent undergraduate admission SMS alerts and messages targeting university applicants in Nigeria.

This system leverages **Random Forest Classification** combined with a custom **Nigerian Pidgin and SMS shorthand normalisation pipeline** to identify fraud indicators related to CAPS, JAMB, result upgrading, exam fraud, and bribery (sorting).

---

## Features

- **Nigerian Pidgin Normalisation**: Translates common Nigerian Pidgin terms (e.g., *abeg*, *sharp sharp*, *sorting*, *runs*) and SMS shorthand abbreviations (e.g., *ur*, *pls*, *txt*) to Standard English to improve NLP matching.
- **Context-Specific Stop Words**: Standard English stop words are filtered out while deliberately retaining words that serve as strong fraud signals in this domain (e.g., *portal*, *account*, *jamb*, *caps*, *pay*, *urgent*, *verify*).
- **Punctuation & Digit Handling**: Removes general punctuation but retains numbers and digits, which represent crucial fraud signals (e.g., phone numbers, bank account details, and monetary charges like N50/N100).
- **Streamlit Web Application**: An interactive user interface to verify suspicious messages, displaying classification results (Legitimate/Fraudulent), model prediction probabilities, safety guidelines, and a view of the preprocessed text.
- **Workflow Notebooks**: Five structured Jupyter Notebooks mapping the entire data pipeline from loading and exploratory data analysis to model training and evaluation.

---

## Directory Structure

```text
fake_admission_detection/
├── app/
│   └── app.py                # Streamlit Web Application
├── data/
│   ├── processed/            # Cleaned and preprocessed datasets (CSV)
│   └── raw/                  # 20 raw user SMS datasets (CSV)
├── models/
│   ├── model.pkl             # Trained Random Forest model binary
│   └── vectoriser.pkl        # Fitted TF-IDF Vectorizer binary
├── notebooks/
│   ├── 01_data_loading.ipynb # Merging and cleaning raw CSV data
│   ├── 02_eda.ipynb          # Exploratory Data Analysis & visualizations
│   ├── 03_preprocessing.ipynb# Text normalisation and TF-IDF extraction
│   ├── 04_training_evaluation.ipynb # Classifier training & testing
│   └── 05_results_summary.ipynb    # Compiling model evaluations & importances
├── src/
│   ├── __init__.py           # Package initializer
│   ├── pidgin_dict.py        # Nigerian Pidgin & SMS shorthand dictionary
│   └── preprocessor.py       # Reusable text preprocessing pipeline functions
├── outputs/
│   ├── figures/              # Generated visualizations
│   └── reports/              # Performance reports & metric CSVs
├── requirements.txt          # Python dependencies
├── run_app.bat               # Run Streamlit Web Application script
├── setup_env.bat             # Automatic environment setup script
└── README.md                 # Project documentation (this file)
```

---

## Model Performance

Both a **Random Forest Classifier** and a **Naïve Bayes Baseline** were trained on the **ExAIS_SMS Corpus** (3,886 messages after preprocessing). The Random Forest model demonstrates superior recall, making it highly effective at minimizing missed fraud cases (False Negatives).

| Model | Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest** | **87.40%** | 83.74% | **82.59%** | **83.16%** |
| **Naïve Bayes (Baseline)** | 85.99% | **84.85%** | 76.45% | 80.43% |

---

## Installation & Setup

### Option 1: Automatic Setup (Windows)
Double-click and run the `setup_env.bat` batch file in the project root. This script will automatically:
1. Create a Python virtual environment (`venv`).
2. Upgrade `pip`.
3. Install all dependencies from `requirements.txt`.
4. Register the virtual environment as a Jupyter Notebook kernel (`fake_admission_env`).

### Option 2: Manual Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - **Windows (CMD/PowerShell)**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Register Jupyter Kernel** (Optional, for running notebooks):
   ```bash
   python -m ipykernel install --user --name=fake_admission_env --display-name "Python (fake_admission_env)"
   ```

---

## How to Run the Project

### 1. Run the Web Application

- **On Windows (Automatic)**:
  Double-click the `run_app.bat` script in the project root. This will automatically activate the virtual environment and start the Streamlit server.

- **Manual (All Platforms)**:
  Make sure your virtual environment is activated, then run the Streamlit web application with:
  ```bash
  streamlit run app/app.py
  ```
  This will start a local development server and automatically open the application in your default web browser (typically at `http://localhost:8501`).

### 2. Run the Jupyter Notebooks
To explore data analysis, processing steps, or retrain models:
```bash
jupyter notebook
```
Open any notebook in the `notebooks/` directory. Ensure you select the registered `fake_admission_env` kernel from the kernel menu for running cells.

---

## Technologies Used

- **Language**: Python 3.8+
- **Machine Learning**: Scikit-Learn, Joblib, Imbalanced-Learn
- **NLP**: Custom regex-based normalisation, TF-IDF Vectorisation
- **Web App**: Streamlit (with Custom CSS styling)
- **Data & Visualisation**: Pandas, NumPy, Matplotlib, Seaborn, WordCloud
- **Interface/IDE**: Jupyter Notebook

---

## Author & Project Info

- **Author**: Clement Neko Promise
- **Major**: Computer Science
- **Institution**: Federal University of Lafia
- **Graduation Year**: 2026
- **Project Title**: *Detection of Fake Undergraduate Admission/SMS Alerts in Nigerian Universities Using Machine Learning Techniques*
