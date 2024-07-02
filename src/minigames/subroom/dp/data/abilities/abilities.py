class MoveDefault:
    type_name: str
    cooldown: int
    priority: int = 0
    damages: dict = {}
    effects: dict = {}

class Warrior_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1
    damages = {
        "DAMAGE": 10,
        "CRITICAL": 10 * 1.5
    }
    effects = {
        "ENFRAQUECIDO": {"ROUNDS": 2, "POWER": 20, "TYPE": "negative"}
    }

class Warrior_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 2
    priority = 1
    effects = {
        "PROTEGIDO": {"ROUNDS": 2, "POWER": 20, "TYPE": "positive"}
    }

class Warrior_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 3
    damages = {
        "DAMAGE": 33,
        "CRITICAL": 33 * 1.5
    }

class Mage_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1
    damages = {
        "DAMAGE": 6,
        "CRITICAL": 6 * 1.5
    }

class Mage_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 2
    priority = 1
    effects = {
        "ESCUDO DE FOGO": {"ROUNDS": -1, "POWER": 0, "TYPE": "other"}
    }

class Mage_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 3
    damages = {
        "DAMAGE": 18,
        "CRITICAL": 18 * 1.5
    }
    effects = {
        "QUEIMADO": {"ROUNDS": -1, "POWER": 0, "TYPE": "negative"}
    }

class Mage_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1
    damages = {
        "DAMAGE": 6,
        "CRITICAL": 6 * 1.5
    }

class Mage_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 2
    priority = 1
    effects = {
        "ESCUDO DE FOGO": {"ROUNDS": -1, "POWER": 0, "TYPE": "other"}
    }

class Mage_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 3
    damages = {
        "DAMAGE": 18,
        "CRITICAL": 18 * 1.5
    }
    effects = {
        "QUEIMADO": {"ROUNDS": -1, "POWER": 0, "TYPE": "negative"}
    }

abilities_dict = {
    "warrior1": Warrior_01,
    "warrior2": Warrior_02,
    "warrior3": Warrior_03,
    "mage1": Mage_01,
    "mage2": Mage_02,
    "mage3": Mage_03,
}