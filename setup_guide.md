# Installation and Setup Guide

## Prerequisites
- Python 3.6 or higher
- Access to GoHighLevel and IntakeQ accounts
- API credentials for both platforms

## Step 1: Clone the Repository
If you're using Git:
```bash
git clone https://github.com/yourusername/gohighlevel-intakeq-integration.git
cd gohighlevel-intakeq-integration
```

Alternatively, you can download and extract the ZIP file containing the integration code.

## Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 3: Configure Environment Variables
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your API credentials:
   ```
   # IntakeQ API Key
   INTAKEQ_API_KEY=606a35d920b18518a35aa2248a4220bbcc079014
   
   # GoHighLevel OAuth (to be filled)
   GHL_CLIENT_ID=your_client_id
   GHL_CLIENT_SECRET=your_client_secret
   GHL_REDIRECT_URI=your_redirect_uri
   
   # Application Settings
   DEBUG=True
   LOG_LEVEL=INFO
   
   # Server Settings
   HOST=0.0.0.0
   PORT=5000
   ```

## Step 4: Configure Field Mapping
Review and modify the `config/config.json` file to ensure the field mapping matches your specific needs:

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
  }
}
```

## Step 5: Start the Integration Server
```bash
python main.py
```

## Step 6: Set Up GoHighLevel Webhook
1. Log in to your GoHighLevel account
2. Navigate to Settings > Integrations > Webhooks
3. Click "Add Webhook"
4. Configure the webhook:
   - Name: IntakeQ Integration
   - URL: `https://your-server.com/webhook/gohighlevel`
   - Event: Contact Tag Added
5. Save the webhook configuration

## Step 7: Test the Integration
1. Add the "paid" tag to a contact in GoHighLevel
2. Check the logs to verify the webhook was received and processed
3. Verify that a new client was created in IntakeQ with the correct information
4. Confirm that the GLP-1 Intake form was populated with the custom field data

## Step 8: Monitor and Maintain
- Regularly check the logs in the `logs/` directory
- Update the integration as needed when APIs change
- Back up your configuration files before making changes

## Troubleshooting
If you encounter issues:
1. Check the logs in `logs/app.log`
2. Verify your API credentials are correct
3. Ensure your server is accessible from the internet
4. Confirm the webhook URL is correctly configured in GoHighLevel
