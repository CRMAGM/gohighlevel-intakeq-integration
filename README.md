# GoHighLevel to IntakeQ Integration

This application integrates GoHighLevel with IntakeQ, automatically creating customers in IntakeQ when contacts in GoHighLevel are tagged with "paid".

## Features

- Webhook listener for GoHighLevel tag events
- Automatic customer creation in IntakeQ
- Custom field mapping between platforms
- Location and Treatment tag transfer
- Error handling and logging

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API credentials
4. Configure field mappings in `config/config.json`
5. Run the application:
   ```
   python main.py
   ```

## Configuration

### Environment Variables

- `INTAKEQ_API_KEY`: Your IntakeQ API key
- `GHL_CLIENT_ID`: GoHighLevel OAuth client ID
- `GHL_CLIENT_SECRET`: GoHighLevel OAuth client secret
- `GHL_REDIRECT_URI`: OAuth redirect URI
- `DEBUG`: Enable debug mode (True/False)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)

### Field Mapping

Field mappings are configured in `config/config.json`. You can customize how fields are mapped between GoHighLevel and IntakeQ.

## Webhook Setup

1. In GoHighLevel, go to Settings > Integrations > Webhooks
2. Add a new webhook with the URL: `https://your-server.com/webhook/gohighlevel`
3. Select the "Contact Tag Added" event

## Usage

Once set up, the integration will automatically:
1. Listen for the "paid" tag being added to contacts in GoHighLevel
2. Retrieve the contact's full details from GoHighLevel
3. Create a new client in IntakeQ with mapped data
4. Add Location and Treatment tags based on GoHighLevel custom fields

## Development

### Project Structure

- `main.py`: Application entry point
- `src/api/`: API clients for GoHighLevel and IntakeQ
- `src/handlers/`: Webhook event handlers
- `src/models/`: Data models
- `src/utils/`: Utility functions
- `config/`: Configuration files
- `tests/`: Test cases
- `logs/`: Application logs

### Running Tests

```
pytest tests/
```

## Troubleshooting

Check the logs in the `logs/` directory for detailed error information.

Common issues:
- Invalid API credentials
- Webhook configuration errors
- Missing required fields

## License

This project is licensed under the MIT License - see the LICENSE file for details.
