@echo off
title RAG with Google Gemini - Streamlit App

echo.
echo ========================================
echo   RAG using LangChain with Google Gemini  
echo ========================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

:: Check if we're in the correct directory
if not exist "streamlit_app.py" (
    echo Error: streamlit_app.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

:: Install requirements if needed
echo Checking requirements...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing requirements...
    echo Trying flexible requirements first...
    python -m pip install -r requirements-flexible.txt >nul 2>&1
    if errorlevel 1 (
        echo Flexible install failed, trying main requirements...
        python -m pip install -r requirements.txt >nul 2>&1
        if errorlevel 1 (
            echo Main install failed, trying core packages...
            python -m pip install streamlit plotly langchain google-generativeai chromadb pypdf python-dotenv pandas numpy >nul 2>&1
            if errorlevel 1 (
                echo Error: Failed to install requirements
                echo Please run: python install_safe.py
                pause
                exit /b 1
            )
        )
    )
)

:: Create directories
echo Creating directories...
if not exist "data\documents" mkdir "data\documents"
if not exist "outputs" mkdir "outputs"
if not exist "vector_db" mkdir "vector_db"

:: Launch the app
echo.
echo Starting Streamlit application...
echo The app will open in your default web browser
echo Press Ctrl+C to stop the application
echo.

python -m streamlit run streamlit_app.py --server.port 8501 --server.address localhost

pause
