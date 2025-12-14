from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import re
import tempfile
from urllib.parse import urlparse, parse_qs
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create downloads directory if it doesn't exist
DOWNLOADS_DIR = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


def detect_platform(url):
    """Detect which platform the URL belongs to"""
    url_lower = url.lower()
    
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'youtube'
    elif 'linkedin.com' in url_lower:
        return 'linkedin'
    elif 'twitter.com' in url_lower or 'x.com' in url_lower:
        return 'twitter'
    elif 'instagram.com' in url_lower:
        return 'instagram'
    else:
        return 'unknown'


def get_video_info(url, platform):
    """Get video information without downloading"""
    try:
        # Configure yt-dlp options to bypass YouTube bot detection
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            # Bypass YouTube bot detection
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls'],  # Skip formats that might trigger bot detection
                }
            },
            # Additional options to appear more like a browser
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Keep-Alive': '300',
                'Connection': 'keep-alive',
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            if 'formats' in info:
                for fmt in info['formats']:
                    if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':  # Video with audio
                        formats.append({
                            'format_id': fmt.get('format_id'),
                            'ext': fmt.get('ext', 'mp4'),
                            'resolution': fmt.get('resolution', 'unknown'),
                            'quality': fmt.get('quality', 0),
                            'filesize': fmt.get('filesize', 0),
                        })
            
            return {
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'formats': formats[:10],  # Limit to 10 formats
                'platform': platform
            }
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error getting video info: {error_msg}")
        
        # Check for YouTube bot detection error
        if 'bot' in error_msg.lower() or 'cookies' in error_msg.lower() or 'Sign in to confirm' in error_msg:
            # Return user-friendly error message
            raise Exception(
                "YouTube is temporarily blocking automated access. "
                "This is a known issue with YouTube's bot detection. "
                "Please try again in a few minutes, or the video may require authentication."
            )
        raise


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    """Analyze video URL and return information"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        platform = detect_platform(url)
        if platform == 'unknown':
            return jsonify({'error': 'Unsupported platform. Please use YouTube, LinkedIn, X (Twitter), or Instagram.'}), 400
        
        video_info = get_video_info(url, platform)
        return jsonify(video_info)
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error analyzing video: {error_msg}")
        
        # Check for YouTube bot detection error
        if 'bot' in error_msg.lower() or 'cookies' in error_msg.lower() or 'Sign in to confirm' in error_msg:
            return jsonify({
                'error': 'YouTube is temporarily blocking automated access. Please try again in a few minutes.'
            }), 503  # Service Unavailable
        
        return jsonify({'error': f'Failed to analyze video: {error_msg}'}), 500


@app.route('/api/download', methods=['POST'])
def download_video():
    """Download video with specified format"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        format_id = data.get('format_id', 'best')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        platform = detect_platform(url)
        if platform == 'unknown':
            return jsonify({'error': 'Unsupported platform'}), 400
        
        # Configure download options with bot detection bypass
        ydl_opts = {
            'format': format_id if format_id != 'best' else 'best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            'quiet': False,
            # Bypass YouTube bot detection
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls'],
                }
            },
            # Additional options to appear more like a browser
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Keep-Alive': '300',
                'Connection': 'keep-alive',
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Clean filename
            safe_filename = re.sub(r'[<>:"/\\|?*]', '', os.path.basename(filename))
            filepath = os.path.join(DOWNLOADS_DIR, safe_filename)
            
            if os.path.exists(filename):
                if filename != filepath:
                    os.rename(filename, filepath)
                return jsonify({
                    'success': True,
                    'filename': safe_filename,
                    'filepath': filepath,
                    'title': info.get('title', 'Unknown')
                })
            else:
                return jsonify({'error': 'Download failed - file not found'}), 500
                
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error downloading video: {error_msg}")
        
        # Check for YouTube bot detection error
        if 'bot' in error_msg.lower() or 'cookies' in error_msg.lower() or 'Sign in to confirm' in error_msg:
            return jsonify({
                'error': 'YouTube is temporarily blocking automated access. Please try again in a few minutes.'
            }), 503  # Service Unavailable
        
        return jsonify({'error': f'Download failed: {error_msg}'}), 500


@app.route('/api/download-file/<filename>')
def download_file(filename):
    """Serve downloaded file"""
    try:
        filepath = os.path.join(DOWNLOADS_DIR, filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error serving file: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

