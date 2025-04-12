"""
Specialized mapping for GLP-1 Intake Questions Medical History form fields.
This module handles the mapping between GoHighLevel custom fields and 
IntakeQ form questions for the GLP-1 intake process.
"""

import logging

# Define the mapping between GoHighLevel custom fields and IntakeQ form fields
GLP1_FIELD_MAPPING = {
    # GoHighLevel custom field key : IntakeQ form field ID/key
    "check_all_that_apply_in_the_past_2_weeks_other": "check_all_that_apply_in_the_past_2_weeks_other",
    "if_yes_which_glp1_medication": "if_yes_which_glp1_medication",
    "have_you_ever_been_diagnosed_with_any_of_the_following_conditions": "have_you_ever_been_diagnosed_with_any_of_the_following_conditions",
    "check_all_that_apply_in_the_past_2_weeks_gi__gu": "check_all_that_apply_in_the_past_2_weeks_gi__gu",
    "upload_a_picture_of_your_id_drivers_license__for_weight_loss_glp_upload_a_full_body_img": "upload_a_picture_of_your_id_drivers_license__for_weight_loss_glp_upload_a_full_body_img",
    "upload_a_picture_of_your_id_drivers_license__for_weight_loss_glp_upload_a_full_body_image": "upload_a_picture_of_your_id_drivers_license__for_weight_loss_glp_upload_a_full_body_image",
    "target_weight": "target_weight",
    "what_diets_or_programs_have_you_tried_in_the_past": "what_diets_or_programs_have_you_tried_in_the_past",
    "have_you_had_success_with_any_previous_weight_loss_programs_or_medications": "have_you_had_success_with_any_previous_weight_loss_programs_or_medications",
    "are_you_currently_tracking_your_food_or_calorie_intake": "are_you_currently_tracking_your_food_or_calorie_intake",
    "check_all_that_apply_in_the_past_2_weeks": "check_all_that_apply_in_the_past_2_weeks",
    "current_weight": "current_weight",
    "check_all_that_apply_in_the_past_2_weeks_cont": "check_all_that_apply_in_the_past_2_weeks_cont",
    "any_major_health_issues_in_your_immediate_family_parentssiblings": "any_major_health_issues_in_your_immediate_family_parentssiblings",
    "social_history": "social_history",
    "list_any_prescription_otc_or_supplements_you_take_regularly": "list_any_prescription_otc_or_supplements_you_take_regularly",
    "any_past_surgeries": "any_past_surgeries",
    "any_medication_allergies": "any_medication_allergies",
    "what_brings_you_here_today": "what_brings_you_here_today",
    "have_you_ever_been_diagnosed_with_any_of_the_following_conditions_below": "have_you_ever_been_diagnosed_with_any_of_the_following_conditions_below"
}

# The name of the IntakeQ form to populate
GLP1_FORM_NAME = "GLP-1 Intake Questions Medical History"

def extract_glp1_custom_fields(contact):
    """
    Extract GLP-1 related custom fields from a GoHighLevel contact.
    
    Args:
        contact (dict): The GoHighLevel contact data
        
    Returns:
        dict: Extracted GLP-1 custom fields
    """
    glp1_fields = {}
    
    # Extract custom fields from the contact
    for custom_field in contact.get("customFields", []):
        field_key = custom_field.get("key", "")
        
        # Check if this is a GLP-1 related field
        if field_key in GLP1_FIELD_MAPPING:
            glp1_fields[field_key] = custom_field.get("field_value", "")
            logging.info(f"Extracted GLP-1 field: {field_key} = {glp1_fields[field_key]}")
    
    return glp1_fields

def map_glp1_fields_to_intakeq_form(glp1_fields):
    """
    Map GLP-1 custom fields to IntakeQ form fields.
    
    Args:
        glp1_fields (dict): The extracted GLP-1 custom fields
        
    Returns:
        dict: Mapped IntakeQ form fields
    """
    intakeq_form_fields = {
        "formName": GLP1_FORM_NAME,
        "fields": []
    }
    
    # Map each field to the IntakeQ format
    for ghl_field, value in glp1_fields.items():
        if ghl_field in GLP1_FIELD_MAPPING:
            intakeq_field = {
                "id": GLP1_FIELD_MAPPING[ghl_field],
                "value": value
            }
            intakeq_form_fields["fields"].append(intakeq_field)
    
    return intakeq_form_fields
