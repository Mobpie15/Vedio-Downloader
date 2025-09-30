#!/usr/bin/env python3
"""
Video Downloader Setup Script
Automatically installs dependencies and sets up the environment
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def install_python_packages():
    """Install required Python packages"""
    packages = [
        "flask==2.3.3",
        "flask-cors==4.0.0", 
        "yt-dlp==2023.9.24",
        "requests==2.31.0",
        "Pillow==10.0.1",
        "werkzeug==2.3.7"
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    return True

def install_buildozer():
    """Install buildozer for Android APK building"""
    return run_command("pip install buildozer", "Installing buildozer")

def install_ffmpeg():
    """Install FFmpeg based on the operating system"""
    system = platform.system().lower()
    
    if system == "linux":
        return run_command("sudo apt update && sudo apt install -y ffmpeg", "Installing FFmpeg (Linux)")
    elif system == "darwin":  # macOS
        return run_command("brew install ffmpeg", "Installing FFmpeg (macOS)")
    elif system == "windows":
        print("⚠️  Please install FFmpeg manually on Windows:")
        print("   1. Download from https://ffmpeg.org/download.html")
        print("   2. Add to your PATH environment variable")
        return True
    else:
        print(f"⚠️  Unsupported operating system: {system}")
        print("   Please install FFmpeg manually")
        return True

def create_directories():
    """Create necessary directories"""
    directories = ["downloads", "bin"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 Video Downloader Setup")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install Python packages
    if not install_python_packages():
        print("❌ Failed to install Python packages")
        sys.exit(1)
    
    # Install buildozer
    if not install_buildozer():
        print("❌ Failed to install buildozer")
        sys.exit(1)
    
    # Install FFmpeg
    if not install_ffmpeg():
        print("❌ Failed to install FFmpeg")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run web app: python app.py")
    print("2. Build Android APK: buildozer android debug")
    print("3. Deploy to cloud: run deploy.bat (Windows) or ./deploy.sh (Linux/Mac)")
    print("\n📚 For more information, check README.md")

if __name__ == "__main__":
    main()
