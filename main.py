#!/usr/bin/env python3
"""
GoHighLevel to IntakeQ Integration
Main entry point for the application.
"""

import os
from dotenv import load_dotenv
from src.api.webhook_server import create_app

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    app = create_app()
    host = "0.0.0.0"  # Heroku requires this
    port = int(os.environ.get("PORT", 5001))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    app.run(host=host, port=port, debug=debug)
