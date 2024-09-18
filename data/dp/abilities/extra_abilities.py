class MoveDefault:
    type_name: str
    cooldown: int
    priority: int = 0
    damages: dict = {}
    effects: dict = {}

class Escudo_de_Fogo(MoveDefault):
    type_name = "Escudo de Fogo"
    cooldown = 0
    damages = {
    "DAMAGE": 14,
    "CRITICAL": 14 * 1.5
    }

abilities_dict = {
    "escudodefogo": Escudo_de_Fogo,
}