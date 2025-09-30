from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import yt_dlp
import threading
import os
import subprocess
import sys
import requests
from io import BytesIO
import time
import json
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Global variables to track download progress
download_progress = {}
active_downloads = {}

class VideoDownloader:
    def __init__(self):
        self.video_info = None
        self.instagram_preview = None
        self.video_formats = []
        self.audio_formats = []
    
    def progress_hook(self, d, download_id):
        """Progress hook for yt-dlp downloads"""
        try:
            status = d.get('status')
            if status == 'downloading':
                percent_str = d.get('_percent_str') or f"{d.get('percent', 0):.1f}%"
                speed_str = d.get('_speed_str') or self._human_readable(d.get('speed'))
                eta_str = d.get('_eta_str') or str(d.get('eta')) if d.get('eta') else 'NA'
                
                # Extract percentage
                try:
                    percent = float(percent_str.strip().replace('%', ''))
                except:
                    total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                    downloaded = d.get('downloaded_bytes') or 0
                    percent = (downloaded / total * 100) if total else 0
                
                download_progress[download_id] = {
                    'status': 'downloading',
                    'percent': percent,
                    'speed': speed_str,
                    'eta': eta_str
                }
            
            elif status == 'finished':
                download_progress[download_id] = {
                    'status': 'finalizing',
                    'percent': 100,
                    'speed': '',
                    'eta': 'Finalizing...'
                }
        except Exception as e:
            print(f"Progress hook error: {e}")
    
    def _human_readable(self, bytes_per_sec):
        if not bytes_per_sec:
            return ""
        try:
            b = float(bytes_per_sec)
        except:
            return ""
        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        i = 0
        while b >= 1024 and i < len(units) - 1:
            b /= 1024.0
            i += 1
        return f"{b:.2f} {units[i]}"
    
    def fetch_youtube_info(self, url):
        """Fetch YouTube video information"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'logger': None,  # Disable logging to avoid the error
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
            # Process formats
            formats = info.get('formats', [])
            video_formats = []
            audio_formats = []
            
            # Video formats
            for fmt in formats:
                if (fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none' and 
                    fmt.get('ext') == 'mp4'):
                    height = fmt.get('height')
                    if height:
                        video_formats.append({
                            'height': height,
                            'format_id': fmt['format_id'],
                            'ext': fmt.get('ext', 'mp4'),
                            'filesize': fmt.get('filesize'),
                            'quality': f"{height}p",
                            'has_audio': True
                        })
                
                elif (fmt.get('vcodec') != 'none' and fmt.get('acodec') == 'none' and 
                      fmt.get('ext') in ['mp4', 'webm']):
                    height = fmt.get('height')
                    if height and height >= 240:
                        video_formats.append({
                            'height': height,
                            'format_id': fmt['format_id'],
                            'ext': fmt.get('ext', 'mp4'),
                            'filesize': fmt.get('filesize'),
                            'quality': f"{height}p",
                            'has_audio': False
                        })
                
                # Audio formats
                elif (fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none'):
                    abr = fmt.get('abr', 0)
                    ext = fmt.get('ext', '')
                    if abr and ext in ['m4a', 'mp3', 'aac']:
                        audio_formats.append({
                            'abr': abr,
                            'format_id': fmt['format_id'],
                            'ext': ext,
                            'filesize': fmt.get('filesize'),
                            'quality': f"{int(abr)}kbps"
                        })
            
            # Remove duplicates and sort
            video_formats = self._remove_duplicate_formats(video_formats)
            video_formats.sort(key=lambda x: x['height'], reverse=True)
            audio_formats.sort(key=lambda x: x['abr'], reverse=True)
            
            return {
                'success': True,
                'title': info.get('title', 'Unknown Title'),
                'duration': self._format_duration(info.get('duration', 0)),
                'views': self._format_views(info.get('view_count', 0)),
                'thumbnail': info.get('thumbnail'),
                'video_formats': video_formats,
                'audio_formats': audio_formats,
                'url': url
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def fetch_instagram_info(self, url):
        """Fetch Instagram video information"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'logger': None,  # Disable logging to avoid the error
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            return {
                'success': True,
                'title': info.get('title', 'Instagram Reel'),
                'uploader': info.get('uploader', 'Unknown User'),
                'thumbnail': info.get('thumbnail'),
                'url': url
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _remove_duplicate_formats(self, formats):
        """Remove duplicate formats with same height"""
        seen = {}
        for fmt in formats:
            height = fmt['height']
            if height not in seen:
                seen[height] = fmt
            elif fmt.get('has_audio', False) and not seen[height].get('has_audio', False):
                seen[height] = fmt
        return list(seen.values())
    
    def _format_duration(self, seconds):
        if not seconds:
            return "Unknown"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def _format_views(self, views):
        if not views:
            return "Unknown"
        
        if views >= 1_000_000:
            return f"{views/1_000_000:.1f}M"
        elif views >= 1_000:
            return f"{views/1_000:.1f}K"
        else:
            return str(views)

# Initialize downloader
downloader = VideoDownloader()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch_info', methods=['POST'])
def fetch_info():
    data = request.json
    url = data.get('url', '').strip()
    platform = data.get('platform', 'youtube')
    
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'})
    
    if platform == 'youtube':
        if 'youtube.com' not in url and 'youtu.be' not in url:
            return jsonify({'success': False, 'error': 'Invalid YouTube URL'})
        return jsonify(downloader.fetch_youtube_info(url))
    else:
        if 'instagram.com' not in url:
            return jsonify({'success': False, 'error': 'Invalid Instagram URL'})
        return jsonify(downloader.fetch_instagram_info(url))

@app.route('/api/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    platform = data.get('platform', 'youtube')
    quality = data.get('quality')
    format_type = data.get('format_type', 'video')
    download_path = data.get('download_path', './downloads')
    
    if not url or not quality:
        return jsonify({'success': False, 'error': 'URL and quality are required'})
    
    # Create download directory
    os.makedirs(download_path, exist_ok=True)
    
    # Generate unique download ID
    download_id = str(uuid.uuid4())
    
    def download_thread():
        try:
            download_progress[download_id] = {
                'status': 'starting',
                'percent': 0,
                'speed': '',
                'eta': 'Starting...'
            }
            
            if platform == 'youtube':
                download_youtube(url, quality, format_type, download_path, download_id)
            else:
                download_instagram(url, download_path, download_id)
                
            download_progress[download_id] = {
                'status': 'completed',
                'percent': 100,
                'speed': '',
                'eta': 'Completed!'
            }
            
        except Exception as e:
            download_progress[download_id] = {
                'status': 'error',
                'percent': 0,
                'speed': '',
                'eta': f'Error: {str(e)}'
            }
    
    # Start download in background
    thread = threading.Thread(target=download_thread, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'download_id': download_id})

@app.route('/api/progress/<download_id>')
def get_progress(download_id):
    progress = download_progress.get(download_id, {
        'status': 'unknown',
        'percent': 0,
        'speed': '',
        'eta': 'Unknown'
    })
    return jsonify(progress)

def download_youtube(url, quality, format_type, download_path, download_id):
    """Download YouTube video"""
    prefer_aac_audio = "bestaudio[ext=m4a]/bestaudio[ext=aac]/bestaudio"
    
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'noprogress': True,
        'progress_hooks': [lambda d: downloader.progress_hook(d, download_id)],
    }
    
    if format_type == "video":
        # Parse quality (e.g., "720p (with audio)" or "720p (video only)")
        height = int(quality.split('p')[0])
        
        # Find matching format
        video_format = None
        for fmt in downloader.video_formats:
            if fmt['height'] == height:
                video_format = fmt
                break
        
        if video_format and video_format.get('has_audio'):
            ydl_opts['format'] = video_format['format_id']
        else:
            ydl_opts['format'] = f"best[height<={height}]+{prefer_aac_audio}/best"
        
        ydl_opts['merge_output_format'] = 'mp4'
    else:
        # Audio only
        ydl_opts['format'] = prefer_aac_audio
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_instagram(url, download_path, download_id):
    """Download Instagram reel"""
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(uploader)s_%(title)s.%(ext)s'),
        'format': 'best[ext=mp4]/best',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        'quiet': True,
        'noprogress': True,
        'progress_hooks': [lambda d: downloader.progress_hook(d, download_id)]
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    os.makedirs('./downloads', exist_ok=True)
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
