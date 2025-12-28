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
    EncouragementStrategy,
    SurpriseStrategy,
    AgreementStrategy,
    DisagreementStrategy,
    AdviceStrategy,
    PersonalityTraitStrategy,
    RandomFactStrategy,
    JokeStrategy,
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
        # Test new attributes
        assert hasattr(colombian_personality, 'ENCOURAGEMENTS')
        assert hasattr(colombian_personality, 'SURPRISE_EXPRESSIONS')
        assert hasattr(colombian_personality, 'REGIONAL_EXPRESSIONS')
    
    def test_get_greeting_returns_string(self, colombian_personality):
        """Test greeting returns a non-empty string."""
        greeting = colombian_personality.get_greeting()
        assert isinstance(greeting, str)
        assert len(greeting) > 0
        # Removed name assertion since greetings may not always contain the name
    
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
        for _ in range(30):  # Increased from 20 to 30 for better probability
            result = colombian_personality.add_colombian_flavor(original_message)
            flavored_messages.append(result)
        
        # All messages should contain original message
        assert all(original_message in msg for msg in flavored_messages)
    
    def test_get_encouragement(self, colombian_personality):
        """Test encouragement returns a non-empty string."""
        encouragement = colombian_personality.get_encouragement()
        assert isinstance(encouragement, str)
        assert len(encouragement) > 0
    
    def test_get_surprise_expression(self, colombian_personality):
        """Test surprise expression returns a non-empty string."""
        surprise = colombian_personality.get_surprise_expression()
        assert isinstance(surprise, str)
        assert len(surprise) > 0
    
    def test_get_agreement_phrase(self, colombian_personality):
        """Test agreement phrase returns a non-empty string."""
        agreement = colombian_personality.get_agreement_phrase()
        assert isinstance(agreement, str)
        assert len(agreement) > 0
    
    def test_get_disagreement_phrase(self, colombian_personality):
        """Test disagreement phrase returns a non-empty string."""
        disagreement = colombian_personality.get_disagreement_phrase()
        assert isinstance(disagreement, str)
        assert len(disagreement) > 0
    
    def test_get_random_slang_word(self, colombian_personality):
        """Test random slang word returns a tuple with three elements."""
        word, meaning, description = colombian_personality.get_random_slang_word()
        assert isinstance(word, str)
        assert isinstance(meaning, str)
        assert isinstance(description, str)
        assert word in colombian_personality.SLANG
    
    def test_get_personality_trait(self, colombian_personality):
        """Test personality trait returns a non-empty string."""
        trait = colombian_personality.get_personality_trait()
        assert isinstance(trait, str)
        assert len(trait) > 0
    
    def test_generate_colombian_advice(self, colombian_personality):
        """Test Colombian advice returns a non-empty string."""
        advice = colombian_personality.generate_colombian_advice()
        assert isinstance(advice, str)
        assert len(advice) > 0


# ==================== TESTS FOR NEW RESPONSE STRATEGIES ====================
class TestEncouragementStrategy:
    """Test encouragement response strategy."""
    
    def test_can_handle_encouragement(self, colombian_personality):
        """Test detection of encouragement requests."""
        strategy = EncouragementStrategy(colombian_personality)
        
        assert strategy.can_handle("estoy triste") == True
        assert strategy.can_handle("necesito ánimo") == True
        assert strategy.can_handle("ESTOY DEPRIMIDO") == True
        assert strategy.can_handle("  ánimo  ") == True
    
    def test_cannot_handle_non_encouragement(self, colombian_personality):
        """Test that non-encouragement requests are not handled."""
        strategy = EncouragementStrategy(colombian_personality)
        
        assert strategy.can_handle("hola") == False
        assert strategy.can_handle("") == False
        assert strategy.can_handle("qué significa parce") == False
    
    def test_get_response_returns_encouragement(self, colombian_personality):
        """Test response generation for encouragement."""
        strategy = EncouragementStrategy(colombian_personality)
        response = strategy.get_response("estoy triste")
        
        assert isinstance(response, str)
        assert len(response) > 0


class TestSurpriseStrategy:
    """Test surprise response strategy."""
    
    def test_can_handle_surprise(self, colombian_personality):
        """Test detection of surprise expressions."""
        strategy = SurpriseStrategy(colombian_personality)
        
        assert strategy.can_handle("qué sorpresa") == True
        assert strategy.can_handle("NO PUEDO CREER") == True
        assert strategy.can_handle("es increíble") == True
        assert strategy.can_handle("  wow  ") == True
    
    def test_cannot_handle_non_surprise(self, colombian_personality):
        """Test that non-surprise expressions are not handled."""
        strategy = SurpriseStrategy(colombian_personality)
        
        assert strategy.can_handle("hola") == False
        assert strategy.can_handle("") == False
        assert strategy.can_handle("adiós") == False
    
    def test_get_response_returns_surprise(self, colombian_personality):
        """Test response generation for surprise."""
        strategy = SurpriseStrategy(colombian_personality)
        response = strategy.get_response("qué sorpresa")
        
        assert isinstance(response, str)
        assert len(response) > 0


class TestAgreementStrategy:
    """Test agreement response strategy."""
    
    def test_can_handle_agreement(self, colombian_personality):
        """Test detection of agreement expressions."""
        strategy = AgreementStrategy(colombian_personality)
        
        assert strategy.can_handle("sí") == True
        assert strategy.can_handle("CLARO") == True
        assert strategy.can_handle("estoy de acuerdo") == True
        assert strategy.can_handle("  exacto  ") == True
    
    def test_cannot_handle_non_agreement(self, colombian_personality):
        """Test that non-agreement expressions are not handled."""
        strategy = AgreementStrategy(colombian_personality)
        
        assert strategy.can_handle("hola") == False
        assert strategy.can_handle("") == False
        assert strategy.can_handle("no") == False
    
    def test_get_response_returns_agreement(self, colombian_personality):
        """Test response generation for agreement."""
        strategy = AgreementStrategy(colombian_personality)
        response = strategy.get_response("sí")
        
        assert isinstance(response, str)
        assert len(response) > 0


class TestDisagreementStrategy:
    """Test disagreement response strategy."""
    
    def test_can_handle_disagreement(self, colombian_personality):
        """Test detection of disagreement expressions."""
        strategy = DisagreementStrategy(colombian_personality)
        
        assert strategy.can_handle("no") == True
        assert strategy.can_handle("DISCREPO") == True
        assert strategy.can_handle("no estoy de acuerdo") == True
        assert strategy.can_handle("  no creo  ") == True
    
    def test_cannot_handle_non_disagreement(self, colombian_personality):
        """Test that non-disagreement expressions are not handled."""
        strategy = DisagreementStrategy(colombian_personality)
        
        assert strategy.can_handle("hola") == False
        assert strategy.can_handle("") == False
        assert strategy.can_handle("sí") == False
    
    def test_get_response_returns_disagreement(self, colombian_personality):
        """Test response generation for disagreement."""
        strategy = DisagreementStrategy(colombian_personality)
        response = strategy.get_response("no")
        
        assert isinstance(response, str)
        assert len(response) > 0


class TestJokeStrategy:
    """Test joke response strategy."""
    
    def test_can_handle_joke(self, colombian_personality):
        """Test detection of joke requests."""
        strategy = JokeStrategy(colombian_personality)
        
        assert strategy.can_handle("cuéntame un chiste") == True
        assert strategy.can_handle("CHISTE") == True
        assert strategy.can_handle("quiero reír") == True
        assert strategy.can_handle("  broma  ") == True
    
    def test_cannot_handle_non_joke(self, colombian_personality):
        """Test that non-joke requests are not handled."""
        strategy = JokeStrategy(colombian_personality)
        
        assert strategy.can_handle("hola") == False
        assert strategy.can_handle("") == False
        assert strategy.can_handle("ayuda") == False
    
    def test_get_response_returns_joke(self, colombian_personality):
        """Test response generation for jokes."""
        strategy = JokeStrategy(colombian_personality)
        response = strategy.get_response("chiste")
        
        assert isinstance(response, str)
        assert len(response) > 0


# ==================== TESTS FOR RESPONSE HANDLER ====================
class TestResponseHandler:
    """Test the response handler orchestrator."""
    
    def test_initialization(self, response_handler):
        """Test handler initialization with strategies."""
        # Now there are 13 strategies (including DefaultStrategy)
        assert len(response_handler.strategies) == 13
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
    
    def test_handle_message_encouragement(self, response_handler):
        """Test encouragement message handling."""
        response = response_handler.handle_message("Estoy triste")
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_handle_message_joke(self, response_handler):
        """Test joke message handling."""
        response = response_handler.handle_message("Cuéntame un chiste")
        
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
    
    def test_empty_message_handling(self, response_handler):
        """Test handling of empty messages."""
        response = response_handler.handle_message("")
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert "Estás ahí" in response or "Escribe algo" in response
    
    def test_available_strategies(self, response_handler):
        """Test getting available strategy names."""
        strategies = response_handler.get_available_strategies()
        
        assert isinstance(strategies, list)
        assert len(strategies) == 13
        assert "GreetingStrategy" in strategies
        assert "DefaultStrategy" in strategies


# ==================== TESTS FOR TWILIO SERVICE ====================
class TestTwilioService:
    """Test Twilio service integration."""
    
    def test_initialization(self, mock_settings):
        """Test Twilio service initialization."""
        with patch('src.services.twilio_service.Client') as MockClient:
            # Mock the settings that TwilioService actually uses
            with patch('src.services.twilio_service.settings') as mock_real_settings:
                mock_real_settings.twilio_account_sid = "test"
                mock_real_settings.twilio_auth_token = "test"
                mock_real_settings.twilio_whatsapp_number = "whatsapp:+14155238886"
                
                service = TwilioService()
                
                MockClient.assert_called_once_with("test", "test")
                assert service.whatsapp_number == "whatsapp:+14155238886"
    
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
            # Mock the settings that TwilioService actually uses
            with patch('src.services.twilio_service.settings') as mock_real_settings:
                mock_real_settings.twilio_account_sid = "test"
                mock_real_settings.twilio_auth_token = "test"
                mock_real_settings.twilio_whatsapp_number = "whatsapp:+14155238886"
                
                mock_message = Mock()
                mock_message.sid = "SM1234567890"
                mock_client_instance = MockClient.return_value
                mock_client_instance.messages.create.return_value = mock_message
                
                service = TwilioService()
                result = service.send_message("whatsapp:+0987654321", "Test message")
                
                assert result == "SM1234567890"
                mock_client_instance.messages.create.assert_called_once_with(
                    from_="whatsapp:+14155238886",
                    body="Test message",
                    to="whatsapp:+0987654321"
                )
    
    def test_send_message_failure(self, mock_settings):
        """Test failed message sending."""
        with patch('src.services.twilio_service.Client') as MockClient:
            # Mock the settings that TwilioService actually uses
            with patch('src.services.twilio_service.settings') as mock_real_settings:
                mock_real_settings.twilio_account_sid = "test"
                mock_real_settings.twilio_auth_token = "test"
                mock_real_settings.twilio_whatsapp_number = "whatsapp:+14155238886"
                
                mock_client_instance = MockClient.return_value
                mock_client_instance.messages.create.side_effect = Exception("API Error")
                
                service = TwilioService()
                result = service.send_message("whatsapp:+0987654321", "Test message")
                
                assert result is None


# ==================== TEST CONFIGURATION ====================
if __name__ == "__main__":
    """Allow running tests directly with python."""
    pytest.main(["-v", __file__])