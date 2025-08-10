#!/usr/bin/env python3
"""
Installation and setup script for RAG using LangChain with Google Gemini.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
        print(f"✅ {description} completed successfully")
        return True
    except Exception as e:
        print(f"❌ Error running command: {str(e)}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. You have Python {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_directories():
    """Create necessary directories."""
    directories = [
        "data/documents",
        "outputs",
        "vector_db"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def setup_environment():
    """Set up environment file."""
    env_example = Path("config/.env.example")
    env_file = Path("config/.env")
    
    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print("📄 Created .env file from example")
        print("⚠️  Please edit config/.env and add your Google AI API key")
    elif env_file.exists():
        print("📄 Environment file already exists")
    else:
        print("❌ Could not find config/.env.example")

def main():
    """Main installation function."""
    print("🚀 RAG using LangChain with Google Gemini - Installation Script")
    print("=" * 70)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Install packages
    print("\n📦 Installing Python packages...")
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("❌ Failed to install requirements. You may need to install them manually.")
    
    # Setup environment
    print("\n⚙️  Setting up environment...")
    setup_environment()
    
    # Install package in development mode
    print("\n🔧 Installing package in development mode...")
    run_command("pip install -e .", "Installing package")
    
    print("\n✅ Installation completed!")
    print("\n📋 Next steps:")
    print("1. Edit config/.env and add your Google AI API key")
    print("2. Run 'jupyter notebook app.ipynb' to start the tutorial")
    print("3. Or run 'python src/demo.py' to test the system")
    
    # Check if Jupyter is installed
    if not run_command("jupyter --version", "Checking Jupyter installation"):
        print("\n💡 To install Jupyter, run: pip install jupyter")
    
    return 0

if __name__ == "__main__":
    exit(main())
