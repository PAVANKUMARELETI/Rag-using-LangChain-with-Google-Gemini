#!/usr/bin/env python3
"""
Launch script for the RAG Streamlit application.
"""
import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed."""
    required_packages = [
        ('streamlit', 'streamlit'),
        ('plotly', 'plotly'),
        ('langchain', 'langchain'),
        ('google.generativeai', 'google-generativeai'),
        ('chromadb', 'chromadb')
    ]
    
    missing_packages = []
    
    for package_name, pip_name in required_packages:
        try:
            __import__(package_name)
            print(f"✅ {package_name} found")
        except ImportError:
            missing_packages.append(pip_name)
            print(f"❌ {package_name} missing")
    
    if missing_packages:
        print(f"📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            # Try flexible requirements first
            if Path("requirements-flexible.txt").exists():
                print("📦 Trying flexible requirements...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-flexible.txt"])
            else:
                print("📦 Installing from main requirements...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            
            print("✅ Dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("💡 Try installing manually:")
            print("   pip install streamlit plotly langchain google-generativeai chromadb")
            print("   Or use: pip install -r requirements-flexible.txt")
            return False
    else:
        print("✅ All required dependencies found")
        return True

def launch_app():
    """Launch the Streamlit application."""
    print("🚀 Starting RAG Streamlit Application...")
    print("🌐 The app will open in your default web browser")
    print("🛑 Press Ctrl+C to stop the application")
    
    try:
        # Ensure we're in the correct directory
        app_path = Path(__file__).parent / "streamlit_app.py"
        
        if not app_path.exists():
            print(f"❌ Application file not found: {app_path}")
            return False
        
        # Launch Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(app_path),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--theme.primaryColor", "#1f77b4",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f0f2f6"
        ]
        
        subprocess.run(cmd)
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        return False

def main():
    """Main launcher function."""
    print("🤖 RAG using LangChain with Google Gemini")
    print("=" * 50)
    
    # Check if in correct directory
    if not Path("streamlit_app.py").exists():
        print("❌ Please run this script from the project root directory")
        print("   The directory should contain 'streamlit_app.py'")
        return 1
    
    # Check requirements
    if not check_requirements():
        return 1
    
    # Create necessary directories
    directories = ["data/documents", "outputs", "vector_db"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("📁 Created necessary directories")
    
    # Launch application
    success = launch_app()
    
    if success:
        print("👋 Thank you for using RAG with Gemini!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main())
