"""
Flask server to handle webhooks from GoHighLevel.
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from src.handlers.webhook_handler import process_webhook

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ]
    )
    
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy"})
    
    @app.route("/webhook/gohighlevel", methods=["POST"])
    def gohighlevel_webhook():
        """Handle webhooks from GoHighLevel."""
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        logging.info(f"Received webhook: {json.dumps(data)}")
        
        # Process the webhook
        try:
            result = process_webhook(data)
            return jsonify(result)
        except Exception as e:
            logging.error(f"Error processing webhook: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    return app
