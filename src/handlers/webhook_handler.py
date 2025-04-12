"""
Handler for processing webhooks from GoHighLevel.
"""

import logging
import json
import os
from dotenv import load_dotenv
from src.api.gohighlevel_client import GoHighLevelClient
from src.api.intakeq_client import IntakeQClient
from src.utils.data_mapper import map_contact_to_client
from src.utils.glp1_field_mapping import extract_glp1_custom_fields, map_glp1_fields_to_intakeq_form

def process_webhook(data):
    """
    Process a webhook from GoHighLevel.
    Only processes contacts with the 'paid' tag and ignores empty fields.
    
    Args:
        data (dict): The webhook payload
        
    Returns:
        dict: The result of processing the webhook
    """
    logging.info("Processing webhook")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("INTAKEQ_API_KEY")
    if not api_key:
        logging.error("IntakeQ API Key not found")
        return {"status": "error", "reason": "IntakeQ API Key not found"}
    logging.info("IntakeQ API Key found: " + api_key[:4] + "...")
    
    # Load configuration
    with open("config/config.json", "r") as f:
        config = json.load(f)
    
    # Check if this is a contact with the 'paid' tag
    # First check if the tag is in the payload.tagName field (webhook format)
    if "payload" in data and "tagName" in data["payload"] and data["payload"]["tagName"].lower() == "paid":
        logging.info("Found 'paid' tag in payload.tagName")
        is_paid = True
    # Then check if the tag is in the tags field (direct contact format)
    elif "tags" in data:
        tags = data.get("tags", "").split(",")
        is_paid = "paid" in [tag.strip().lower() for tag in tags]
        if is_paid:
            logging.info("Found 'paid' tag in tags field")
    else:
        is_paid = False
    
    if not is_paid:
        logging.info("Ignoring: 'paid' tag not found")
        return {"status": "ignored", "reason": "Not a paid tag"}
    
    # Get contact data from the appropriate location in the payload
    if "payload" in data:
        # Webhook format
        payload = data["payload"]
        contact = {
            "id": payload.get("contactId"),
            "firstName": payload.get("firstName"),
            "lastName": payload.get("lastName"),
            "email": payload.get("email"),
            "phone": payload.get("phone"),
            "city": payload.get("city"),
            "state": payload.get("state"),
            "country": payload.get("country", "USA"),
            "postalCode": payload.get("postalCode"),
            "customFields": []
        }
        
        # Add custom fields from the payload
        if "customFields" in payload:
            for field in payload["customFields"]:
                field_key = field.get("key", "")
                field_value = field.get("field_value")
                
                # Map specific fields we care about
                if field_key == "Height Feet":
                    contact["Height Feet"] = field_value
                elif field_key == "Height Inches":
                    contact["Height Inches"] = field_value
                elif field_key == "BMI":
                    contact["BMI"] = field_value
                elif field_key == "Current Weight?":
                    contact["Current Weight?"] = field_value
                elif field_key == "Target Weight":
                    contact["Target Weight"] = field_value
                
                # Still add to customFields for general processing
                contact["customFields"].append({
                    "key": field_key,
                    "field_value": str(field_value) if field_value is not None else ""
                })
    else:
        # Direct contact format
        contact = {
            "id": data.get("contact_id"),
            "firstName": data.get("first_name"),
            "lastName": data.get("last_name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "city": data.get("city"),
            "state": data.get("state"),
            "country": data.get("country"),
            "postalCode": data.get("postal_code"),
            "customFields": []
        }
        
        # Add all form fields as custom fields
        for key, value in data.items():
            if key not in ["contact_id", "first_name", "last_name", "email", "phone", "tags", "city", "state", "country", "postal_code"]:
                contact["customFields"].append({
                    "key": key,
                    "field_value": str(value) if value is not None else ""
                })
    
    # Initialize clients
    intakeq_client = IntakeQClient(api_key=api_key)
    
    # Map GoHighLevel contact to IntakeQ client
    client_data = map_contact_to_client(contact, config["field_mapping"])
    
    # Extract and map GLP-1 custom fields
    glp1_fields = extract_glp1_custom_fields(contact)
    if glp1_fields:
        # Filter out empty fields
        glp1_fields = {k: v for k, v in glp1_fields.items() if v}
        if glp1_fields:
            logging.info(f"Found {len(glp1_fields)} GLP-1 custom fields with values")
            form_data = map_glp1_fields_to_intakeq_form(glp1_fields)
            client_data["form_data"] = form_data
        else:
            logging.info("No GLP-1 custom fields with values found")
    else:
        logging.info("No GLP-1 custom fields found")
    
    logging.info(f"Raw client data: {client_data}")
    
    # Create client in IntakeQ
    try:
        result = intakeq_client.create_client(client_data)
        return {
            "status": "success",
            "gohighlevel_contact_id": contact["id"],
            "intakeq_client_id": result.get("ClientId") if result else None,
            "glp1_fields_mapped": len(glp1_fields) if glp1_fields else 0
        }
    except Exception as e:
        logging.error(f"Error creating client in IntakeQ: {str(e)}")
        return {
            "status": "error",
            "reason": f"Failed to create client in IntakeQ: {str(e)}"
        }
