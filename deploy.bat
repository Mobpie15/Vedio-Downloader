@echo off
echo 🚀 Video Downloader Deployment Script
echo ======================================

echo.
echo Choose deployment option:
echo 1. Build Android APK
echo 2. Build Docker image for web deployment
echo 3. Deploy to Heroku
echo 4. Deploy to Railway
echo 5. All of the above

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto build_apk
if "%choice%"=="2" goto build_docker
if "%choice%"=="3" goto deploy_heroku
if "%choice%"=="4" goto deploy_railway
if "%choice%"=="5" goto deploy_all
goto invalid_choice

:build_apk
echo 📱 Building Android APK...
pip install buildozer
buildozer android debug
echo ✅ APK built successfully! Check bin/ directory
goto end

:build_docker
echo 🐳 Building Docker image...
docker build -t video-downloader .
echo ✅ Docker image built successfully!
echo To run: docker run -p 5000:5000 video-downloader
goto end

:deploy_heroku
echo ☁️ Deploying to Heroku...
heroku create video-downloader-%RANDOM%
git add .
git commit -m "Deploy video downloader"
git push heroku main
echo ✅ Deployed to Heroku!
goto end

:deploy_railway
echo 🚂 Deploying to Railway...
npm install -g @railway/cli
railway login
railway init
railway up
echo ✅ Deployed to Railway!
goto end

:deploy_all
echo 🔄 Running all deployment options...

echo 📱 Building Android APK...
pip install buildozer
buildozer android debug

echo 🐳 Building Docker image...
docker build -t video-downloader .

echo ☁️ Deploying to Heroku...
heroku create video-downloader-%RANDOM%
git add .
git commit -m "Deploy video downloader"
git push heroku main

echo 🚂 Deploying to Railway...
npm install -g @railway/cli
railway login
railway init
railway up

echo ✅ All deployments completed!
goto end

:invalid_choice
echo ❌ Invalid choice. Please run the script again.
goto end

:end
echo.
echo 🎉 Deployment process completed!
echo.
echo 📱 Android APK: Check bin/ directory
echo 🌐 Web App: Check your deployment platform
echo 🐳 Docker: Run with 'docker run -p 5000:5000 video-downloader'
pause
