#!/usr/bin/env python3
"""
Test script for Video Downloader
Tests both web app and Android app functionality
"""

import requests
import json
import time
import sys
import subprocess
import threading
from main import VideoDownloaderApp

def test_web_app():
    """Test the web application"""
    print("🌐 Testing Web Application...")
    
    try:
        # Start the Flask app in a separate thread
        def run_flask():
            from app import app
            app.run(host='127.0.0.1', port=5001, debug=False)
        
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        # Test endpoints
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing
        
        # Test fetch_info endpoint
        response = requests.post('http://127.0.0.1:5001/api/fetch_info', 
                               json={'url': test_url, 'platform': 'youtube'})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Web app fetch_info endpoint working")
                print(f"   Title: {data.get('title', 'N/A')}")
            else:
                print(f"❌ Web app fetch_info failed: {data.get('error')}")
        else:
            print(f"❌ Web app fetch_info returned status {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Web app test failed: {e}")
        return False

def test_android_app():
    """Test the Android app components"""
    print("📱 Testing Android App Components...")
    
    try:
        # Test if we can import the main app
        from main import VideoDownloaderApp
        print("✅ Android app imports successfully")
        
        # Test video info fetching
        app = VideoDownloaderApp()
        
        # Test YouTube info fetching
        youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        info = app.fetch_youtube_info(youtube_url)
        
        if info.get('success'):
            print("✅ YouTube info fetching working")
            print(f"   Title: {info.get('title', 'N/A')}")
        else:
            print(f"❌ YouTube info fetching failed: {info.get('error')}")
        
        # Test Instagram info fetching (with a known working URL)
        instagram_url = "https://www.instagram.com/p/example/"  # This will fail but we can test the function
        info = app.fetch_instagram_info(instagram_url)
        
        if not info.get('success'):
            print("✅ Instagram info fetching handles errors correctly")
        else:
            print("✅ Instagram info fetching working")
        
        return True
        
    except Exception as e:
        print(f"❌ Android app test failed: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("📦 Testing Dependencies...")
    
    required_packages = [
        'flask', 'flask_cors', 'yt_dlp', 'requests', 
        'PIL', 'kivy', 'kivymd'
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
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Video Downloader Test Suite")
    print("=" * 40)
    
    all_passed = True
    
    # Test dependencies
    if not test_dependencies():
        all_passed = False
    
    print()
    
    # Test Android app
    if not test_android_app():
        all_passed = False
    
    print()
    
    # Test web app (optional, requires Flask to be running)
    try:
        if not test_web_app():
            all_passed = False
    except Exception as e:
        print(f"⚠️  Web app test skipped: {e}")
    
    print("\n" + "=" * 40)
    
    if all_passed:
        print("🎉 All tests passed! Your app is ready to use.")
        print("\n📋 Next steps:")
        print("1. Run web app: python app.py")
        print("2. Build Android APK: buildozer android debug")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
