class ClassDefault:
    name: str
    hp: float
    atk: float
    cr: float
    dr: float
    gold: float = -1
    positive_effects: dict = {}
    negative_effects: dict = {}
    other_effects: dict = {}
    default_abilities = {}
    cooldowns: dict = {}

class Warrior(ClassDefault):
    name = "Warrior"
    hp = 70
    atk = 70
    cr = 20
    dr = 20
    default_abilities = ["warrior1", "warrior2", "warrior3"]

class Mage(ClassDefault):
    name = "Mage"
    hp = 60
    atk = 60
    cr = 30
    dr = 30
    default_abilities = ["mage1", "mage2", "mage3"]

class Cleric(ClassDefault):
    name = "Cleric"
    hp = 60
    atk = 50
    cr = 30
    dr = 40
    default_abilities = ["cleric1", "cleric2", "cleric3"]

class Ninja(ClassDefault):
    name = "Ninja"
    hp = 30
    atk = 50
    cr = 30
    dr = 70
    default_abilities = ["ninja1", "ninja2", "ninja3"]

class Paladin(ClassDefault):
    name = "Paladin"
    hp = 70
    atk = 60
    cr = 30
    dr = 20
    default_abilities = ["paladin1", "paladin2", "paladin3"]

class Trapper(ClassDefault):
    name = "Trapper"
    hp = 70
    atk = 80
    cr = 10
    dr = 20
    default_abilities = ["trapper1", "trapper2", "trapper3"]

class Archer(ClassDefault):
    name = "Archer"
    hp = 50
    atk = 50
    cr = 40
    dr = 40
    default_abilities = ["archer1", "archer2", "archer3"]

class Berserker(ClassDefault):
    name = "Berserker"
    hp = 90
    atk = 60
    cr = 20
    dr = 10
    default_abilities = ["berserker1", "berserker2", "berserker3"]

class Bard(ClassDefault):
    name = "Bard"
    hp = 60
    atk = 40
    cr = 40
    dr = 40
    default_abilities = ["bard1", "bard2", "bard3"]

class Necromancer(ClassDefault):
    name = "Necromancer"
    hp = 60
    atk = 70
    cr = 20
    dr = 30
    default_abilities = ["necromancer1", "necromancer2", "necromancer3"]

class Gambler(ClassDefault):
    name = "Gambler"
    hp = 60
    atk = 40
    cr = 40
    dr = 40
    gold = 0
    default_abilities = ["gambler1", "gambler2", "gambler3"]

class Spirit(ClassDefault):
    name = "Spirit"
    hp = 30
    atk = 70
    cr = 30
    dr = 50
    default_abilities = ["spirit1", "spirit2", "spirit3"]

classes_dict = {
    "warrior": Warrior,
    "mage": Mage,
    "cleric": Cleric,
    "ninja": Ninja,
    "paladin": Paladin,
    "trapper": Trapper,
    "archer": Archer,
    "berserker": Berserker,
    "bard": Bard,
    "necromancer": Necromancer,
    "gambler": Gambler,
    "spirit": Gambler,
}