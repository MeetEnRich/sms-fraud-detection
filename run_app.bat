@echo off
echo ===================================================
echo  fake_admission_detection - Launching Application
echo ===================================================

cd /d "%~dp0"

:: Check if the virtual environment exists
if not exist venv (
    echo [ERROR] Virtual environment 'venv' was not found.
    echo Please run 'setup_env.bat' first to install all dependencies.
    echo.
    pause
    exit /b 1
)

echo.
echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [2/2] Starting Streamlit Web App...
echo.
echo Streamlit server starting. Your browser should open automatically...
echo Press Ctrl+C in this terminal window to stop the server.
echo.
streamlit run app\app.py

pause
