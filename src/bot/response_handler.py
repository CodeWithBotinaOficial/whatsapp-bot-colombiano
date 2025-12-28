from abc import ABC, abstractmethod
from typing import Dict, Optional
from .personality import ColombianPersonality
import random


class ResponseStrategy(ABC):
    """Abstract base class for response strategies."""
    
    @abstractmethod
    def can_handle(self, message: str) -> bool:
        """Check if this strategy can handle the message."""
        pass
    
    @abstractmethod
    def get_response(self, message: str) -> str:
        """Generate response for the message."""
        pass


class GreetingStrategy(ResponseStrategy):
    """Handles greeting messages."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        greetings = ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'quiubo', 'qué más']
        return any(greet in message.lower() for greet in greetings)
    
    def get_response(self, message: str) -> str:
        return self.personality.get_greeting()


class FarewellStrategy(ResponseStrategy):
    """Handles farewell messages."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        farewells = ['adiós', 'chao', 'nos vemos', 'hasta luego', 'bye']
        return any(farewell in message.lower() for farewell in farewells)
    
    def get_response(self, message: str) -> str:
        return self.personality.get_farewell()


class SlangStrategy(ResponseStrategy):
    """Handles requests about Colombian slang."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        triggers = ['qué significa', 'qué quiere decir', 'slang', 'jerga']
        return any(trigger in message.lower() for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        words = message.lower().split()
        slang_words = [word for word in words if word in self.personality.SLANG]
        
        if slang_words:
            explanations = []
            for word in slang_words[:3]:  # Limit to 3 words max
                explanations.append(self.personality.explain_slang(word))
            return " ".join(explanations)
        
        return "Dime qué palabra colombiana quieres que te explique, ¡vamos!"


class HelpStrategy(ResponseStrategy):
    """Handles help requests."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        return 'ayuda' in message.lower() or 'qué puedes hacer' in message.lower()
    
    def get_response(self, message: str) -> str:
        help_text = """
        ¡Claro, mi hermano! Yo soy {name}, tu bot colombiano. Puedo:
        
        • Saludarte con mucho sabor colombiano 🇨🇴
        • Explicarte palabras de nuestra jerga
        • Decirte chao con todo el estilo
        • Responderte con buena energía
        
        Solo escríbeme cosas como:
        - "Hola" o "Quiubo"
        - "¿Qué significa parce?"
        - "Chao" o "Nos vemos"
        
        ¡Vamos, pregúntame lo que quieras!
        """.format(name=self.personality.name)
        
        return help_text.strip()


class DefaultStrategy(ResponseStrategy):
    """Default response strategy."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        return True  # This is the catch-all strategy
    
    def get_response(self, message: str) -> str:
        responses = [
            f"¡Vea! No entendí bien eso, ¿me lo explicas de nuevo?",
            f"¿Cómo dice, mi hermano? No capté bien eso",
            f"¡Uy! Creo que no te entendí. ¿Me lo repites?",
            f"¿Perdón? No pude entender eso. Cuéntame de nuevo, ¡vamos!"
        ]
        return self.personality.add_colombian_flavor(random.choice(responses))


class ResponseHandler:
    """Orchestrates response strategies."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
        self.strategies = [
            GreetingStrategy(personality),
            FarewellStrategy(personality),
            SlangStrategy(personality),
            HelpStrategy(personality),
            DefaultStrategy(personality)
        ]
    
    def handle_message(self, message: str) -> str:
        """Process message and return appropriate response."""
        for strategy in self.strategies:
            if strategy.can_handle(message):
                response = strategy.get_response(message)
                return self.personality.add_colombian_flavor(response)
        
        # Fallback (should never reach here due to DefaultStrategy)
        return self.personality.add_colombian_flavor("¡Uy! Algo pasó. ¿Me repites?")