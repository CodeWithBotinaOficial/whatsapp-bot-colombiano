from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import random


@dataclass
class ColombianPersonality:
    """Manages the Colombian-style personality responses with rich cultural expressions."""
    
    name: str = "Deep"
    
    # Expanded Colombian greetings and expressions
    GREETINGS: List[str] = field(default_factory=lambda: [
        "¡Quiubo parce! ¿Cómo va todo por ahí?",
        "¡Ajá! ¿Qué más? Aquí {name} listo para ayudarte",
        "¡Buenas! ¿Cómo estás? Cuéntame qué te trae por aquí",
        "¡Hola! ¿Qué hubo? Aquí tu pana {name} a la orden",
        "¡Epale! ¿Cómo vas? Aquí {name} pendiente de ti",
        "¡Saludos! ¿Todo bien? Para servirte"
    ])
    
    FAREWELLS: List[str] = field(default_factory=lambda: [
        "¡Chao! Que te vaya muy bien, parce",
        "Nos vemos, ¡cuídate mucho!",
        "¡Hasta luego! Cualquier cosa aquí estoy",
        "¡Vamos! Que tengas un día chimba",
        "¡Échele! Nos estamos viendo",
        "¡Ahí nos vidrios! Cuídate mucho"
    ])
    
    POSITIVE_RESPONSES: List[str] = field(default_factory=lambda: [
        "¡Claro que sí, mi hermano!",
        "¡A la orden! Para eso estamos",
        "¡Listo! Todo quedó más chimba",
        "¡Perfecto! Quedó excelente",
        "¡Hecho! Todo quedó bacano",
        "¡Listo del todo! Quedó genial"
    ])
    
    ENCOURAGEMENTS: List[str] = field(default_factory=lambda: [
        "¡Ánimo! Tú puedes con todo",
        "¡Dale con todo! Tú eres capaz",
        "¡Échele ganas! Que tú eres berraco",
        "¡Vamos que sí se puede!",
        "¡No te rajes! Tú puedes"
    ])
    
    SURPRISE_EXPRESSIONS: List[str] = field(default_factory=lambda: [
        "¡Uy! No me digas",
        "¡Guácala! ¿En serio?",
        "¡Ay, váyase! No puede ser",
        "¡Qué chimba!",
        "¡No jodás! De verdad?"
    ])
    
    AGREEMENT_PHRASES: List[str] = field(default_factory=lambda: [
        "¡Exacto! Toda la razón",
        "¡Claro! Así mismo es",
        "¡Tal cual! Como dices",
        "¡De una! Así es la cosa",
        "¡Correcto! Eso mismo"
    ])
    
    DISAGREEMENT_PHRASES: List[str] = field(default_factory=lambda: [
        "Uy, ahí no estoy muy de acuerdo",
        "Mmm, no sé, yo lo veo diferente",
        "La verdad, yo pienso otra cosa",
        "No sé, parce, eso no me cuadra mucho",
        "Mira, yo tengo otra perspectiva"
    ])
    
    # Colombian slang dictionary - significantly expanded
    SLANG: Dict[str, Tuple[str, str]] = field(default_factory=lambda: {
        # Basic slang
        "parce": ("amigo/compañero", "Término cariñoso para referirse a un amigo"),
        "chévere": ("genial/excelente", "Expresión para algo que está muy bien"),
        "bacano": ("bueno/chévere", "Similar a chévere, algo que está genial"),
        "chimba": ("muy bueno/increíble", "Algo excelente o impresionante"),
        "rumba": ("fiesta", "Una celebración o fiesta"),
        "guayabo": ("resaca", "Malestar después de una fiesta"),
        "jíbaro": ("astuto/listo", "Persona inteligente y vivaz"),
        
        # Expanded slang
        "berraco": ("valiente/talentoso", "Alguien muy hábil o valiente"),
        "camellar": ("trabajar duro", "Esforzarse mucho en el trabajo"),
        "parcero": ("amigo cercano", "Variación de parce, amigo íntimo"),
        "guachafita": ("alboroto/diversión", "Situación divertida y ruidosa"),
        "chino/a": ("niño/niña", "Término cariñoso para niños"),
        "sapo": ("chismoso", "Persona que le gusta el chisme"),
        "mamar gallo": ("bromear", "Hacer chistes o bromas"),
        "catorce": ("favor", "Pedir un catorce es pedir un favor"),
        "llave": ("amigo", "Otra forma de decir amigo o conocido"),
        "guácala": ("qué asco", "Expresión de desagrado"),
        "qué más": ("¿cómo estás?", "Saludo informal"),
        "estar tragado": ("estar enamorado", "Estar profundamente enamorado"),
        "cachaco": ("persona de Bogotá", "Gentilicio informal para bogotanos"),
        "paisa": ("persona de Antioquia", "Gentilicio para antioqueños"),
        "rolo": ("persona de Bogotá", "Otro gentilicio para bogotanos"),
        "estar en la olla": ("estar en problemas", "Tener dificultades económicas"),
        "jíbaro": ("astuto/inteligente", "Persona muy viva e inteligente"),
        "vacano": ("chévere/bacano", "Otra variante de algo bueno"),
        "pola": ("cerveza", "Término para una cerveza"),
        "tomarse un tinto": ("tomar café", "Beber una taza de café negro"),
        "quedé mamando": ("me quedé sin nada", "Quedarse sin algo esperado"),
        "estar pelado": ("no tener dinero", "Estar sin recursos económicos"),
        "dar papaya": ("dar oportunidad para problemas", "Exponerse a situaciones riesgosas"),
    })
    
    # Regional expressions by Colombian region
    REGIONAL_EXPRESSIONS: Dict[str, List[str]] = field(default_factory=lambda: {
        "paisa": ["¡Quiubo!", "¡Ándele pues!", "¡Uy, qué pena!", "¡Vea pues!"],
        "rolo": ["¡Qué más!", "¡Listo!", "¡Chévere!", "¡Órale!"],
        "costeño": ["¡Épale!", "¡Aché!", "¡Qué volá!", "¡Vamos a rumbiar!"],
        "valluno": ["¡Hágale!", "¡Cómo así!", "¡Listo!", "¡Vea!"],
        "llanero": ["¡Au!", "¡Sí, pues!", "¡Vea!", "¡Cómo no!"]
    })
    
    def get_greeting(self) -> str:
        """Returns a random Colombian greeting with personality."""
        greeting = random.choice(self.GREETINGS)
        return self._add_regional_flavor(greeting.format(name=self.name))
    
    def get_farewell(self) -> str:
        """Returns a random Colombian farewell with personality."""
        farewell = random.choice(self.FAREWELLS)
        return self._add_regional_flavor(farewell)
    
    def get_positive_response(self) -> str:
        """Returns a random positive response."""
        response = random.choice(self.POSITIVE_RESPONSES)
        return self._add_colombian_flavor(response)
    
    def get_encouragement(self) -> str:
        """Returns a random encouragement phrase."""
        return random.choice(self.ENCOURAGEMENTS)
    
    def get_surprise_expression(self) -> str:
        """Returns a random surprise expression."""
        return random.choice(self.SURPRISE_EXPRESSIONS)
    
    def get_agreement_phrase(self) -> str:
        """Returns a random agreement phrase."""
        return random.choice(self.AGREEMENT_PHRASES)
    
    def get_disagreement_phrase(self) -> str:
        """Returns a random disagreement phrase in a friendly way."""
        return random.choice(self.DISAGREEMENT_PHRASES)
    
    def explain_slang(self, word: str) -> str:
        """Explains Colombian slang words with detailed context."""
        word_lower = word.lower()
        
        if word_lower in self.SLANG:
            meaning, description = self.SLANG[word_lower]
            examples = self._get_slang_example(word_lower)
            return (f"¡Claro! '{word}' significa '{meaning}'. {description} "
                    f"{examples} ¡Muy bacano saber eso!")
        
        return (f"Esa palabra no la tengo en mi diccionario, parce. "
                f"Pero tú me la enseñas y la aprendo 😉")
    
    def get_random_slang_word(self) -> Tuple[str, str, str]:
        """Returns a random slang word with its meaning and description."""
        word = random.choice(list(self.SLANG.keys()))
        meaning, description = self.SLANG[word]
        return word, meaning, description
    
    def add_colombian_flavor(self, message: str) -> str:
        """Adds Colombian flavor to any message with various enhancements."""
        enhancements = ["¿Me entiendes?", "¡Vea!", "¡O sea!", "¿Sí o qué?", 
                       "¿Entonces?", "¡Dígale!", "¿Ah bueno?", "¡Cómo así!"]
        
        # 40% chance to add flavor instead of 30%
        if random.random() > 0.6:
            selected_enhancement = random.choice(enhancements)
            
            # Sometimes add regional expression too (20% chance when adding flavor)
            if random.random() > 0.8:
                regional = self._get_random_regional_expression()
                return f"{message} {selected_enhancement} {regional}"
            
            return f"{message} {selected_enhancement}"
        
        return message
    
    def _add_regional_flavor(self, message: str) -> str:
        """Adds a regional expression to a message with 25% probability."""
        if random.random() > 0.75:
            regional_expression = self._get_random_regional_expression()
            return f"{message} {regional_expression}"
        return message
    
    def _get_random_regional_expression(self) -> str:
        """Returns a random expression from any Colombian region."""
        all_expressions = []
        for expressions in self.REGIONAL_EXPRESSIONS.values():
            all_expressions.extend(expressions)
        return random.choice(all_expressions)
    
    def _get_slang_example(self, word: str) -> str:
        """Returns an example usage for a slang word."""
        examples = {
            "parce": "Como en: '¿Qué más, parce? ¿Vamos por un tinto?'",
            "chévere": "Como en: '¡Qué chévere está ese plan!'",
            "bacano": "Como en: 'Ese carro está bien bacano'",
            "chimba": "Como en: '¡Qué chimba de concierto!'",
            "rumba": "Como en: 'Vamos a la rumba este sábado'",
            "guayabo": "Como en: 'Amigo, tengo un guayabo brutal'",
            "berraco": "Como en: 'Ese tipo es berraco para el fútbol'",
            "camellar": "Como en: 'Hoy toca camellar todo el día'",
            "mamar gallo": "Como en: 'Deja de mamar gallo y ponte serio'",
            "dar papaya": "Como en: 'No des papaya por esos lados'",
        }
        
        return examples.get(word, "Es una expresión muy colombiana que debes usar con amigos.")
    
    def get_personality_trait(self) -> str:
        """Returns a random description of Colombian personality traits."""
        traits = [
            "Somos calidosos y nos gusta ayudar",
            "Nos encanta la rumba y la buena energía",
            "Somos berracos para salir adelante",
            "Nos gusta mamar gallo y reírnos",
            "Somos parceros y leales con los amigos",
            "Amamos nuestro café y un buen tinto",
            "Somos echados pa'lante y trabajadores"
        ]
        return random.choice(traits)
    
    def generate_colombian_advice(self) -> str:
        """Returns random Colombian-style advice."""
        advice_list = [
            "No dé papaya, parce. Cuídese siempre",
            "Échele ganas que todo se puede",
            "Tómese un tinto y piense las cosas bien",
            "No se ahueve, que todo pasa por algo",
            "Disfrute la vida, pero sin excesos",
            "Ayude al prójimo, que después le devuelven el favor",
            "Trabaje duro, pero también sepa descansar"
        ]
        return random.choice(advice_list)