# 🔧 Installation Troubleshooting Guide

## The Issue
The error you encountered is related to the `unstructured` library version `0.12.4` not being available in the Python Package Index (PyPI).

## Quick Solutions

### Solution 1: Use the Safe Installer (Recommended)
```bash
python install_safe.py
```
This script tries multiple installation strategies and handles dependency conflicts gracefully.

### Solution 2: Use Flexible Requirements
```bash
pip install -r requirements-flexible.txt
```
This uses version ranges instead of exact versions, making it more compatible.

### Solution 3: Manual Core Installation
```bash
pip install streamlit plotly langchain google-generativeai chromadb pypdf python-dotenv pandas numpy
pip install streamlit-chat streamlit-option-menu
```

### Solution 4: Skip Optional Packages
The `unstructured` library is optional. You can run the app without it:
```bash
pip install --no-deps streamlit plotly langchain google-generativeai chromadb pypdf python-dotenv pandas numpy streamlit-chat streamlit-option-menu
```

## What I Fixed

1. **Updated requirements.txt**: Commented out the problematic `unstructured==0.12.4` package
2. **Created requirements-flexible.txt**: Uses version ranges instead of exact versions
3. **Enhanced run_app.py**: Better error handling and fallback installation
4. **Updated run_app.bat**: Multiple installation strategies
5. **Created install_safe.py**: Comprehensive installation script with fallbacks

## Testing Your Installation

After trying any solution above, test with:
```bash
python -c "import streamlit, plotly, langchain; print('✅ Core packages working!')"
```

## Running the App

Once installed, you can run:
```bash
python run_app.py
```
or
```bash
streamlit run streamlit_app.py
```

## Common Issues & Solutions

### Issue: Package conflicts
**Solution**: Use a virtual environment
```bash
python -m venv rag_env
rag_env\Scripts\activate  # Windows
pip install -r requirements-flexible.txt
```

### Issue: Slow installation
**Solution**: Use faster package manager
```bash
pip install --upgrade pip
pip install -r requirements-flexible.txt --no-cache-dir
```

### Issue: Permission errors
**Solution**: Install for user only
```bash
pip install -r requirements-flexible.txt --user
```

### Issue: Network/proxy issues
**Solution**: Use trusted hosts
```bash
pip install -r requirements-flexible.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
```

## Alternative: Minimal Installation

If you just want to test the core functionality:
```bash
pip install streamlit google-generativeai langchain pypdf python-dotenv
```

This gives you basic RAG functionality without all the extras.

## Verification Steps

1. **Test imports**:
   ```python
   import streamlit as st
   import google.generativeai as genai
   from langchain_google_genai import ChatGoogleGenerativeAI
   print("✅ All core imports successful!")
   ```

2. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Check in browser**: App should open at `http://localhost:8501`

## Getting Help

If you're still having issues:
1. Try the safe installer: `python install_safe.py`
2. Check your Python version: `python --version` (needs 3.8+)
3. Update pip: `python -m pip install --upgrade pip`
4. Use a fresh virtual environment

## What's Working Now

✅ Fixed version conflicts  
✅ Made unstructured library optional  
✅ Added multiple installation fallbacks  
✅ Created flexible requirements  
✅ Enhanced error handling  

Your RAG app should now install and run smoothly! 🚀
