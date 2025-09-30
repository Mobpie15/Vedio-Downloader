#!/usr/bin/env python3
"""
Alternative APK Building Script for Windows
This script provides an alternative way to build APK when buildozer doesn't work on Windows
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

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

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'kivy', 'kivymd', 'requests', 'yt_dlp', 'Pillow'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        for package in missing_packages:
            run_command(f"pip install {package}", f"Installing {package}")
    
    return True

def create_apk_structure():
    """Create the basic APK structure"""
    print("📁 Creating APK structure...")
    
    # Create directories
    dirs = ['apk_build', 'apk_build/assets', 'apk_build/res', 'apk_build/src']
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    return True

def create_android_manifest():
    """Create AndroidManifest.xml"""
    manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.mobpie.videodownloader"
    android:versionCode="1"
    android:versionName="1.0">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="Video Downloader"
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen">
        
        <activity
            android:name="org.kivy.android.PythonActivity"
            android:label="Video Downloader"
            android:screenOrientation="portrait"
            android:configChanges="keyboardHidden|orientation|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
    
    with open('apk_build/AndroidManifest.xml', 'w') as f:
        f.write(manifest_content)
    
    print("✅ AndroidManifest.xml created")
    return True

def create_build_script():
    """Create a build script for the APK"""
    build_script = '''#!/bin/bash
# Build script for Video Downloader APK

echo "🚀 Building Video Downloader APK..."

# Set up environment
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements_android.txt

# Install python-for-android
pip install python-for-android

# Build APK
p4a apk --private . --package=org.mobpie.videodownloader --name="Video Downloader" --version=1.0 --bootstrap=sdl2 --requirements=python3,kivy,kivymd,requests,yt-dlp,Pillow --arch=arm64-v8a,armeabi-v7a

echo "✅ APK build completed!"
echo "📱 APK location: dist/"
'''
    
    with open('build_apk.sh', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # Make it executable on Unix systems
    if os.name != 'nt':
        os.chmod('build_apk.sh', 0o755)
    
    print("✅ Build script created")
    return True

def create_windows_build_script():
    """Create a Windows batch file for building APK"""
    build_script = '''@echo off
echo 🚀 Building Video Downloader APK...

REM Set up environment
set ANDROID_HOME=%USERPROFILE%\\Android\\Sdk
set PATH=%PATH%;%ANDROID_HOME%\\tools;%ANDROID_HOME%\\platform-tools

REM Create virtual environment
python -m venv venv
call venv\\Scripts\\activate.bat

REM Install requirements
pip install -r requirements_android.txt

REM Install python-for-android
pip install python-for-android

REM Build APK
p4a apk --private . --package=org.mobpie.videodownloader --name="Video Downloader" --version=1.0 --bootstrap=sdl2 --requirements=python3,kivy,kivymd,requests,yt-dlp,Pillow --arch=arm64-v8a,armeabi-v7a

echo ✅ APK build completed!
echo 📱 APK location: dist\\
pause
'''
    
    with open('build_apk.bat', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    print("✅ Windows build script created")
    return True

def create_simple_apk_guide():
    """Create a simple guide for building APK"""
    guide_content = '''# 📱 How to Build APK on Windows

## Method 1: Using Python-for-Android (Recommended)

### Prerequisites:
1. Install Android Studio
2. Set up Android SDK
3. Install Java JDK

### Steps:
1. Open Command Prompt as Administrator
2. Run: `python build_apk.py`
3. Follow the instructions

## Method 2: Using WSL (Windows Subsystem for Linux)

### Prerequisites:
1. Install WSL2
2. Install Ubuntu in WSL
3. Install buildozer in WSL

### Steps:
1. Open WSL terminal
2. Navigate to project directory
3. Run: `buildozer android debug`

## Method 3: Using Online Build Services

### Option A: GitHub Actions
1. Push code to GitHub
2. Use GitHub Actions to build APK
3. Download APK from Actions artifacts

### Option B: GitLab CI
1. Push code to GitLab
2. Use GitLab CI to build APK
3. Download APK from CI artifacts

## Method 4: Using Docker

### Prerequisites:
1. Install Docker Desktop
2. Install WSL2

### Steps:
1. Run: `docker run -it --rm -v %cd%:/app kivy/buildozer android debug`
2. APK will be in bin/ directory

## Troubleshooting:

### Common Issues:
1. **Java not found**: Install Java JDK and set JAVA_HOME
2. **Android SDK not found**: Install Android Studio and set ANDROID_HOME
3. **Build fails**: Check internet connection and try again
4. **Permission denied**: Run as Administrator

### Alternative Solutions:
1. Use online APK builders
2. Use cloud build services
3. Use Linux VM or WSL
4. Use GitHub Actions for automated builds
'''
    
    with open('APK_BUILD_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ APK build guide created")
    return True

def main():
    """Main function"""
    print("🚀 Video Downloader APK Builder")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        return False
    
    # Create APK structure
    if not create_apk_structure():
        print("❌ Failed to create APK structure")
        return False
    
    # Create Android manifest
    if not create_android_manifest():
        print("❌ Failed to create Android manifest")
        return False
    
    # Create build scripts
    if not create_build_script():
        print("❌ Failed to create build script")
        return False
    
    if not create_windows_build_script():
        print("❌ Failed to create Windows build script")
        return False
    
    # Create guide
    if not create_simple_apk_guide():
        print("❌ Failed to create guide")
        return False
    
    print("\n🎉 APK build setup completed!")
    print("\n📋 Next steps:")
    print("1. Install Android Studio and Android SDK")
    print("2. Set ANDROID_HOME environment variable")
    print("3. Run: build_apk.bat (Windows) or ./build_apk.sh (Linux/Mac)")
    print("4. Or follow the guide in APK_BUILD_GUIDE.md")
    
    print("\n⚠️  Note: Building APK on Windows can be challenging.")
    print("   Consider using WSL2, Docker, or online build services.")
    
    return True

if __name__ == "__main__":
    main()
