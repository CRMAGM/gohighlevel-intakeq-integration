"""
Client for interacting with the IntakeQ API.
"""

import os
import logging
import requests
from dotenv import load_dotenv
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

# Load environment variables
load_dotenv()

class IntakeQClient:
    """Client for interacting with the IntakeQ API."""
    
    def __init__(self, api_key: str):
        """Initialize the IntakeQ client."""
        self.api_key = api_key
        self.base_url = "https://intakeq.com/api/v1"  # Updated base URL
        self.headers = {
            "X-Auth-Key": api_key,  # Using X-Auth-Key header as per API docs
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.logger = logging.getLogger(__name__)
        if not self.api_key:
            raise ValueError("INTAKEQ_API_KEY environment variable is not set")
        logging.info(f"IntakeQ API Key found: {self.api_key[:4]}...")

    def _make_request(self, method, endpoint, data=None):
        """
        Make a request to the IntakeQ API.
        
        Args:
            method (str): HTTP method (GET, POST, PATCH, etc.)
            endpoint (str): API endpoint
            data (dict): Request data
            
        Returns:
            dict: Response data or None if request failed
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            logging.info(f"Making {method} request to {url}")
            if data:
                logging.info(f"Request data: {json.dumps(data)}")
            
            response = requests.request(method, url, headers=self.headers, json=data)
            logging.info(f"Response status: {response.status_code}")
            logging.info(f"Response body: {response.text}")
            
            if response.status_code == 401:
                logging.error("Authentication failed")
                return {"error": "Authentication failed", "status_code": 401}
            
            if response.status_code == 404:
                logging.error("Resource not found")
                return {"error": "Resource not found", "status_code": 404}
            
            response.raise_for_status()
            
            if not response.text:
                return {}
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {str(e)}")
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response: {str(e)}")
            return {"error": f"Invalid JSON response: {str(e)}", "status_code": response.status_code}

    def create_client(self, client_data):
        """
        Create or update a client in IntakeQ.
        
        Args:
            client_data (dict): Client data
            
        Returns:
            dict: Response data
        """
        # Search for existing client by email
        email = client_data.get("Email")
        if not email:
            logging.error("Email is required")
            return None
        
        search_result = self._make_request("GET", f"/clients/search?email={email.lower()}")
        if not search_result or "error" in search_result:
            logging.info("No existing client found, creating new client")
            return self._make_request("POST", "/clients", client_data)
        
        # Update existing client
        client_id = search_result[0].get("ClientId")
        if client_id:
            logging.info(f"Updating existing client {client_id}")
            return self._make_request("PATCH", f"/clients/{client_id}", client_data)
        
        logging.error("Failed to get client ID from search result")
        return None

    def _add_tag_to_client(self, client_id: int, tag: str) -> bool:
        """Add a tag to a client"""
        try:
            response = self._make_request("POST", f"clients/{client_id}/tags", json={"tag": tag})
            
            if response:
                self.logger.info(f"Successfully added tag {tag} to client {client_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error adding tag to client: {str(e)}")
            return False

    def _search_clients_by_email(self, email):
        """Search for clients by email."""
        try:
            response = self._make_request("GET", "clients", params={'search': email})
            return response
        except Exception as e:
            logging.error(f"Error searching clients: {str(e)}")
            return None 