#!/usr/bin/env python3
"""
Simple Python launcher for the basic RAG app
Works with Python 3.8+ and handles missing dependencies gracefully
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version too old.")
        return False
    return True

def install_basic_packages():
    """Install basic packages required for the app"""
    packages = [
        "streamlit",
        "google-generativeai", 
        "plotly",
        "pandas",
        "numpy"
    ]
    
    print("📦 Installing basic packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  ✅ {package}")
        except subprocess.CalledProcessError:
            print(f"  ❌ Failed to install {package}")
    print()

def run_streamlit_app():
    """Run the streamlit app"""
    script_dir = Path(__file__).parent
    app_file = script_dir / "streamlit_basic.py"
    
    if not app_file.exists():
        print(f"❌ App file not found: {app_file}")
        return False
    
    print("🚀 Starting Streamlit app...")
    print("📱 The app will open in your browser automatically")
    print("🛑 Press Ctrl+C to stop the app")
    print()
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_file)], 
                      check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start app: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
        return True

def main():
    """Main launcher function"""
    print("🤖 RAG with Google Gemini - Basic App Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    print("✅ Python version compatible")
    print()
    
    # Install packages
    install_basic_packages()
    
    # Run app
    success = run_streamlit_app()
    
    if not success:
        print()
        print("💡 Alternative methods:")
        print("   1. Run manually: streamlit run streamlit_basic.py")
        print("   2. Check SOLUTION_SUMMARY.md for more options")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
