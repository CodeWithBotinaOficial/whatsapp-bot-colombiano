from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from typing import Optional
from src.config.settings import settings


class TwilioService:
    """Service for handling Twilio communications."""
    
    def __init__(self):
        self.client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token
        )
        self.whatsapp_number = settings.twilio_whatsapp_number
    
    def validate_request(self, request_signature: str, url: str, params: dict) -> bool:
        """
        Validate Twilio request signature.
        
        Args:
            request_signature: Signature from Twilio headers
            url: The full URL of the request
            params: POST parameters
            
        Returns:
            Boolean indicating if request is valid
        """
        # In production, implement proper validation
        return True  # For development purposes
    
    def create_messaging_response(self, body: str) -> str:
        """
        Create TwiML response for WhatsApp.
        
        Args:
            body: Response text message
            
        Returns:
            TwiML string
        """
        response = MessagingResponse()
        response.message(body=body)
        return str(response)
    
    def send_message(self, to: str, body: str) -> Optional[str]:
        """
        Send WhatsApp message via Twilio.
        
        Args:
            to: Recipient WhatsApp number (format: whatsapp:+1234567890)
            body: Message content
            
        Returns:
            Message SID if successful, None otherwise
        """
        try:
            message = self.client.messages.create(
                from_=self.whatsapp_number,
                body=body,
                to=to
            )
            return message.sid
        except Exception as e:
            print(f"Error sending message: {e}")
            return None