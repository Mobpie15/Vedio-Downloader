# 📱 How to Build APK on Windows

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
