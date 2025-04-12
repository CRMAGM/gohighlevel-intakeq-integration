# GoHighLevel to IntakeQ Integration
## User Guide and Documentation

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Webhook Setup](#webhook-setup)
8. [Custom Field Mapping](#custom-field-mapping)
9. [GLP-1 Intake Form Integration](#glp-1-intake-form-integration)
10. [Troubleshooting](#troubleshooting)
11. [Support](#support)

## Overview

This integration connects GoHighLevel with IntakeQ, allowing you to automatically create clients in IntakeQ when contacts in GoHighLevel are tagged with "paid". The integration transfers contact information, adds Location and Treatment tags, and populates the "GLP-1 Intake Questions Medical History" form with data from GoHighLevel custom fields.

## Features

- **Automated Client Creation**: Automatically creates clients in IntakeQ when contacts in GoHighLevel receive the "paid" tag
- **Tag Transfer**: Transfers Location and Treatment information as tags in IntakeQ
- **Custom Field Mapping**: Maps GoHighLevel custom fields to IntakeQ client fields
- **GLP-1 Form Integration**: Populates the "GLP-1 Intake Questions Medical History" form with data from GoHighLevel
- **Comprehensive Logging**: Detailed logging for troubleshooting and monitoring
- **Error Handling**: Robust error handling to ensure reliable operation

## Requirements

- GoHighLevel account with API access
- IntakeQ account with API access
- Python 3.6 or higher
- Web server with public internet access for webhook endpoint

## Installation

1. Clone the repository to your server:
   ```
   git clone https://github.com/yourusername/gohighlevel-intakeq-integration.git
   cd gohighlevel-intakeq-integration
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy the example environment file and edit it with your API credentials:
   ```
   cp .env.example .env
   nano .env
   ```

## Configuration

### Environment Variables

Edit the `.env` file with your API credentials and settings:

```
# API Credentials
INTAKEQ_API_KEY=your_intakeq_api_key

# GoHighLevel OAuth (to be filled)
GHL_CLIENT_ID=your_ghl_client_id
GHL_CLIENT_SECRET=your_ghl_client_secret
GHL_REDIRECT_URI=your_redirect_uri

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
WEBHOOK_SECRET=your_webhook_secret

# Server Settings
HOST=0.0.0.0
PORT=5000
```

### Field Mapping Configuration

The field mapping between GoHighLevel and IntakeQ is configured in `config/config.json`. You can customize this mapping to suit your specific needs:

```json
{
  "app": {
    "name": "GoHighLevel to IntakeQ Integration",
    "version": "0.1.0"
  },
  "field_mapping": {
    "gohighlevel_to_intakeq": {
      "firstName": "firstName",
      "lastName": "lastName",
      "email": "email",
      "phone": "phone",
      "address1": "address",
      "city": "city",
      "state": "state",
      "postalCode": "zipCode"
    },
    "custom_fields": {
      "location": "location_tag",
      "treatment": "treatment_tag"
    }
  },
  "webhook": {
    "events": ["contact.tag.added"]
  },
  "retry": {
    "max_attempts": 3,
    "backoff_factor": 2
  }
}
```

## Usage

1. Start the integration server:
   ```
   python main.py
   ```

2. The server will start listening for webhook events from GoHighLevel.

3. When a contact in GoHighLevel is tagged with "paid", the integration will:
   - Retrieve the contact's full details from GoHighLevel
   - Create a new client in IntakeQ with the mapped data
   - Add Location and Treatment tags to the client in IntakeQ
   - Populate the "GLP-1 Intake Questions Medical History" form with data from GoHighLevel custom fields

## Webhook Setup

To set up the webhook in GoHighLevel:

1. Log in to your GoHighLevel account
2. Go to Settings > Integrations > Webhooks
3. Click "Add Webhook"
4. Enter the following details:
   - Name: IntakeQ Integration
   - URL: `https://your-server.com/webhook/gohighlevel`
   - Event: Contact Tag Added
5. Click "Save"

Make sure your server is accessible from the internet and the URL is correctly configured.

## Custom Field Mapping

The integration maps the following custom fields from GoHighLevel to IntakeQ:

- Basic contact information (name, email, phone, etc.)
- Location and Treatment as tags
- Additional fields for the GLP-1 Intake form

You can customize the field mapping in the `config/config.json` file to match your specific field names and requirements.

## GLP-1 Intake Form Integration

The integration specifically supports populating the "GLP-1 Intake Questions Medical History" form in IntakeQ with data from GoHighLevel custom fields. The following fields are mapped:

- check_all_that_apply_in_the_past_2_weeks_other
- if_yes_which_glp1_medication
- have_you_ever_been_diagnosed_with_any_of_the_following_conditions
- check_all_that_apply_in_the_past_2_weeks_gi__gu
- upload_a_picture_of_your_id_drivers_license__for_weight_loss_glp_upload_a_full_body_img
- upload_a_picture_of_your_id_drivers_license__for_weight_loss_glp_upload_a_full_body_image
- target_weight
- what_diets_or_programs_have_you_tried_in_the_past
- have_you_had_success_with_any_previous_weight_loss_programs_or_medications
- are_you_currently_tracking_your_food_or_calorie_intake
- check_all_that_apply_in_the_past_2_weeks
- current_weight
- check_all_that_apply_in_the_past_2_weeks_cont
- any_major_health_issues_in_your_immediate_family_parentssiblings
- social_history
- list_any_prescription_otc_or_supplements_you_take_regularly
- any_past_surgeries
- any_medication_allergies
- what_brings_you_here_today
- have_you_ever_been_diagnosed_with_any_of_the_following_conditions_below

To ensure these fields are correctly mapped, make sure the custom field names in GoHighLevel match the keys listed above.

## Troubleshooting

### Common Issues

1. **Webhook not receiving events**
   - Verify the webhook URL is correctly configured in GoHighLevel
   - Check that your server is accessible from the internet
   - Ensure the webhook endpoint is properly set up in the integration

2. **Client not being created in IntakeQ**
   - Check the IntakeQ API key is correct
   - Verify the "paid" tag is being added to contacts in GoHighLevel
   - Check the logs for any error messages

3. **Custom fields not being populated**
   - Ensure the custom field names in GoHighLevel match the expected keys
   - Check that the form name in IntakeQ matches "GLP-1 Intake Questions Medical History"
   - Verify the custom field values are being correctly set in GoHighLevel

### Logs

The integration logs all activity to the `logs/app.log` file. Check this file for detailed information about any issues:

```
tail -f logs/app.log
```

## Support

For support with this integration, please contact:

- Email: support@yourdomain.com
- Phone: (123) 456-7890

When reporting issues, please include:
- A description of the problem
- Any error messages from the logs
- Steps to reproduce the issue
