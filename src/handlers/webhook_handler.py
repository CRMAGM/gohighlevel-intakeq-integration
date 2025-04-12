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
    tags = data.get("tags", "").split(",")
    if "paid" not in [tag.strip().lower() for tag in tags]:
        logging.info("Ignoring: 'paid' tag not found")
        return {"status": "ignored", "reason": "Not a paid tag"}
    
    # Get contact data directly from the webhook payload
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
            "intakeq_client_id": result.get("id"),
            "glp1_fields_mapped": len(glp1_fields) if glp1_fields else 0
        }
    except Exception as e:
        logging.error(f"Error creating client in IntakeQ: {str(e)}")
        return {
            "status": "error",
            "reason": f"Failed to create client in IntakeQ: {str(e)}"
        }
