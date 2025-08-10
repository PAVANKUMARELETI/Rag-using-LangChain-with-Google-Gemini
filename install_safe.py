#!/usr/bin/env python3
"""
Simple installation script that handles dependency issues gracefully.
"""
import subprocess
import sys
import os
from pathlib import Path

def install_with_fallbacks():
    """Try different installation strategies."""
    
    print("🚀 RAG Installation Script")
    print("=" * 40)
    
    strategies = [
        ("Flexible requirements", ["pip", "install", "-r", "requirements-flexible.txt"]),
        ("Core packages only", ["pip", "install", "streamlit", "plotly", "langchain", "google-generativeai", "chromadb", "pypdf", "python-dotenv", "pandas", "numpy"]),
        ("One by one (safe)", None)  # Special case
    ]
    
    for strategy_name, command in strategies:
        print(f"\n📦 Trying: {strategy_name}")
        
        if command is None:
            # Install one by one
            packages = [
                "streamlit>=1.28.0",
                "plotly>=5.15.0", 
                "langchain>=0.1.0",
                "google-generativeai>=0.3.0",
                "chromadb>=0.4.0",
                "pypdf>=4.0.0",
                "python-dotenv>=1.0.0",
                "pandas>=2.0.0",
                "numpy>=1.24.0",
                "streamlit-chat",
                "streamlit-option-menu"
            ]
            
            success = True
            for package in packages:
                try:
                    print(f"   Installing {package}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                        capture_output=True, text=True)
                    print(f"   ✅ {package} installed")
                except subprocess.CalledProcessError as e:
                    print(f"   ⚠️  {package} failed, continuing...")
                    continue
            
            if success:
                print("✅ One-by-one installation completed")
                return True
        else:
            try:
                result = subprocess.run([sys.executable, "-m"] + command, 
                                      capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"✅ {strategy_name} successful!")
                    return True
                else:
                    print(f"❌ {strategy_name} failed:")
                    print(f"   {result.stderr}")
            
            except subprocess.TimeoutExpired:
                print(f"⏱️  {strategy_name} timed out")
            except Exception as e:
                print(f"❌ {strategy_name} error: {e}")
    
    print("\n❌ All installation strategies failed")
    print("\n💡 Manual installation:")
    print("   pip install streamlit plotly langchain google-generativeai chromadb")
    return False

def test_installation():
    """Test if key packages can be imported."""
    test_packages = [
        'streamlit',
        'plotly', 
        'langchain',
        'google.generativeai',
        'chromadb'
    ]
    
    print("\n🧪 Testing installation...")
    all_good = True
    
    for package in test_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            all_good = False
    
    return all_good

def main():
    """Main installation function."""
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return 1
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Install packages
    if not install_with_fallbacks():
        return 1
    
    # Test installation
    if not test_installation():
        print("\n⚠️  Some packages failed to install, but core functionality may still work")
    else:
        print("\n🎉 Installation successful!")
    
    # Create directories
    directories = ["data/documents", "outputs", "vector_db"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("\n📁 Created directories")
    print("\n🚀 Ready to run!")
    print("   python run_app.py")
    print("   or")
    print("   streamlit run streamlit_app.py")
    
    return 0

if __name__ == "__main__":
    exit(main())
