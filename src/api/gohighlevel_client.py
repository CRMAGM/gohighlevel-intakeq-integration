"""
Client for interacting with the GoHighLevel API.
"""

import os
import logging
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GoHighLevelClient:
    """Client for interacting with the GoHighLevel API."""
    
    def __init__(self):
        """Initialize the GoHighLevel client."""
        self.base_url = "https://services.leadconnectorhq.com"
        self.client_id = os.getenv("GHL_CLIENT_ID")
        self.client_secret = os.getenv("GHL_CLIENT_SECRET")
        self.access_token = None
    
    def _get_headers(self):
        """Get headers for API requests."""
        if not self.access_token:
            logging.error("No access token available")
            raise ValueError("No access token available")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Version": "2021-07-28",
            "Content-Type": "application/json"
        }
    
    def get_contact(self, contact_id):
        """
        Get a contact by ID.
        
        Args:
            contact_id (str): The ID of the contact
            
        Returns:
            dict: The contact data
        """
        logging.info(f"Getting contact {contact_id} from GoHighLevel")
        
        # TODO: Implement OAuth token retrieval
        # For now, this is a placeholder implementation
        
        # Mock response for development with enhanced fields
        mock_contact = {
            "id": "1872",  # Client ID as specified
            "firstName": "Rolanda",
            "lastName": "Green",
            "email": "mz_green174@yahoo.com",
            "phone": "(773) 726-2196",  # Mobile phone
            "address1": "",  # Address left empty as specified
            "city": "",
            "state": "",
            "postalCode": "",
            "gender": "Female",
            "dateOfBirth": "",  # Empty for now
            "tags": ["paid", "new-customer"],
            "customFields": [
                {
                    "id": "location_field_id",
                    "key": "location",
                    "field_value": "Downtown"
                },
                {
                    "id": "treatment_field_id",
                    "key": "treatment",
                    "field_value": "Weight Loss"
                },
                {
                    "id": "sex_field_id",
                    "key": "sex",
                    "field_value": "Female"
                },
                {
                    "id": "marital_status_field_id",
                    "key": "marital_status",
                    "field_value": ""
                },
                {
                    "id": "height_feet_field_id",
                    "key": "height_feet",
                    "field_value": ""
                },
                {
                    "id": "height_inches_field_id",
                    "key": "height_inches",
                    "field_value": ""
                },
                {
                    "id": "bmi_field_id",
                    "key": "bmi",
                    "field_value": ""
                },
                {
                    "id": "current_weight_field_id",
                    "key": "current_weight",
                    "field_value": ""
                },
                {
                    "id": "target_weight_field_id",
                    "key": "target_weight",
                    "field_value": ""
                },
                {
                    "id": "body_mass_reduction_percentage_field_id",
                    "key": "body_mass_reduction_percentage",
                    "field_value": ""
                },
                {
                    "id": "current_weight_loss_medication_field_id",
                    "key": "current_weight_loss_medication",
                    "field_value": ""
                },
                {
                    "id": "tracking_field_id",
                    "key": "tracking",
                    "field_value": ""
                },
                {
                    "id": "check_all_that_apply_in_the_past_2_weeks_other_field_id",
                    "key": "check_all_that_apply_in_the_past_2_weeks_other",
                    "field_value": "Headache, Fatigue"
                },
                {
                    "id": "if_yes_which_glp1_medication_field_id",
                    "key": "if_yes_which_glp1_medication",
                    "field_value": "Ozempic"
                },
                {
                    "id": "have_you_ever_been_diagnosed_with_any_of_the_following_conditions_field_id",
                    "key": "have_you_ever_been_diagnosed_with_any_of_the_following_conditions",
                    "field_value": "Hypertension, Diabetes"
                },
                {
                    "id": "what_brings_you_here_today_field_id",
                    "key": "what_brings_you_here_today",
                    "field_value": "Weight loss management"
                }
            ]
        }
        
        return mock_contact
