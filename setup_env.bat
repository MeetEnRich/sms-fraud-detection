@echo off
echo ============================================
echo  fake_admission_detection — Environment Setup
echo ============================================

cd /d C:\Users\onahe\OneDrive\Desktop\StudentProjects\fake_admission_detection

echo.
echo [1/4] Creating virtual environment...
python -m venv venv

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/4] Installing dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip --prefer-binary
venv\Scripts\python.exe -m pip install pandas numpy scikit-learn imbalanced-learn matplotlib seaborn wordcloud joblib streamlit ipykernel notebook openpyxl --prefer-binary

echo.
echo [4/4] Registering Jupyter kernel...
venv\Scripts\python.exe -m ipykernel install --user --name=fake_admission_env --display-name "Python (fake_admission_env)"

echo.
echo ============================================
echo  Setup complete.
echo  To activate later:  venv\Scripts\activate
echo  To run notebooks:   jupyter notebook
echo  To run app:         streamlit run app\app.py
echo ============================================
pause