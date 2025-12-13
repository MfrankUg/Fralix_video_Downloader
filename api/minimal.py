"""
Minimal Flask app for testing Vercel deployment
Use this to verify basic Flask functionality works
"""
import sys
import logging

# Configure logging to stderr (Vercel can see this)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

try:
    logger.info("Starting minimal Flask app...")
    
    from flask import Flask, jsonify
    logger.info("Flask imported successfully")
    
    app = Flask(__name__)
    logger.info("Flask app created")
    
    @app.route('/')
    def home():
        logger.info("Home route called")
        return jsonify({
            'status': 'ok',
            'message': 'Minimal Flask app is working!',
            'version': 'minimal-test'
        })
    
    @app.route('/health')
    def health():
        logger.info("Health check called")
        return jsonify({
            'status': 'ok',
            'message': 'Server is running'
        })
    
    # Vercel handler
    handler = app
    logger.info("Handler set successfully")
    logger.info("Minimal app loaded successfully!")
    
except Exception as e:
    logger.error(f"Error in minimal app: {str(e)}", exc_info=True)
    raise

