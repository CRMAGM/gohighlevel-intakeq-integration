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

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
