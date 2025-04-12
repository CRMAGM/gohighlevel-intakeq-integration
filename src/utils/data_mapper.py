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
        "Target Weight": {"FieldId": "fovf", "Value": None},
        "Current Weight Loss Medication": {"FieldId": "9dmc", "Value": None},
        "Dose": {"FieldId": "vr53", "Value": None},
        "State": {"FieldId": "i5ju", "Value": None},
        "Tracking": {"FieldId": "ku5d", "Value": None},
        "State?": {"FieldId": "8fjy", "Value": None},
        
        "Weight Loss Goal?": {"FieldId": "weight_loss_goal", "Value": None},
        "Goal?": {"FieldId": "goal", "Value": None},
        "By When would you like to acheive this result?": {"FieldId": "goal_timeline", "Value": None},
        "If you qualify how soon would you like to get started?": {"FieldId": "start_timeline", "Value": None},
        "Have you been diagnosed with any of the following conditions?": {"FieldId": "medical_conditions", "Value": None},
        "Are you currently taking any PRESCRIPTION medications for weight loss?": {"FieldId": "current_prescriptions", "Value": None},
        "Please enter the details of any allergies": {"FieldId": "allergies", "Value": None},
        "Have you ever been diagnosed with any of the following conditions below?": {"FieldId": "medical_history", "Value": None},
        "What brings you here today?": {"FieldId": "reason_for_visit", "Value": None},
        "Any past surgeries?": {"FieldId": "past_surgeries", "Value": None},
        "Social History": {"FieldId": "social_history", "Value": None},
        "Any major health issues in your immediate family (parents/siblings)?": {"FieldId": "family_history", "Value": None},
        "List any prescription, OTC, or supplements you take regularly.": {"FieldId": "current_medications", "Value": None},
        "Any medication allergies?": {"FieldId": "medication_allergies", "Value": None},
        "What diets or programs have you tried in the past?": {"FieldId": "past_diets", "Value": None},
        "Have you had success with any previous weight loss programs or medications?": {"FieldId": "past_success", "Value": None},
        "Are you currently tracking your food or calorie intake?": {"FieldId": "tracking_food", "Value": None}
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
