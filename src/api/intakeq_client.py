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
        self.base_url = "https://api.intakeq.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger(__name__)
        if not self.api_key:
            raise ValueError("INTAKEQ_API_KEY environment variable is not set")
        logging.info(f"IntakeQ API Key found: {self.api_key[:4]}...")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make a request to the IntakeQ API."""
        url = f"{self.base_url}/{endpoint}"
        kwargs['headers'] = self.headers
        response = requests.request(method, url, **kwargs)
        self.logger.info(f"{method} {endpoint} response status: {response.status_code}")
        if response.text:
            self.logger.info(f"{method} {endpoint} raw response: {response.text}")
        return response
    
    def create_client(self, client_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new client in IntakeQ"""
        try:
            # Map client data to IntakeQ format
            intakeq_client = {
                "FirstName": client_data.get('firstName'),
                "LastName": client_data.get('lastName'),
                "Email": client_data.get('email'),
                "Phone": client_data.get('phone', '').replace('+', ''),
                "City": client_data.get('city'),
                "State": client_data.get('state'),
                "PostalCode": client_data.get('zipCode'),
                "DateOfBirth": client_data.get('dateOfBirth'),
                "CustomFields": []
            }
            
            # Map custom fields
            custom_fields = client_data.get('customFields', {})
            
            # Map height and weight fields
            if 'Height Feet' in custom_fields:
                intakeq_client["CustomFields"].append({
                    "FieldId": "sotc",
                    "Text": "Height Feet",
                    "Value": str(custom_fields['Height Feet'])
                })
            
            if 'Height Inches' in custom_fields:
                intakeq_client["CustomFields"].append({
                    "FieldId": "o0a0",
                    "Text": "Height Inches",
                    "Value": str(custom_fields['Height Inches'])
                })
            
            if 'Current Weight?' in custom_fields:
                intakeq_client["CustomFields"].append({
                    "FieldId": "n0dx",
                    "Text": "Current Weight?",
                    "Value": str(custom_fields['Current Weight?'])
                })
            
            if 'Target Weight' in custom_fields:
                intakeq_client["CustomFields"].append({
                    "FieldId": "fovf",
                    "Text": "Target Weight",
                    "Value": str(custom_fields['Target Weight'])
                })

            if 'Currently Taking' in custom_fields:
                intakeq_client["CustomFields"].append({
                    "FieldId": "fudl",
                    "Text": "Currently Taking",
                    "Value": str(custom_fields['Currently Taking'])
                })

            if 'State_options' in custom_fields:
                intakeq_client["CustomFields"].append({
                    "FieldId": "8fjy",
                    "Text": "State_options",
                    "Value": str(custom_fields['State_options'])
                })

            # Search for existing client by email
            search_response = self._make_request("GET", "clients", params={"email": client_data.get('email')})
            
            if search_response.status_code == 200:
                existing_clients = search_response.json()
                if existing_clients:
                    # Update existing client
                    client_id = existing_clients[0]['ClientId']
                    update_response = self._make_request("PUT", f"clients/{client_id}", json=intakeq_client)
                    
                    if update_response.status_code == 200:
                        self.logger.info(f"Successfully updated client {client_id}")
                        
                        # Add tags if present
                        if "tags" in client_data:
                            for tag in client_data["tags"]:
                                self._add_tag_to_client(client_id, tag)
                        
                        return update_response.json()
                    else:
                        self.logger.error(f"Failed to update client: {update_response.text}")
                        return None
                else:
                    # Create new client
                    create_response = self._make_request("POST", "clients", json=intakeq_client)
                    
                    if create_response.status_code == 200:
                        new_client = create_response.json()
                        self.logger.info(f"Successfully created client {new_client['ClientId']}")
                        
                        # Add tags if present
                        if "tags" in client_data:
                            for tag in client_data["tags"]:
                                self._add_tag_to_client(new_client["ClientId"], tag)
                        
                        return new_client
                    else:
                        self.logger.error(f"Failed to create client: {create_response.text}")
                        return None
            else:
                self.logger.error(f"Failed to search for client: {search_response.text}")
                return None

        except Exception as e:
            self.logger.error(f"Error creating client in IntakeQ: {str(e)}")
            return None

    def _add_tag_to_client(self, client_id: int, tag: str) -> bool:
        """Add a tag to a client"""
        try:
            response = self._make_request("POST", f"clients/{client_id}/tags", json={"tag": tag})
            
            if response.status_code == 200:
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
            return response.json()
        except Exception as e:
            logging.error(f"Error searching clients: {str(e)}")
            return [] 