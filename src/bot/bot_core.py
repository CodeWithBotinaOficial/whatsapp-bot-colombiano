from typing import Dict, Optional
from .personality import ColombianPersonality
from .response_handler import ResponseHandler
from datetime import datetime


class WhatsAppBot:
    """Main bot class following Single Responsibility Principle."""
    
    def __init__(self, name: str = "Deep", personality: str = "colombian"):
        self.name = name
        self.personality = ColombianPersonality(name=name)
        self.response_handler = ResponseHandler(self.personality)
        self.conversation_context: Dict[str, any] = {}
    
    def process_message(self, message: str, sender: str) -> str:
        """
        Process incoming message and generate response.
        
        Args:
            message: The message text from user
            sender: The sender's phone number
            
        Returns:
            Formatted response message
        """
        # Clean and prepare message
        cleaned_message = message.strip()
        
        # Update conversation context
        self._update_context(sender, cleaned_message)
        
        # Get response from handler
        response = self.response_handler.handle_message(cleaned_message)
        
        return response
    
    def _update_context(self, sender: str, message: str) -> None:
        """Update conversation context for the sender."""
        if sender not in self.conversation_context:
            self.conversation_context[sender] = {
                'message_count': 0,
                'last_message': '',
                'interaction_time': None
            }
        
        self.conversation_context[sender]['message_count'] += 1
        self.conversation_context[sender]['last_message'] = message
        self.conversation_context[sender]['interaction_time'] = datetime.now()
    
    def get_bot_info(self) -> Dict[str, str]:
        """Get information about the bot."""
        return {
            'name': self.name,
            'personality': 'colombian',
            'description': 'Bot con personalidad colombiana chévere',
            'version': '1.0.0'
        }