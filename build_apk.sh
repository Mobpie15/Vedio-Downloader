#!/bin/bash
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
