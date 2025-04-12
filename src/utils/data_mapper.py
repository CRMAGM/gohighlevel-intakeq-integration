"""
Utility functions for mapping data between GoHighLevel and IntakeQ.
"""

import logging

def map_contact_to_client(contact, field_mapping):
    """
    Map a GoHighLevel contact to an IntakeQ client.
    Only includes non-empty fields and doesn't overwrite existing data.
    
    Args:
        contact (dict): The GoHighLevel contact
        field_mapping (dict): The field mapping configuration
        
    Returns:
        dict: The IntakeQ client data
    """
    logging.info(f"Mapping contact {contact.get('id')} to IntakeQ client")
    
    # Initialize client data with only required fields
    # Handle both camelCase (webhook) and snake_case (direct) formats
    first_name = contact.get("firstName") or contact.get("first_name") or ""
    last_name = contact.get("lastName") or contact.get("last_name") or ""
    full_name = f"{first_name} {last_name}".strip()
    
    # Start with minimal required fields
    client_data = {
        "FirstName": first_name,
        "LastName": last_name,
        "Name": full_name,
        "Email": (contact.get("email") or contact.get("Email") or "").strip(),
        "Phone": (contact.get("phone") or contact.get("Phone") or "").strip(),
        "City": (contact.get("city") or contact.get("City") or "").strip(),
        "StateShort": (contact.get("state") or contact.get("State") or "").strip(),
        "PostalCode": (contact.get("postalCode") or contact.get("postal_code") or "").strip(),
        "Country": (contact.get("country") or contact.get("Country") or "USA").strip(),
        "CustomFields": []
    }
    
    # Map specific fields we care about with their IntakeQ field IDs
    field_mappings = {
        "Height Feet": {"FieldId": "sotc", "Value": None},
        "Height Inches": {"FieldId": "o0a0", "Value": None},
        "BMI": {"FieldId": "gcf3", "Value": None},
        "Current Weight?": {"FieldId": "n0dx", "Value": None},
        "Target Weight": {"FieldId": "fovf", "Value": None}
    }
    
    # Extract values from custom fields
    height_feet = None
    height_inches = None
    weight = None
    
    for custom_field in contact.get("customFields", []):
        field_key = custom_field.get("key")
        field_value = custom_field.get("field_value")
        
        # Store height and weight values for BMI calculation
        if field_key == "Height Feet":
            height_feet = float(field_value) if field_value else None
        elif field_key == "Height Inches":
            height_inches = float(field_value) if field_value else None
        elif field_key == "Current Weight?":
            weight = float(field_value) if field_value else None
            
        # Update field mappings
        if field_key in field_mappings:
            field_mappings[field_key]["Value"] = field_value
    
    # Calculate BMI if we have both height and weight
    if height_feet is not None and height_inches is not None and weight is not None:
        # Convert height to inches
        total_inches = (height_feet * 12) + height_inches
        # BMI formula: (weight in pounds * 703) / (height in inches)²
        bmi = round((weight * 703) / (total_inches * total_inches), 1)
        field_mappings["BMI"]["Value"] = str(bmi)
        logging.info(f"Calculated BMI: {bmi}")
    
    # Add any non-empty custom fields to the request
    for field_name, field_data in field_mappings.items():
        if field_data["Value"]:
            client_data["CustomFields"].append({
                "FieldId": field_data["FieldId"],
                "Value": str(field_data["Value"])
            })
    
    # Map location data
    if "location" in contact:
        location = contact["location"]
        if location:
            client_data["City"] = location.get("city", "").strip()
            client_data["StateShort"] = location.get("state", "").strip()
            client_data["PostalCode"] = location.get("postalCode", "").strip()
            client_data["Country"] = location.get("country", "USA").strip()
    
    # Remove any empty values
    client_data = {k: v for k, v in client_data.items() if v}
    
    logging.debug(f"Mapped client data: {client_data}")
    return client_data
