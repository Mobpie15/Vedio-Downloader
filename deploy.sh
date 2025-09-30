#!/bin/bash

# Video Downloader Deployment Script

echo "🚀 Video Downloader Deployment Script"
echo "======================================"

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer not found. Installing..."
    pip install buildozer
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

echo ""
echo "Choose deployment option:"
echo "1. Build Android APK"
echo "2. Build Docker image for web deployment"
echo "3. Deploy to Heroku"
echo "4. Deploy to Railway"
echo "5. All of the above"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "📱 Building Android APK..."
        buildozer android debug
        echo "✅ APK built successfully! Check bin/ directory"
        ;;
    2)
        echo "🐳 Building Docker image..."
        docker build -t video-downloader .
        echo "✅ Docker image built successfully!"
        echo "To run: docker run -p 5000:5000 video-downloader"
        ;;
    3)
        echo "☁️ Deploying to Heroku..."
        if ! command -v heroku &> /dev/null; then
            echo "Installing Heroku CLI..."
            # Install Heroku CLI based on OS
            if [[ "$OSTYPE" == "darwin"* ]]; then
                brew install heroku/brew/heroku
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                curl https://cli-assets.heroku.com/install.sh | sh
            else
                echo "Please install Heroku CLI manually"
                exit 1
            fi
        fi
        
        heroku create video-downloader-$(date +%s)
        git add .
        git commit -m "Deploy video downloader"
        git push heroku main
        echo "✅ Deployed to Heroku!"
        ;;
    4)
        echo "🚂 Deploying to Railway..."
        if ! command -v railway &> /dev/null; then
            echo "Installing Railway CLI..."
            npm install -g @railway/cli
        fi
        
        railway login
        railway init
        railway up
        echo "✅ Deployed to Railway!"
        ;;
    5)
        echo "🔄 Running all deployment options..."
        
        echo "📱 Building Android APK..."
        buildozer android debug
        
        echo "🐳 Building Docker image..."
        docker build -t video-downloader .
        
        echo "☁️ Deploying to Heroku..."
        heroku create video-downloader-$(date +%s)
        git add .
        git commit -m "Deploy video downloader"
        git push heroku main
        
        echo "🚂 Deploying to Railway..."
        railway login
        railway init
        railway up
        
        echo "✅ All deployments completed!"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment process completed!"
echo ""
echo "📱 Android APK: Check bin/ directory"
echo "🌐 Web App: Check your deployment platform"
echo "🐳 Docker: Run with 'docker run -p 5000:5000 video-downloader'"
