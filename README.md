# 📺 Video Downloader

A powerful video downloader application that supports YouTube and Instagram, available as both a web application and Android APK.

## ✨ Features

- 🎥 **YouTube Support**: Download videos in various qualities (240p to 4K)
- 📱 **Instagram Support**: Download Instagram reels and posts
- 🎵 **Audio Extraction**: Download audio-only versions in MP3 format
- 📱 **Mobile App**: Native Android application built with Kivy
- 🌐 **Web App**: Beautiful web interface with real-time progress tracking
- 📊 **Progress Tracking**: Real-time download progress with speed and ETA
- 🎨 **Modern UI**: Clean, responsive design with smooth animations

## 🚀 Quick Start

### Web Application

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5000`

### Android APK

1. **Install buildozer:**
   ```bash
   pip install buildozer
   ```

2. **Build the APK:**
   ```bash
   buildozer android debug
   ```

3. **Install the APK:**
   The APK will be generated in the `bin/` directory

## 📦 Deployment Options

### 1. Docker Deployment

```bash
# Build Docker image
docker build -t video-downloader .

# Run the container
docker run -p 5000:5000 video-downloader
```

### 2. Heroku Deployment

1. Install Heroku CLI
2. Login to Heroku: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`

### 3. Railway Deployment

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Deploy: `railway up`

### 4. Automated Deployment

Run the deployment script:

**Windows:**
```cmd
deploy.bat
```

**Linux/Mac:**
```bash
./deploy.sh
```

## 🛠️ Development

### Project Structure

```
video_downloader/
├── app.py                 # Flask web application
├── main.py               # Kivy Android application
├── templates/
│   └── index.html        # Web UI template
├── requirements.txt      # Web app dependencies
├── requirements_android.txt # Android app dependencies
├── buildozer.spec       # Android build configuration
├── Dockerfile           # Docker configuration
├── Procfile            # Heroku configuration
└── deploy.bat/deploy.sh # Deployment scripts
```

### Dependencies

**Web Application:**
- Flask 2.3.3
- Flask-CORS 4.0.0
- yt-dlp 2023.9.24
- requests 2.31.0
- Pillow 10.0.1

**Android Application:**
- Kivy 2.1.0
- KivyMD 1.1.1
- yt-dlp 2023.9.24
- requests 2.31.0
- Pillow 10.0.1

## 📱 Android App Features

- **Native Performance**: Built with Kivy for smooth performance
- **Offline Capability**: Works without internet after initial setup
- **File Management**: Downloads saved to device storage
- **Progress Tracking**: Real-time download progress
- **Quality Selection**: Choose from available video/audio qualities

## 🌐 Web App Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Live progress tracking with WebSocket-like updates
- **Modern UI**: Beautiful gradient design with smooth animations
- **Platform Switching**: Easy toggle between YouTube and Instagram
- **Quality Preview**: See available formats before downloading

## 🔧 Configuration

### Android App Configuration

Edit `buildozer.spec` to customize:
- App name and package
- Icon and splash screen
- Permissions
- Target Android versions

### Web App Configuration

Environment variables:
- `PORT`: Server port (default: 5000)
- `FLASK_ENV`: Environment (development/production)

## 📋 Requirements

### System Requirements

**For Web App:**
- Python 3.8+
- FFmpeg (for video processing)
- 2GB RAM minimum

**For Android App:**
- Python 3.8+
- Android SDK
- Buildozer
- 4GB RAM recommended

### Supported Platforms

**Web App:**
- Windows, macOS, Linux
- All modern browsers

**Android App:**
- Android 5.0+ (API level 21+)
- ARM64 and ARMv7 architectures

## 🚨 Troubleshooting

### Common Issues

1. **FFmpeg not found:**
   - Install FFmpeg: `sudo apt install ffmpeg` (Linux) or `brew install ffmpeg` (macOS)

2. **Buildozer build fails:**
   - Update buildozer: `pip install --upgrade buildozer`
   - Clear build cache: `buildozer android clean`

3. **Permission denied on Android:**
   - Enable "Install from unknown sources" in Android settings

4. **Download fails:**
   - Check internet connection
   - Verify video URL is accessible
   - Try different quality options

### Getting Help

- Check the logs in the application
- Ensure all dependencies are installed
- Verify your internet connection
- Try with different video URLs

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Developer

Developed by **Mobpie/Ujjwal Mishra**

- 📧 Email: meujjwal13@gmail.com
- 📱 Instagram: @mobpie_op
- 🎬 YouTube: Mobpie

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect the terms of service of the platforms you're downloading from and only download content you have permission to download.

---

**Happy Downloading! 🎉**
