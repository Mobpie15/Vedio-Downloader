from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import threading
import requests
import json
import os
import subprocess
import sys
import yt_dlp
import uuid
from io import BytesIO

class VideoDownloaderApp(App):
    def build(self):
        self.title = "Video Downloader"
        self.current_platform = "youtube"
        self.video_info = None
        self.download_progress = {}
        self.active_downloads = {}
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='📺 Video Downloader',
            size_hint_y=None,
            height=60,
            font_size=24,
            bold=True
        )
        main_layout.add_widget(header)
        
        # Platform selector
        platform_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        self.youtube_btn = ToggleButton(
            text='🎥 YouTube',
            group='platform',
            state='down'
        )
        self.youtube_btn.bind(on_press=self.switch_platform)
        
        self.instagram_btn = ToggleButton(
            text='📱 Instagram',
            group='platform'
        )
        self.instagram_btn.bind(on_press=self.switch_platform)
        
        platform_layout.add_widget(self.youtube_btn)
        platform_layout.add_widget(self.instagram_btn)
        main_layout.add_widget(platform_layout)
        
        # URL input
        url_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        url_label = Label(text='Video URL:', size_hint_y=None, height=30)
        self.url_input = TextInput(
            hint_text='https://www.youtube.com/watch?v=...',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        url_layout.add_widget(url_label)
        url_layout.add_widget(self.url_input)
        main_layout.add_widget(url_layout)
        
        # Fetch button
        self.fetch_btn = Button(
            text='Fetch Video Info',
            size_hint_y=None,
            height=50
        )
        self.fetch_btn.bind(on_press=self.fetch_video_info)
        main_layout.add_widget(self.fetch_btn)
        
        # Video info section
        self.video_info_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        self.video_info_layout.opacity = 0
        
        # Video thumbnail
        self.thumbnail = Image(
            size_hint_y=None,
            height=120,
            allow_stretch=True,
            keep_ratio=True
        )
        self.video_info_layout.add_widget(self.thumbnail)
        
        # Video details
        self.video_title = Label(
            text='',
            size_hint_y=None,
            height=30,
            text_size=(None, None),
            halign='center'
        )
        self.video_duration = Label(
            text='',
            size_hint_y=None,
            height=25,
            font_size=12
        )
        self.video_views = Label(
            text='',
            size_hint_y=None,
            height=25,
            font_size=12
        )
        
        self.video_info_layout.add_widget(self.video_title)
        self.video_info_layout.add_widget(self.video_duration)
        self.video_info_layout.add_widget(self.video_views)
        
        main_layout.add_widget(self.video_info_layout)
        
        # Quality selection
        self.quality_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120)
        self.quality_layout.opacity = 0
        
        # Format selection
        format_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        
        self.video_format_btn = ToggleButton(
            text='🎬 Video',
            group='format',
            state='down'
        )
        self.audio_format_btn = ToggleButton(
            text='🎵 Audio',
            group='format'
        )
        
        format_layout.add_widget(self.video_format_btn)
        format_layout.add_widget(self.audio_format_btn)
        self.quality_layout.add_widget(format_layout)
        
        # Quality spinner
        quality_label = Label(text='Quality:', size_hint_y=None, height=30)
        self.quality_spinner = Spinner(
            text='Select quality...',
            size_hint_y=None,
            height=40
        )
        
        self.quality_layout.add_widget(quality_label)
        self.quality_layout.add_widget(self.quality_spinner)
        
        main_layout.add_widget(self.quality_layout)
        
        # Download button
        self.download_btn = Button(
            text='📥 Download',
            size_hint_y=None,
            height=50
        )
        self.download_btn.bind(on_press=self.download_video)
        main_layout.add_widget(self.download_btn)
        
        # Progress section
        self.progress_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        self.progress_layout.opacity = 0
        
        self.progress_bar = ProgressBar(
            max=100,
            size_hint_y=None,
            height=30
        )
        self.progress_text = Label(
            text='',
            size_hint_y=None,
            height=30
        )
        
        self.progress_layout.add_widget(self.progress_bar)
        self.progress_layout.add_widget(self.progress_text)
        
        main_layout.add_widget(self.progress_layout)
        
        # Status label
        self.status_label = Label(
            text='',
            size_hint_y=None,
            height=30,
            color=(1, 0, 0, 1)
        )
        main_layout.add_widget(self.status_label)
        
        return main_layout
    
    def switch_platform(self, instance):
        if instance.text == '🎥 YouTube':
            self.current_platform = 'youtube'
            self.url_input.hint_text = 'https://www.youtube.com/watch?v=...'
        else:
            self.current_platform = 'instagram'
            self.url_input.hint_text = 'https://www.instagram.com/reel/...'
        
        self.hide_video_info()
        self.hide_quality_selection()
        self.hide_progress()
        self.show_status('')
    
    def fetch_video_info(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.show_status('Please enter a valid URL', error=True)
            return
        
        self.fetch_btn.text = 'Fetching...'
        self.fetch_btn.disabled = True
        self.show_status('Fetching video information...')
        
        # Run in background thread
        threading.Thread(target=self._fetch_info_thread, args=(url,), daemon=True).start()
    
    def _fetch_info_thread(self, url):
        try:
            if self.current_platform == 'youtube':
                info = self.fetch_youtube_info(url)
            else:
                info = self.fetch_instagram_info(url)
            
            Clock.schedule_once(lambda dt: self._on_info_fetched(info))
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_fetch_error(str(e)))
    
    def _on_info_fetched(self, info):
        self.fetch_btn.text = 'Fetch Video Info'
        self.fetch_btn.disabled = False
        
        if info.get('success'):
            self.video_info = info
            self.display_video_info(info)
            self.show_quality_selection()
            self.show_status('Video info fetched successfully!')
        else:
            self.show_status(f'Error: {info.get("error", "Unknown error")}', error=True)
    
    def _on_fetch_error(self, error):
        self.fetch_btn.text = 'Fetch Video Info'
        self.fetch_btn.disabled = False
        self.show_status(f'Error: {error}', error=True)
    
    def fetch_youtube_info(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'logger': None,  # Disable logging to avoid the error
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            formats = info.get('formats', [])
            video_formats = []
            audio_formats = []
            
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
    
    def display_video_info(self, info):
        # Load thumbnail
        try:
            if info.get('thumbnail'):
                response = requests.get(info['thumbnail'])
                self.thumbnail.texture = Image(BytesIO(response.content)).texture
        except:
            pass
        
        self.video_title.text = info.get('title', 'Unknown Title')
        
        if self.current_platform == 'youtube':
            self.video_duration.text = f"Duration: {info.get('duration', 'Unknown')}"
            self.video_views.text = f"Views: {info.get('views', 'Unknown')}"
        else:
            self.video_duration.text = f"By: @{info.get('uploader', 'Unknown')}"
            self.video_views.text = ""
        
        self.show_video_info()
    
    def show_video_info(self):
        self.video_info_layout.opacity = 1
        self.video_info_layout.size_hint_y = None
        self.video_info_layout.height = 200
    
    def hide_video_info(self):
        self.video_info_layout.opacity = 0
        self.video_info_layout.size_hint_y = None
        self.video_info_layout.height = 0
    
    def show_quality_selection(self):
        self.quality_layout.opacity = 1
        self.quality_layout.size_hint_y = None
        self.quality_layout.height = 120
        
        # Update quality options
        self.quality_spinner.values = ['Select quality...']
        
        if self.current_platform == 'youtube' and self.video_info:
            if self.video_format_btn.state == 'down' and self.video_info.get('video_formats'):
                for fmt in self.video_info['video_formats']:
                    self.quality_spinner.values.append(
                        f"{fmt['quality']}{' (with audio)' if fmt.get('has_audio') else ' (video only)'}"
                    )
            elif self.audio_format_btn.state == 'down' and self.video_info.get('audio_formats'):
                for fmt in self.video_info['audio_formats']:
                    self.quality_spinner.values.append(f"{fmt['quality']} ({fmt['ext']})")
        else:
            self.quality_spinner.values.append('Best Available')
            self.quality_spinner.text = 'Best Available'
    
    def hide_quality_selection(self):
        self.quality_layout.opacity = 0
        self.quality_layout.size_hint_y = None
        self.quality_layout.height = 0
    
    def download_video(self, instance):
        if not self.video_info or self.quality_spinner.text == 'Select quality...':
            self.show_status('Please select a quality option', error=True)
            return
        
        self.download_btn.text = 'Downloading...'
        self.download_btn.disabled = True
        self.show_progress()
        self.show_status('Starting download...')
        
        # Run download in background thread
        threading.Thread(target=self._download_thread, daemon=True).start()
    
    def _download_thread(self):
        try:
            download_id = str(uuid.uuid4())
            url = self.url_input.text.strip()
            quality = self.quality_spinner.text
            
            if self.current_platform == 'youtube':
                self.download_youtube(url, quality, download_id)
            else:
                self.download_instagram(url, download_id)
            
            Clock.schedule_once(lambda dt: self._on_download_complete())
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_download_error(str(e)))
    
    def download_youtube(self, url, quality, download_id):
        download_path = self.get_download_path()
        os.makedirs(download_path, exist_ok=True)
        
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'noprogress': True,
            'progress_hooks': [lambda d: self.progress_hook(d, download_id)],
        }
        
        if self.video_format_btn.state == 'down':
            # Video format
            if 'p' in quality:
                height = int(quality.split('p')[0])
                ydl_opts['format'] = f"best[height<={height}]+bestaudio/best"
            else:
                ydl_opts['format'] = 'best'
            ydl_opts['merge_output_format'] = 'mp4'
        else:
            # Audio format
            ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio[ext=aac]/bestaudio'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    def download_instagram(self, url, download_id):
        download_path = self.get_download_path()
        os.makedirs(download_path, exist_ok=True)
        
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(uploader)s_%(title)s.%(ext)s'),
            'format': 'best[ext=mp4]/best',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            'quiet': True,
            'noprogress': True,
            'progress_hooks': [lambda d: self.progress_hook(d, download_id)]
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    def progress_hook(self, d, download_id):
        try:
            status = d.get('status')
            if status == 'downloading':
                percent = d.get('percent', 0)
                speed = d.get('_speed_str', '')
                eta = d.get('_eta_str', '')
                
                Clock.schedule_once(lambda dt: self.update_progress(percent, speed, eta))
            elif status == 'finished':
                Clock.schedule_once(lambda dt: self.update_progress(100, '', 'Completed!'))
        except Exception as e:
            print(f"Progress hook error: {e}")
    
    def update_progress(self, percent, speed, eta):
        self.progress_bar.value = percent
        self.progress_text.text = f"{percent:.1f}% - {eta}"
        if speed:
            self.progress_text.text += f" ({speed})"
    
    def show_progress(self):
        self.progress_layout.opacity = 1
        self.progress_layout.size_hint_y = None
        self.progress_layout.height = 80
    
    def hide_progress(self):
        self.progress_layout.opacity = 0
        self.progress_layout.size_hint_y = None
        self.progress_layout.height = 0
    
    def _on_download_complete(self):
        self.download_btn.text = '📥 Download'
        self.download_btn.disabled = False
        self.hide_progress()
        self.show_status('Download completed successfully!')
    
    def _on_download_error(self, error):
        self.download_btn.text = '📥 Download'
        self.download_btn.disabled = False
        self.hide_progress()
        self.show_status(f'Download failed: {error}', error=True)
    
    def get_download_path(self):
        if platform == 'android':
            return '/storage/emulated/0/Download/VideoDownloader'
        else:
            return './downloads'
    
    def show_status(self, message, error=False):
        self.status_label.text = message
        if error:
            self.status_label.color = (1, 0, 0, 1)  # Red
        else:
            self.status_label.color = (0, 0.7, 0, 1)  # Green

if __name__ == '__main__':
    VideoDownloaderApp().run()
