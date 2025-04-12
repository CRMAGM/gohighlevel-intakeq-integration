#!/usr/bin/env python3
"""
Test script for the GoHighLevel to IntakeQ integration.
This script simulates a webhook event from GoHighLevel and tests the integration.
"""

import os
import json
import logging
import requests
from dotenv import load_dotenv
from src.handlers.webhook_handler import process_webhook

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

def simulate_webhook_event():
    """
    Simulate a webhook event from GoHighLevel for a contact being tagged with "paid".
    """
    # Sample webhook payload for a contact.tag.added event
    webhook_payload = {
        "event": "contact.tag.added",
        "locationId": "ve9EPM428h8vShlRW1KT",
        "payload": {
            "contactId": "sample_contact_123",
            "tagName": "paid",
            "tagId": "tag_123"
        }
    }
    
    logging.info("Simulating webhook event: contact.tag.added with 'paid' tag")
    
    # Process the webhook
    try:
        result = process_webhook(webhook_payload)
        logging.info(f"Webhook processing result: {result}")
        return result
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        raise

def test_intakeq_api():
    """
    Test direct connection to IntakeQ API.
    """
    api_key = os.getenv("INTAKEQ_API_KEY")
    if not api_key:
        logging.error("IntakeQ API key not found in environment variables")
        return False
    
    logging.info("Testing IntakeQ API connection")
    
    # Test endpoint (get clients)
    url = "https://intakeq.com/api/v1/clients"
    headers = {
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            logging.info("Successfully connected to IntakeQ API")
            return True
        else:
            logging.error(f"Failed to connect to IntakeQ API: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error connecting to IntakeQ API: {str(e)}")
        return False

def main():
    """
    Main function to run the integration tests.
    """
    print("Running GoHighLevel to IntakeQ Integration Tests")
    print("===============================================")
    
    # Test IntakeQ API connection
    print("\n1. Testing IntakeQ API Connection")
    if test_intakeq_api():
        print("✅ IntakeQ API connection successful")
    else:
        print("❌ IntakeQ API connection failed")
        print("Please check your API key and try again")
        return
    
    # Simulate webhook event
    print("\n2. Simulating GoHighLevel Webhook Event")
    try:
        result = simulate_webhook_event()
        if result.get("status") == "success":
            print("✅ Webhook processing successful")
            print(f"GoHighLevel Contact ID: {result.get('gohighlevel_contact_id')}")
            print(f"IntakeQ Client ID: {result.get('intakeq_client_id')}")
        else:
            print("❌ Webhook processing failed")
            print(f"Reason: {result.get('reason')}")
    except Exception as e:
        print(f"❌ Error during webhook simulation: {str(e)}")
    
    print("\nTest Summary")
    print("===========")
    print("Check the logs/test.log file for detailed test results")

if __name__ == "__main__":
    main()
