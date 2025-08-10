@echo off
title RAG Basic - Python 3.8 Compatible

echo.
echo ========================================
echo   RAG Basic - Python 3.8 Compatible
echo ========================================
echo.

:: Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3.8+ required
    pause
    exit /b 1
)

echo Python version check: OK

:: Install basic packages that work with Python 3.8
echo.
echo Installing Python 3.8 compatible packages...

python -m pip install streamlit google-generativeai plotly pandas numpy requests beautifulsoup4 streamlit-chat streamlit-option-menu

if errorlevel 1 (
    echo.
    echo Some packages failed to install. Trying core packages only...
    python -m pip install streamlit google-generativeai plotly
    
    if errorlevel 1 (
        echo Error: Failed to install core packages
        echo Please install manually: pip install streamlit google-generativeai
        pause
        exit /b 1
    )
)

echo.
echo Testing installation...
python -c "import streamlit, google.generativeai; print('Core packages working!')" >nul 2>&1
if errorlevel 1 (
    echo Error: Core packages not working
    pause
    exit /b 1
)

echo.
echo ✅ Installation successful!
echo.
echo Starting basic RAG application...
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop
echo.

streamlit run streamlit_basic.py --server.port 8501

pause
