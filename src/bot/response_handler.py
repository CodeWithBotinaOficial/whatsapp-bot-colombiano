from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from .personality import ColombianPersonality
import random


class ResponseStrategy(ABC):
    """Abstract base class for response strategies following Open/Closed Principle."""
    
    @abstractmethod
    def can_handle(self, message: str) -> bool:
        """Check if this strategy can handle the message."""
        pass
    
    @abstractmethod
    def get_response(self, message: str) -> str:
        """Generate response for the message."""
        pass
    
    def _clean_message(self, message: str) -> str:
        """Helper method to clean and normalize messages."""
        return message.strip().lower()


class GreetingStrategy(ResponseStrategy):
    """Handles greeting messages with comprehensive Colombian expressions."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        greetings = [
            'hola', 'buenos días', 'buenas tardes', 'buenas noches',
            'quiubo', 'qué más', 'epale', 'saludos', 'buenas', 'qué hubo',
            'cómo estás', 'cómo vas', 'todo bien'
        ]
        return any(greet in cleaned_message for greet in greetings)
    
    def get_response(self, message: str) -> str:
        # Add personality greeting with potential follow-up question
        greeting = self.personality.get_greeting()
        
        # 30% chance to add a follow-up question for engagement
        if random.random() > 0.7:
            follow_ups = [
                "¿En qué te puedo ayudar?",
                "¿Cómo va tu día?",
                "¿Qué te trae por aquí?",
                "¿Todo bien por allá?"
            ]
            return f"{greeting} {random.choice(follow_ups)}"
        
        return greeting


class FarewellStrategy(ResponseStrategy):
    """Handles farewell messages with warm Colombian style."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        farewells = [
            'adiós', 'chao', 'nos vemos', 'hasta luego', 'bye',
            'hasta pronto', 'cuídate', 'hasta la próxima', 'ahí nos vemos',
            'ahí nos vidrios', 'échele', 'vamos'
        ]
        return any(farewell in cleaned_message for farewell in farewells)
    
    def get_response(self, message: str) -> str:
        # Get farewell with possible additional warm wishes
        farewell = self.personality.get_farewell()
        
        # 25% chance to add extra warm wish
        if random.random() > 0.75:
            extra_wishes = [
                "Que te vaya súper bien.",
                "Un abrazo bien grande.",
                "Que tengas un día espectacular.",
                "Cuidado con el tráfico."
            ]
            return f"{farewell} {random.choice(extra_wishes)}"
        
        return farewell


class SlangStrategy(ResponseStrategy):
    """Handles requests about Colombian slang with detailed explanations."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        triggers = [
            'qué significa', 'qué quiere decir', 'slang', 'jerga',
            'significado de', 'qué es', 'explica', 'definición de',
            'colombianismo', 'expresión colombiana'
        ]
        return any(trigger in cleaned_message for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        cleaned_message = self._clean_message(message)
        
        # Extract potential slang words from the message
        words = cleaned_message.split()
        
        # Look for slang words in the message
        slang_words = []
        for word in words:
            # Remove punctuation
            clean_word = word.strip('.,!?¿¡')
            if clean_word in self.personality.SLANG:
                slang_words.append(clean_word)
        
        if slang_words:
            explanations = []
            for word in slang_words[:2]:  # Limit to 2 words to avoid overwhelming
                explanations.append(self.personality.explain_slang(word))
            
            # Add a fun fact about Colombian slang
            if random.random() > 0.5:
                fun_facts = [
                    "¿Sabías que Colombia tiene más de 50 palabras para 'amigo'?",
                    "La jerga colombiana varía mucho entre regiones.",
                    "Algunas palabras colombianas se usan en otros países latinos.",
                    "El 'parce' viene de 'parcero' que significa compañero."
                ]
                explanations.append(random.choice(fun_facts))
            
            return " ".join(explanations)
        
        # If no specific word found, offer to explain random slang
        if 'slang' in cleaned_message or 'jerga' in cleaned_message:
            word, meaning, description = self.personality.get_random_slang_word()
            return (f"¡Claro! Te explico una palabra al azar: '{word}' significa "
                    f"'{meaning}'. {description} ¿Quieres saber de otra?")
        
        return ("Dime exactamente qué palabra colombiana quieres que te explique, "
                "por ejemplo: '¿Qué significa parce?' ¡Vamos!")


class HelpStrategy(ResponseStrategy):
    """Handles help requests with comprehensive Colombian charm."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        triggers = [
            'ayuda', 'qué puedes hacer', 'funciones', 'comandos',
            'qué haces', 'para qué sirves', 'cómo funcionas', 'qué sabes hacer'
        ]
        return any(trigger in cleaned_message for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        help_text = f"""
        ¡Claro que sí, {self.personality.name}! Yo soy tu bot colombiano. Aquí te cuento lo que puedo hacer 🇨🇴

        📚 **Aprende jerga colombiana:**
        • "¿Qué significa parce?"
        • "Explícame la palabra chimba"
        • "Dime un colombianismo"

        💬 **Conversación colombiana:**
        • "Hola" o "Quiubo" → Saludo caluroso
        • "Chao" o "Nos vemos" → Despedida con estilo
        • "Cuéntame un chiste" → Humor colombiano
        • "Dame un consejo" → Sabiduría paisa

        🎭 **Expresiones y emociones:**
        • "¡Qué sorpresa!" → Reacciono con estilo
        • "Estoy triste" → Te doy ánimo
        • "Estoy de acuerdo" → Te apoyo
        • "No estoy seguro" → Te ayudo a decidir

        🎲 **Diversión colombiana:**
        • "Dime un dato curioso"
        • "Enséñame algo colombiano"
        • "Háblame de Colombia"

        ¡Soy como un amigo colombiano en tu bolsillo! ¿Qué te gustaría hacer primero?
        """
        
        # Clean up formatting for WhatsApp
        return "\n".join([line.strip() for line in help_text.split("\n")])


class EncouragementStrategy(ResponseStrategy):
    """Handles requests for motivation and encouragement."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        triggers = [
            'ánimo', 'triste', 'deprimido', 'desanimado', 'motivación',
            'desesperado', 'frustrado', 'cansado', 'agotado', 'necesito ánimo',
            'mal día', 'estoy mal', 'siento mal'
        ]
        return any(trigger in cleaned_message for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        encouragement = self.personality.get_encouragement()
        
        # 40% chance to add Colombian advice
        if random.random() > 0.6:
            advice = self.personality.generate_colombian_advice()
            return f"{encouragement} {advice}"
        
        return encouragement


class SurpriseStrategy(ResponseStrategy):
    """Handles expressions of surprise or shocking news."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        triggers = [
            'sorpresa', 'increíble', 'no puedo creer', 'asombroso',
            'impresionante', 'wow', 'guau', 'no me digas', 'en serio',
            'de verdad', 'qué pasó', 'qué ocurrió', 'noticia'
        ]
        return any(trigger in cleaned_message for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        surprise = self.personality.get_surprise_expression()
        
        # 50% chance to follow up with curiosity
        if random.random() > 0.5:
            follow_ups = [
                "Cuéntame más, ¿qué pasó?",
                "¿Y eso? Explícame bien.",
                "¡Qué fuerte! ¿Y luego?",
                "No jodás, ¿y cómo fue?"
            ]
            return f"{surprise} {random.choice(follow_ups)}"
        
        return surprise


class AgreementStrategy(ResponseStrategy):
    """Handles agreement expressions."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        triggers = [
            'sí', 'claro', 'exacto', 'correcto', 'afirmativo',
            'de acuerdo', 'estoy de acuerdo', 'así es', 'tienes razón',
            'totalmente', 'completamente', 'sin duda', 'por supuesto'
        ]
        return any(trigger in cleaned_message for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        agreement = self.personality.get_agreement_phrase()
        
        # 30% chance to add reinforcement
        if random.random() > 0.7:
            reinforcements = [
                "Eso es hablar claro.",
                "Así me gusta, con seguridad.",
                "Hablaste con la verdad.",
                "Palabra de honor."
            ]
            return f"{agreement} {random.choice(reinforcements)}"
        
        return agreement


class DisagreementStrategy(ResponseStrategy):
    """Handles disagreement expressions politely."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        triggers = [
            'no', 'discrepo', 'no estoy de acuerdo', 'no creo',
            'pienso diferente', 'no me convence', 'no estoy seguro',
            'tengo mis dudas', 'no sé', 'tal vez no', 'probablemente no'
        ]
        return any(trigger in cleaned_message for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        disagreement = self.personality.get_disagreement_phrase()
        
        # 40% chance to invite further discussion
        if random.random() > 0.6:
            invitations = [
                "Pero cuéntame por qué piensas así.",
                "Me interesa saber tu punto de vista.",
                "Vamos a conversarlo, ¿te parece?",
                "Explícame más para entender."
            ]
            return f"{disagreement} {random.choice(invitations)}"
        
        return disagreement


class AdviceStrategy(ResponseStrategy):
    """Handles requests for Colombian-style advice."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        triggers = [
            'consejo', 'qué hago', 'qué debería hacer', 'necesito ayuda',
            'qué me recomiendas', 'no sé qué hacer', 'estoy en problemas',
            'dilema', 'problema', 'difícil', 'complicado'
        ]
        return any(trigger in cleaned_message for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        advice = self.personality.generate_colombian_advice()
        
        # 50% chance to add a follow-up question
        if random.random() > 0.5:
            follow_ups = [
                "¿Te sirve ese consejo?",
                "¿Qué piensas de eso?",
                "¿Te ayudo en algo más?",
                "¿Cómo te sientes ahora?"
            ]
            return f"{advice} {random.choice(follow_ups)}"
        
        return advice


class PersonalityTraitStrategy(ResponseStrategy):
    """Shares Colombian personality traits and cultural insights."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        triggers = [
            'colombiano', 'colombiana', 'cultura colombiana', 'cómo son',
            'personalidad colombiana', 'rasgo colombiano', 'qué los caracteriza',
            'cómo es la gente', 'características', 'colombia'
        ]
        return any(trigger in cleaned_message for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        trait = self.personality.get_personality_trait()
        
        # 60% chance to add more cultural context
        if random.random() > 0.4:
            contexts = [
                "Además, nos encanta el café y un buen sancocho los domingos.",
                "Por eso Colombia es el país de la felicidad, parce.",
                "Así somos, siempre con la mejor actitud.",
                "Y eso que no te he contado de nuestra música y bailes."
            ]
            return f"{trait} {random.choice(contexts)}"
        
        return trait


class RandomFactStrategy(ResponseStrategy):
    """Shares random Colombian facts or slang words."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        triggers = [
            'dato curioso', 'enséñame algo', 'cuéntame algo', 'interesante',
            'curiosidad', 'aprender', 'nuevo', 'sorpréndeme', 'qué sabes',
            'información', 'hecho', 'dime algo'
        ]
        return any(trigger in cleaned_message for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        # 50% chance to share slang, 50% chance to share fact
        if random.random() > 0.5:
            word, meaning, description = self.personality.get_random_slang_word()
            return (f"¡Te enseño una palabra colombiana! '{word}' significa "
                    f"'{meaning}'. {description} ¿Quieres saber más?")
        else:
            facts = [
                "¿Sabías que Colombia tiene más de 1,900 especies de aves? ¡El país con más diversidad de aves en el mundo!",
                "El café colombiano es considerado uno de los mejores del mundo. ¡Un orgullo paisa!",
                "Colombia es el segundo país más biodiverso del planeta después de Brasil.",
                "Gabriel García Márquez, nuestro Nobel de Literatura, hizo famoso el realismo mágico.",
                "En Colombia hablamos el español más claro y neutro de Latinoamérica, según muchos lingüistas.",
                "Tenemos carnavales como el de Barranquilla, declarado Patrimonio Cultural de la Humanidad.",
                "La arepa colombiana tiene más de 75 preparaciones diferentes según la región."
            ]
            return random.choice(facts)


class JokeStrategy(ResponseStrategy):
    """Tells Colombian-style jokes or humorous anecdotes."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        cleaned_message = self._clean_message(message)
        triggers = [
            'chiste', 'broma', 'gracioso', 'divertido', 'humor',
            'cuéntame un chiste', 'río', 'reír', 'alegría', 'felicidad'
        ]
        return any(trigger in cleaned_message for trigger in triggers)
    
    def get_response(self, message: str) -> str:
        jokes = [
            "¿Qué le dice un colombiano a otro cuando se van de rumba? 'Nos vemos en el guayabo' 😄",
            "¿Por qué el colombiano no usa reloj? Porque siempre llega 'ahorita'.",
            "Un colombiano le dice a su amigo: 'Oye, ¿me prestas un 14?' El amigo responde: '¿14 qué?' '¡14 pesos, hombre!'",
            "¿Qué hace un colombiano cuando gana la lotería? Compra más chances.",
            "Un paisano llega a Bogotá y pregunta: '¿Dónde puedo tomar un tinto?' Le responden: 'En todas partes, menos en la noche'.",
            "¿Cómo sabe un colombiano que el café está listo? Cuando el vecino pregunta '¿Ya está listo el tinto?'",
            "Un costeño, un paisa y un rolo van en un carro. ¿Quién maneja? ¡La policía! 🤣"
        ]
        return random.choice(jokes)


class DefaultStrategy(ResponseStrategy):
    """Default response strategy with improved Colombian engagement."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
    
    def can_handle(self, message: str) -> bool:
        return True  # This is the catch-all strategy
    
    def get_response(self, message: str) -> str:
        cleaned_message = self._clean_message(message)
        
        # More engaging default responses
        responses = [
            f"¡Vea! No entendí bien eso, ¿me lo explicas de nuevo?",
            f"¿Cómo dice, mi hermano? No capté bien eso.",
            f"¡Uy! Creo que no te entendí. ¿Me lo repites?",
            f"¿Perdón? No pude entender eso. Cuéntame de nuevo, ¡vamos!",
            f"Mmm, no estoy seguro de entender. ¿Puedes decirlo de otra forma?",
            f"¡O sea! No me quedó claro. ¿Me lo explicas mejor?"
        ]
        
        # 20% chance to suggest help
        if random.random() > 0.8 and len(cleaned_message) > 3:
            suggestions = [
                f"Puedo ayudarte si me preguntas cosas como '¿Qué significa parce?' o 'Dame un consejo'.",
                f"¿Quieres que te explique algo de Colombia o nuestra jerga?",
                f"Intenta preguntarme '¿Qué puedes hacer?' para ver todo lo que te puedo ayudar."
            ]
            return random.choice(suggestions)
        
        return self.personality.add_colombian_flavor(random.choice(responses))


class ResponseHandler:
    """Orchestrates response strategies with improved strategy pattern."""
    
    def __init__(self, personality: ColombianPersonality):
        self.personality = personality
        self.strategies = [
            GreetingStrategy(personality),
            FarewellStrategy(personality),
            SlangStrategy(personality),
            HelpStrategy(personality),
            EncouragementStrategy(personality),
            SurpriseStrategy(personality),
            AgreementStrategy(personality),
            DisagreementStrategy(personality),
            AdviceStrategy(personality),
            PersonalityTraitStrategy(personality),
            RandomFactStrategy(personality),
            JokeStrategy(personality),
            DefaultStrategy(personality)  # Always last as fallback
        ]
    
    def handle_message(self, message: str) -> str:
        """Process message and return appropriate response."""
        if not message or not message.strip():
            return "¿Estás ahí? No escuché nada, parce. ¡Escribe algo!"
        
        for strategy in self.strategies:
            if strategy.can_handle(message):
                response = strategy.get_response(message)
                # Add Colombian flavor with probability
                if random.random() > 0.3:  # 70% chance to add flavor
                    response = self.personality.add_colombian_flavor(response)
                return response
        
        # Fallback (should never reach here due to DefaultStrategy)
        return self.personality.add_colombian_flavor("¡Uy! Algo pasó. ¿Me repites?")
    
    def get_available_strategies(self) -> List[str]:
        """Returns list of available strategy names for debugging."""
        return [strategy.__class__.__name__ for strategy in self.strategies]