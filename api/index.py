import os
import re
import tempfile
import logging
import sys
from urllib.parse import urlparse, parse_qs

# Configure logging first - write to stderr so Vercel can see it
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Import Flask first (most critical)
try:
    from flask import Flask, render_template, request, jsonify, send_file
    logger.info("Flask imported successfully")
except ImportError as e:
    logger.error(f"Flask import error: {str(e)}")
    raise

try:
    from flask_cors import CORS
    logger.info("flask-cors imported successfully")
except ImportError as e:
    logger.error(f"flask-cors import error: {str(e)}")
    raise

# Lazy-load yt_dlp - don't import it at module level to avoid initialization issues
yt_dlp = None
def get_yt_dlp():
    """Lazy load yt-dlp to avoid initialization crashes"""
    global yt_dlp
    if yt_dlp is None:
        try:
            import yt_dlp as ytdlp
            yt_dlp = ytdlp
            logger.info("yt-dlp imported successfully")
        except ImportError as e:
            logger.error(f"yt-dlp import error: {str(e)}")
            raise
    return yt_dlp

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

logger.info(f"BASE_DIR: {BASE_DIR}")
logger.info(f"PROJECT_ROOT: {PROJECT_ROOT}")

# Initialize Flask app
try:
    static_path = os.path.join(PROJECT_ROOT, 'static')
    template_path = os.path.join(PROJECT_ROOT, 'templates')
    
    logger.info(f"Static folder: {static_path}, exists: {os.path.exists(static_path)}")
    logger.info(f"Template folder: {template_path}, exists: {os.path.exists(template_path)}")
    
    app = Flask(__name__, 
                static_folder=static_path,
                template_folder=template_path)
    CORS(app)
    logger.info("Flask app initialized successfully")
except Exception as e:
    logger.error(f"Flask app initialization error: {str(e)}")
    raise

# Logging already configured above

# Use /tmp for downloads in Vercel (only writable directory)
DOWNLOADS_DIR = os.path.join(tempfile.gettempdir(), 'downloads')
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
        ytdlp = get_yt_dlp()  # Lazy load yt-dlp
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
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
        logger.error(f"Error getting video info: {str(e)}")
        raise


@app.route('/')
def index():
    """Render the main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        return f"Error loading page: {str(e)}", 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200


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
        logger.error(f"Error analyzing video: {str(e)}")
        return jsonify({'error': f'Failed to analyze video: {str(e)}'}), 500


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
        
        # Configure download options
        ytdlp = get_yt_dlp()  # Lazy load yt-dlp
        ydl_opts = {
            'format': format_id if format_id != 'best' else 'best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            'quiet': False,
        }
        
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
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
        logger.error(f"Error downloading video: {str(e)}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500


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


# Vercel serverless function handler
# Export the Flask app - Vercel Python runtime will use this
# The handler variable is what Vercel looks for
logger.info("Setting handler = app")
handler = app
logger.info("Handler set successfully")

# Log that module loaded successfully
logger.info("Module api/index.py loaded successfully")

