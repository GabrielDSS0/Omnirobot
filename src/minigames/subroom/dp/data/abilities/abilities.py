class MoveDefault:
    type_name: str
    cooldown: int
    priority: int = 0
    damages: dict = {}
    effects: dict = {}

class batk(MoveDefault):
    type_name = "Ataque Básico"
    cooldown = 0

class Warrior_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1
    damages = {
        "DAMAGE": 10,
        "CRITICAL": 10 * 1.5
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


class Mage_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 3
    damages = {
        "DAMAGE": 18,
        "CRITICAL": 18 * 1.5,
        "DAMAGE_BURNED": 18 * 2,
        "CRITICAL_BURNED": 18 * 1.5 * 2
    }

class Cleric_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1
    damages = {
        "DAMAGE": 8,
        "CRITICAL": 8 * 1.5
    }

class Cleric_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 2

class Cleric_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 4

class Ninja_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1
    damages = {
        "DAMAGE": 6,
        "CRITICAL": 6 * 1.5,
        "DOUBLE_DAMAGE": 6 * 1.5,
        "DOUBLE_CRITICAL": 6 * 1.5 * 2
    }

class Ninja_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 2
    priority = 1

class Ninja_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 3

class Paladin_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1
    damages = {
        "DAMAGE": 8,
        "CRITICAL": 8 * 1.5
    }

class Paladin_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 1

class Paladin_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 2

class Trapper_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1
    priority = 1
    damages = {
        "DAMAGE": 10,
        "CRITICAL": 10 * 1.5
    }

class Trapper_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 2
    priority = 5

class Trapper_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 2
    priority = 2
    damages = {
        "DAMAGE": 18,
        "CRITICAL": 18 * 1.5,
    }

class Archer_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 2

class Archer_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 1

class Archer_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 2

class Berserker_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 0
    damages = {
        "DAMAGE": 10,
        "CRITICAL": 10 * 1.5
    }

class Berserker_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 0

class Berserker_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 0

class Bard_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1
    damages = {
        "DAMAGE": 10,
        "CRITICAL": 10 * 1.5
    }

class Bard_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 1

class Bard_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 3
    damages = {
        "DAMAGE": 18,
        "CRITICAL": 18 * 1.5,
    }

class Necromancer_00(MoveDefault):
    type_name = "Passiva"
    cooldown = 1

class Necromancer_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 2
    damages = {
        "DAMAGE": 13,
        "CRITICAL": 13 * 1.5
    }

class Necromancer_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 1

class Necromancer_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 2

class Gambler_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1

class Gambler_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 1
    priority = 2

class Gambler_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 0

class Spirit_01(MoveDefault):
    type_name = "Habilidade de Ataque"
    cooldown = 1
    damages = {
        "DAMAGE": 6,
        "CRITICAL": 6 * 1.5
    }

class Spirit_02(MoveDefault):
    type_name = "Habilidade de Suporte"
    cooldown = 2

class Spirit_03(MoveDefault):
    type_name = "Habilidade Especial"
    cooldown = 0


abilities_dict = {
    "warrior1": Warrior_01,
    "warrior2": Warrior_02,
    "warrior3": Warrior_03,
    "mage1": Mage_01,
    "mage2": Mage_02,
    "mage3": Mage_03,
}