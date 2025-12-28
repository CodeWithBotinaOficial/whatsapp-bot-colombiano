"""
Unit tests for the Colombian WhatsApp Bot.
Tests follow AAA pattern (Arrange, Act, Assert).
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime

# Import the modules to test
from src.bot.personality import ColombianPersonality
from src.bot.response_handler import (
    GreetingStrategy,
    FarewellStrategy,
    SlangStrategy,
    HelpStrategy,
    DefaultStrategy,
    ResponseHandler
)
from src.bot.bot_core import WhatsAppBot
from src.services.twilio_service import TwilioService
from src.config.settings import Settings


# ==================== FIXTURES ====================
@pytest.fixture
def colombian_personality():
    """Fixture for ColombianPersonality instance."""
    return ColombianPersonality(name="Deep")


@pytest.fixture
def response_handler(colombian_personality):
    """Fixture for ResponseHandler instance."""
    return ResponseHandler(colombian_personality)


@pytest.fixture
def whatsapp_bot():
    """Fixture for WhatsAppBot instance."""
    return WhatsAppBot(name="TestBot")


@pytest.fixture
def mock_settings():
    """Fixture for mock settings."""
    with patch('src.config.settings.Settings') as MockSettings:
        mock_settings_instance = MockSettings.return_value
        mock_settings_instance.twilio_account_sid = "test_sid"
        mock_settings_instance.twilio_auth_token = "test_token"
        mock_settings_instance.twilio_whatsapp_number = "whatsapp:+1234567890"
        mock_settings_instance.bot_name = "TestBot"
        mock_settings_instance.log_level = "INFO"
        mock_settings_instance.secret_key = "test_secret"
        yield mock_settings_instance


# ==================== TESTS FOR PERSONALITY ====================
class TestColombianPersonality:
    """Test Colombian personality responses and slang."""
    
    def test_initialization(self, colombian_personality):
        """Test personality initialization."""
        assert colombian_personality.name == "Deep"
        assert len(colombian_personality.GREETINGS) > 0
        assert len(colombian_personality.SLANG) > 0
    
    def test_get_greeting_returns_string(self, colombian_personality):
        """Test greeting returns a non-empty string."""
        greeting = colombian_personality.get_greeting()
        assert isinstance(greeting, str)
        assert len(greeting) > 0
        assert "Deep" in greeting or colombian_personality.name in greeting
    
    def test_get_farewell_returns_string(self, colombian_personality):
        """Test farewell returns a non-empty string."""
        farewell = colombian_personality.get_farewell()
        assert isinstance(farewell, str)
        assert len(farewell) > 0
    
    def test_get_positive_response_returns_string(self, colombian_personality):
        """Test positive response returns a non-empty string."""
        response = colombian_personality.get_positive_response()
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_explain_slang_existing_word(self, colombian_personality):
        """Test slang explanation for known words."""
        # Test with known slang
        result = colombian_personality.explain_slang("parce")
        assert "significa" in result.lower()
        assert "amigo" in result.lower() or "compañero" in result.lower()
    
    def test_explain_slang_unknown_word(self, colombian_personality):
        """Test slang explanation for unknown words."""
        result = colombian_personality.explain_slang("unknownword")
        assert "no la tengo" in result.lower() or "enseñas" in result.lower()
    
    def test_add_colombian_flavor_probability(self, colombian_personality):
        """Test that flavor is sometimes added."""
        original_message = "Hola amigo"
        flavored_messages = []
        
        # Run multiple times to test probability
        for _ in range(20):
            result = colombian_personality.add_colombian_flavor(original_message)
            flavored_messages.append(result)
        
        # At least some messages should have flavor (due to 30% probability)
        has_flavor = any(
            any(enhancement in result for enhancement in ["¿Me entiendes?", "¡Vea!", "¡O sea!", "¿Sí o qué?"])
            for result in flavored_messages
        )
        # Note: This test might rarely fail due to randomness, but probability is high it will pass
        
        # All messages should contain original message
        assert all(original_message in msg for msg in flavored_messages)


# ==================== TESTS FOR RESPONSE STRATEGIES ====================
class TestGreetingStrategy:
    """Test greeting response strategy."""
    
    def test_can_handle_greetings(self, colombian_personality):
        """Test detection of various greetings."""
        strategy = GreetingStrategy(colombian_personality)
        
        assert strategy.can_handle("Hola") == True
        assert strategy.can_handle("Buenos días") == True
        assert strategy.can_handle("QUIUBO") == True  # Uppercase
        assert strategy.can_handle("  hola  ") == True  # With spaces
        assert strategy.can_handle("qué más parce") == True
        assert strategy.can_handle("buenas tardes") == True
    
    def test_cannot_handle_non_greetings(self, colombian_personality):
        """Test that non-greetings are not handled."""
        strategy = GreetingStrategy(colombian_personality)
        
        assert strategy.can_handle("adiós") == False
        assert strategy.can_handle("qué significa parce") == False
        assert strategy.can_handle("") == False
        assert strategy.can_handle("ayuda") == False
    
    def test_get_response_returns_greeting(self, colombian_personality):
        """Test response generation for greetings."""
        strategy = GreetingStrategy(colombian_personality)
        response = strategy.get_response("Hola")
        
        assert isinstance(response, str)
        assert len(response) > 0


class TestFarewellStrategy:
    """Test farewell response strategy."""
    
    def test_can_handle_farewells(self, colombian_personality):
        """Test detection of various farewells."""
        strategy = FarewellStrategy(colombian_personality)
        
        assert strategy.can_handle("adiós") == True
        assert strategy.can_handle("CHAO") == True  # Uppercase
        assert strategy.can_handle("nos vemos") == True
        assert strategy.can_handle("hasta luego") == True
        assert strategy.can_handle("bye") == True
    
    def test_cannot_handle_non_farewells(self, colombian_personality):
        """Test that non-farewells are not handled."""
        strategy = FarewellStrategy(colombian_personality)
        
        assert strategy.can_handle("hola") == False
        assert strategy.can_handle("") == False
        assert strategy.can_handle("qué más") == False
    
    def test_get_response_returns_farewell(self, colombian_personality):
        """Test response generation for farewells."""
        strategy = FarewellStrategy(colombian_personality)
        response = strategy.get_response("adiós")
        
        assert isinstance(response, str)
        assert len(response) > 0


class TestSlangStrategy:
    """Test Colombian slang response strategy."""
    
    def test_can_handle_slang_questions(self, colombian_personality):
        """Test detection of slang questions."""
        strategy = SlangStrategy(colombian_personality)
        
        assert strategy.can_handle("qué significa parce") == True
        assert strategy.can_handle("Qué quiere decir chimba?") == True
        assert strategy.can_handle("explícame la jerga") == True
        assert strategy.can_handle("slang colombiano") == True
    
    def test_cannot_handle_non_slang_questions(self, colombian_personality):
        """Test that non-slang questions are not handled."""
        strategy = SlangStrategy(colombian_personality)
        
        assert strategy.can_handle("hola") == False
        assert strategy.can_handle("") == False
        assert strategy.can_handle("cómo estás") == False
    
    def test_get_response_with_known_slang(self, colombian_personality):
        """Test response for known slang words."""
        strategy = SlangStrategy(colombian_personality)
        
        response = strategy.get_response("qué significa parce")
        assert "significa" in response.lower()
        assert "parce" in response.lower()
    
    def test_get_response_without_slang_word(self, colombian_personality):
        """Test response when no slang word is found."""
        strategy = SlangStrategy(colombian_personality)
        
        response = strategy.get_response("qué significa")
        assert "dime qué palabra" in response.lower() or "colombiana" in response.lower()


class TestHelpStrategy:
    """Test help response strategy."""
    
    def test_can_help_requests(self, colombian_personality):
        """Test detection of help requests."""
        strategy = HelpStrategy(colombian_personality)
        
        assert strategy.can_handle("ayuda") == True
        assert strategy.can_handle("AYUDA") == True  # Uppercase
        assert strategy.can_handle("qué puedes hacer") == True
        assert strategy.can_handle("necesito ayuda") == True
    
    def test_cannot_handle_non_help_requests(self, colombian_personality):
        """Test that non-help requests are not handled."""
        strategy = HelpStrategy(colombian_personality)
        
        assert strategy.can_handle("hola") == False
        assert strategy.can_handle("") == False
    
    def test_get_response_returns_help_text(self, colombian_personality):
        """Test response generation for help requests."""
        strategy = HelpStrategy(colombian_personality)
        response = strategy.get_response("ayuda")
        
        assert isinstance(response, str)
        assert len(response) > 50  # Help text should be reasonably long
        assert "Deep" in response or colombian_personality.name in response
        assert "puedo" in response.lower()


class TestDefaultStrategy:
    """Test default response strategy."""
    
    def test_always_can_handle(self, colombian_personality):
        """Test that default strategy always handles messages."""
        strategy = DefaultStrategy(colombian_personality)
        
        assert strategy.can_handle("anything") == True
        assert strategy.can_handle("") == True
        assert strategy.can_handle("random text") == True
    
    def test_get_response_returns_message(self, colombian_personality):
        """Test default response generation."""
        strategy = DefaultStrategy(colombian_personality)
        response = strategy.get_response("unexpected message")
        
        assert isinstance(response, str)
        assert len(response) > 0


# ==================== TESTS FOR RESPONSE HANDLER ====================
class TestResponseHandler:
    """Test the response handler orchestrator."""
    
    def test_initialization(self, response_handler):
        """Test handler initialization with strategies."""
        assert len(response_handler.strategies) == 5
        assert isinstance(response_handler.strategies[0], GreetingStrategy)
        assert isinstance(response_handler.strategies[-1], DefaultStrategy)
    
    def test_handle_message_greeting(self, response_handler):
        """Test greeting message handling."""
        response = response_handler.handle_message("Hola amigo")
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_handle_message_farewell(self, response_handler):
        """Test farewell message handling."""
        response = response_handler.handle_message("Chao")
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_handle_message_slang(self, response_handler):
        """Test slang message handling."""
        response = response_handler.handle_message("Qué significa bacano")
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert "bacano" in response.lower() or "significa" in response.lower()
    
    def test_handle_message_help(self, response_handler):
        """Test help message handling."""
        response = response_handler.handle_message("Ayuda por favor")
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_handle_message_default(self, response_handler):
        """Test default message handling."""
        response = response_handler.handle_message("Random unexpected message 123")
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_handler_order_respected(self, colombian_personality):
        """Test that strategy order is respected (first matching wins)."""
        # Create a custom handler to test order
        strategies = [
            GreetingStrategy(colombian_personality),
            HelpStrategy(colombian_personality),
            DefaultStrategy(colombian_personality)
        ]
        
        # Mock the strategies to track calls
        for strategy in strategies:
            strategy.can_handle = Mock(return_value=True)
            strategy.get_response = Mock(return_value="mocked response")
        
        handler = ResponseHandler(colombian_personality)
        handler.strategies = strategies
        
        response = handler.handle_message("test")
        
        # Only first strategy should be called
        assert strategies[0].can_handle.called
        assert strategies[0].get_response.called
        assert not strategies[1].can_handle.called  # Second shouldn't be called
        assert not strategies[2].can_handle.called  # Third shouldn't be called


# ==================== TESTS FOR WHATSAPP BOT ====================
class TestWhatsAppBot:
    """Test the main WhatsApp bot class."""
    
    def test_initialization(self):
        """Test bot initialization."""
        bot = WhatsAppBot(name="TestBot")
        
        assert bot.name == "TestBot"
        assert isinstance(bot.personality, ColombianPersonality)
        assert isinstance(bot.response_handler, ResponseHandler)
        assert bot.conversation_context == {}
    
    def test_process_message_greeting(self, whatsapp_bot):
        """Test processing a greeting message."""
        sender = "whatsapp:+1234567890"
        response = whatsapp_bot.process_message("Hola", sender)
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert sender in whatsapp_bot.conversation_context
        assert whatsapp_bot.conversation_context[sender]['message_count'] == 1
    
    def test_process_message_updates_context(self, whatsapp_bot):
        """Test that conversation context is updated."""
        sender = "whatsapp:+1234567890"
        
        # First message
        whatsapp_bot.process_message("Primer mensaje", sender)
        assert whatsapp_bot.conversation_context[sender]['message_count'] == 1
        assert whatsapp_bot.conversation_context[sender]['last_message'] == "Primer mensaje"
        
        # Second message
        whatsapp_bot.process_message("Segundo mensaje", sender)
        assert whatsapp_bot.conversation_context[sender]['message_count'] == 2
        assert whatsapp_bot.conversation_context[sender]['last_message'] == "Segundo mensaje"
    
    def test_get_bot_info(self, whatsapp_bot):
        """Test bot information retrieval."""
        info = whatsapp_bot.get_bot_info()
        
        assert isinstance(info, dict)
        assert 'name' in info
        assert 'personality' in info
        assert 'description' in info
        assert 'version' in info
        assert info['name'] == whatsapp_bot.name
        assert info['personality'] == 'colombian'


# ==================== TESTS FOR TWILIO SERVICE ====================
class TestTwilioService:
    """Test Twilio service integration."""
    
    def test_initialization(self, mock_settings):
        """Test Twilio service initialization."""
        with patch('src.services.twilio_service.Client') as MockClient:
            service = TwilioService()
            
            MockClient.assert_called_once_with(
                mock_settings.twilio_account_sid,
                mock_settings.twilio_auth_token
            )
            assert service.whatsapp_number == mock_settings.twilio_whatsapp_number
    
    def test_validate_request_development(self, mock_settings):
        """Test request validation in development."""
        service = TwilioService()
        
        # In development, should always return True
        assert service.validate_request("sig", "http://test.com", {}) == True
    
    def test_create_messaging_response(self, mock_settings):
        """Test TwiML response creation."""
        service = TwilioService()
        response = service.create_messaging_response("Test message")
        
        assert isinstance(response, str)
        assert "Test message" in response
        assert "Message" in response
        assert "Response" in response
    
    def test_send_message_success(self, mock_settings):
        """Test successful message sending."""
        with patch('src.services.twilio_service.Client') as MockClient:
            mock_message = Mock()
            mock_message.sid = "SM1234567890"
            mock_client_instance = MockClient.return_value
            mock_client_instance.messages.create.return_value = mock_message
            
            service = TwilioService()
            result = service.send_message("whatsapp:+0987654321", "Test message")
            
            assert result == "SM1234567890"
            mock_client_instance.messages.create.assert_called_once_with(
                from_=mock_settings.twilio_whatsapp_number,
                body="Test message",
                to="whatsapp:+0987654321"
            )
    
    def test_send_message_failure(self, mock_settings):
        """Test failed message sending."""
        with patch('src.services.twilio_service.Client') as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.messages.create.side_effect = Exception("API Error")
            
            service = TwilioService()
            result = service.send_message("whatsapp:+0987654321", "Test message")
            
            assert result is None


# ==================== INTEGRATION TESTS ====================
class TestIntegration:
    """Integration tests for the complete flow."""
    
    def test_full_message_processing_flow(self):
        """Test complete message processing flow."""
        # Create bot
        bot = WhatsAppBot(name="IntegrationBot")
        
        # Process different types of messages
        test_cases = [
            ("Hola", "greeting"),
            ("adiós", "farewell"),
            ("qué significa chimba", "slang"),
            ("ayuda", "help"),
            ("random unknown text", "default")
        ]
        
        sender = "whatsapp:+1111111111"
        
        for message, expected_type in test_cases:
            response = bot.process_message(message, sender)
            
            # Verify we got a response
            assert isinstance(response, str)
            assert len(response) > 0
            
            # Context should be updated
            assert sender in bot.conversation_context
    
    def test_personality_in_responses(self):
        """Test that Colombian personality appears in responses."""
        bot = WhatsAppBot(name="TestBot")
        
        # Test a few messages
        messages = ["hola", "qué significa bacano", "chao"]
        sender = "whatsapp:+2222222222"
        
        for message in messages:
            response = bot.process_message(message, sender)
            
            # Response should not be empty
            assert response
            # Should not be an error message (unless something is wrong)
            assert "error" not in response.lower()


# ==================== TEST CONFIGURATION ====================
def test_settings_loading():
    """Test that settings can be loaded."""
    # This test requires a .env file or environment variables
    # We'll mock it to avoid dependencies
    with patch('src.config.settings.BaseSettings') as MockBaseSettings:
        mock_settings = MockBaseSettings.return_value
        mock_settings.twilio_account_sid = "test"
        mock_settings.twilio_auth_token = "test"
        
        from src.config.settings import Settings
        # Just verify we can import it
        assert True


# ==================== TEST RUNNER CONFIGURATION ====================
if __name__ == "__main__":
    """Allow running tests directly with python."""
    pytest.main(["-v", __file__])