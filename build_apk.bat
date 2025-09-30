@echo off
echo 🚀 Building Video Downloader APK...

REM Set up environment
set ANDROID_HOME=%USERPROFILE%\Android\Sdk
set PATH=%PATH%;%ANDROID_HOME%\tools;%ANDROID_HOME%\platform-tools

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install requirements
pip install -r requirements_android.txt

REM Install python-for-android
pip install python-for-android

REM Build APK
p4a apk --private . --package=org.mobpie.videodownloader --name="Video Downloader" --version=1.0 --bootstrap=sdl2 --requirements=python3,kivy,kivymd,requests,yt-dlp,Pillow --arch=arm64-v8a,armeabi-v7a

echo ✅ APK build completed!
echo 📱 APK location: dist\
pause
