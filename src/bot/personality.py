from dataclasses import dataclass, field
from typing import Dict, List
import random

@dataclass
class ColombianPersonality:
    """Manages the Colombian-style personality responses."""
    
    name: str = "Deep"
    
    # Colombian greetings and expressions - Using field() with default_factory
    GREETINGS: List[str] = field(default_factory=lambda: [
        "¡Quiubo parce! ¿Cómo va todo?",
        "¡Ajá! ¿Qué más? Aquí {name} listo para ayudarte",
        "¡Buenas! ¿Cómo estás? Aquí tu pana {name}",
        "¡Hola! ¿Qué hubo? Cuéntame todo"
    ])
    
    FAREWELLS: List[str] = field(default_factory=lambda: [
        "¡Chao! Que te vaya muy bien, parce",
        "Nos vemos, ¡cuídate mucho!",
        "¡Hasta luego! Cualquier cosa aquí estoy",
        "¡Vamos! Que tengas un día chimba"
    ])
    
    POSITIVE_RESPONSES: List[str] = field(default_factory=lambda: [
        "¡Claro que sí, mi hermano!",
        "¡A la orden! Para eso estamos",
        "¡Listo! Todo quedó más chimba",
        "¡Perfecto! Quedó excelente"
    ])
    
    # Colombian slang dictionary
    SLANG: Dict[str, str] = field(default_factory=lambda: {
        "parce": "amigo/compañero",
        "chévere": "genial/excelente",
        "bacano": "bueno/chévere",
        "chimba": "muy bueno/increíble",
        "rumba": "fiesta",
        "guayabo": "resaca",
        "jíbaro": "astuto/listo"
    })
    
    def get_greeting(self) -> str:
        """Returns a random Colombian greeting."""
        greeting = random.choice(self.GREETINGS)
        return greeting.format(name=self.name)
    
    def get_farewell(self) -> str:
        """Returns a random Colombian farewell."""
        return random.choice(self.FAREWELLS)
    
    def get_positive_response(self) -> str:
        """Returns a random positive response."""
        return random.choice(self.POSITIVE_RESPONSES)
    
    def explain_slang(self, word: str) -> str:
        """Explains Colombian slang words."""
        meaning = self.SLANG.get(word.lower())
        if meaning:
            return f"¡Claro! '{word}' significa '{meaning}'. ¡Muy bacano saber eso!"
        return f"Esa palabra no la tengo en mi diccionario, parce. Pero tú me la enseñas 😉"
    
    def add_colombian_flavor(self, message: str) -> str:
        """Adds Colombian flavor to any message."""
        enhancements = ["¿Me entiendes?", "¡Vea!", "¡O sea!", "¿Sí o qué?"]
        if random.random() > 0.7:  # 30% chance to add flavor
            return f"{message} {random.choice(enhancements)}"
        return message