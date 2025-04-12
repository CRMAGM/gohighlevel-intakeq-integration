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
    logging.info(f"Mapping contact {contact['id']} to IntakeQ client")
    
    # Initialize client data with only required fields
    first_name = contact.get("firstName", "")
    last_name = contact.get("lastName", "")
    full_name = f"{first_name} {last_name}".strip()
    
    # Start with minimal required fields
    client_data = {
        "firstName": first_name,
        "lastName": last_name,
        "name": full_name,
    }
    
    # Only add non-empty fields from standard mapping
    for ghl_field, intakeq_field in field_mapping["gohighlevel_to_intakeq"].items():
        value = contact.get(ghl_field, "")
        if value:  # Only add if value is not empty
            client_data[intakeq_field] = value
    
    # Extract additional fields from custom fields, only if they have values
    custom_fields_data = {}
    for custom_field in contact.get("customFields", []):
        field_key = custom_field.get("key", "")
        field_value = custom_field.get("field_value", "")
        
        # Only add fields that have values
        if field_value:
            if field_key == "date_of_birth":
                client_data["dateOfBirth"] = field_value
            elif field_key == "marital_status":
                client_data["maritalStatus"] = field_value
            elif field_key == "home_phone":
                client_data["homePhone"] = field_value
            elif field_key == "work_phone":
                client_data["workPhone"] = field_value
            elif field_key == "apt_unit":
                client_data["aptUnit"] = field_value
            elif field_key == "referring_provider":
                client_data["referringProvider"] = field_value
            elif field_key == "emergency_contact_name":
                client_data["emergencyContactName"] = field_value
            elif field_key == "emergency_contact_phone":
                client_data["emergencyContactPhone"] = field_value
            elif field_key == "emergency_contact_relationship":
                client_data["emergencyContactRelationship"] = field_value
            elif field_key == "height_feet":
                custom_fields_data["heightFeet"] = field_value
            elif field_key == "height_inches":
                custom_fields_data["heightInches"] = field_value
            elif field_key == "bmi":
                custom_fields_data["bmi"] = field_value
            elif field_key == "referral_source":
                custom_fields_data["referralSource"] = field_value
            elif field_key == "body_mass_reduction_percentage":
                custom_fields_data["bodyMassReductionPercentage"] = field_value
            elif field_key == "current_weight_loss_medication":
                custom_fields_data["currentWeightLossMedication"] = field_value
            elif field_key == "tracking":
                custom_fields_data["tracking"] = field_value
            
            # Store all custom fields with values
            custom_fields_data[field_key] = field_value
    
    # Add custom fields to client data if there are any
    if custom_fields_data:
        client_data["customFields"] = custom_fields_data
    
    # Extract location and treatment from custom fields for tags
    tags = []
    custom_field_mapping = field_mapping["custom_fields"]
    
    for custom_field in contact.get("customFields", []):
        field_key = custom_field.get("key")
        field_value = custom_field.get("field_value", "")
        
        if field_key in custom_field_mapping and field_value:
            # Only add non-empty tag values
            tags.append(field_value)
    
    # Add tags to client data if there are any
    if tags:
        client_data["tags"] = tags
    
    return client_data
