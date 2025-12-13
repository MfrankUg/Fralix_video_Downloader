"""
Minimal test file to verify Vercel Python setup works
This helps isolate if the issue is with Flask or yt-dlp
"""
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

def handler(request):
    """Simple test handler"""
    logger.info("Test handler called")
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"status": "ok", "message": "Test handler works"}'
    }

logger.info("Test module loaded")

