from flask import Flask, request, jsonify
from src.config.settings import settings
from src.bot.bot_core import WhatsAppBot
from src.services.twilio_service import TwilioService
import logging
from colorlog import ColoredFormatter

# Configure logging
log_format = '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(getattr(logging, settings.log_level))

# Initialize services
app = Flask(__name__)
bot = WhatsAppBot(name=settings.bot_name)
twilio_service = TwilioService()


@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages."""
    try:
        # Get incoming message
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        logger.info(f"Received message from {sender}: {incoming_msg}")
        
        # Process message with bot
        response_text = bot.process_message(incoming_msg, sender)
        
        logger.info(f"Sending response: {response_text}")
        
        # Create TwiML response
        return twilio_service.create_messaging_response(response_text)
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        error_response = "¡Uy! Algo salió mal. Dame un momento y vuelvo."
        return twilio_service.create_messaging_response(error_response)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'bot': bot.get_bot_info(),
        'service': 'whatsapp-bot-colombiano'
    }), 200


@app.route('/', methods=['GET'])
def home():
    """Home endpoint."""
    return jsonify({
        'message': '¡Hola! Soy Deep, tu bot colombiano.',
        'endpoints': {
            'webhook': '/webhook (POST)',
            'health': '/health (GET)'
        },
        'instructions': 'Configure your Twilio webhook to point to /webhook'
    }), 200


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=(settings.flask_env == 'development')
    )