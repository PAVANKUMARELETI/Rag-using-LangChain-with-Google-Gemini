#!/usr/bin/env python3
"""
Python 3.8 Compatible Installation Script
"""
import subprocess
import sys

def install_python38_compatible():
    """Install packages compatible with Python 3.8"""
    
    print("🐍 Python 3.8 Compatible Installation")
    print("=" * 40)
    
    # Core packages that work with Python 3.8
    packages = [
        "langchain<0.1.0",  # Older version compatible with Python 3.8
        "google-generativeai>=0.3.0",
        "chromadb>=0.3.0,<0.4.0",  # Older version for compatibility
        "pypdf>=3.0.0",
        "streamlit>=1.20.0",
        "plotly>=5.0.0",
        "python-dotenv>=1.0.0",
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "streamlit-chat",
        "streamlit-option-menu",
        "requests",
        "beautifulsoup4"
    ]
    
    print("📦 Installing Python 3.8 compatible packages...")
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True)
            print(f"✅ {package}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  {package} failed, trying without version constraint...")
            try:
                package_name = package.split('<')[0].split('>')[0].split('=')[0]
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package_name
                ], capture_output=True)
                print(f"✅ {package_name} (fallback)")
            except:
                print(f"❌ {package_name} failed")
    
    print("\n🧪 Testing imports...")
    test_packages = [
        ('streamlit', 'streamlit'),
        ('google.generativeai', 'google-generativeai'),
        ('plotly', 'plotly'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy')
    ]
    
    working_packages = []
    for import_name, package_name in test_packages:
        try:
            __import__(import_name)
            working_packages.append(package_name)
            print(f"✅ {import_name}")
        except ImportError:
            print(f"❌ {import_name}")
    
    print(f"\n📊 Summary: {len(working_packages)}/{len(test_packages)} core packages working")
    
    if len(working_packages) >= 3:  # Minimum needed for basic functionality
        print("🎉 Minimum requirements met! You can run the basic app.")
        return True
    else:
        print("❌ Not enough packages installed for basic functionality")
        return False

if __name__ == "__main__":
    success = install_python38_compatible()
    
    if success:
        print("\n🚀 Next steps:")
        print("1. python streamlit_basic.py  # Run basic app")
        print("2. streamlit run streamlit_basic.py  # Alternative")
        print("\n💡 Note: Some advanced features may not work with Python 3.8")
    else:
        print("\n💡 Try manual installation:")
        print("pip install streamlit google-generativeai plotly pandas numpy")
    
    exit(0 if success else 1)
