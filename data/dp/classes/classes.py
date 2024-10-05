class ClassDefault:
    def __init__(self):
        self.name: str
        self.hp: float
        self.atk: float
        self.cr: float
        self.dr: float
        self.gold: float = -1
        self.positive_effects: dict = {}
        self.negative_effects: dict = {}
        self.other_effects: dict = {}
        self.default_abilities = {}
        self.cooldowns: dict = {}

class Warrior(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Warrior"
        self.hp = 70
        self.atk = 70
        self.cr = 20
        self.dr = 0
        #self.dr = 20
        self.default_abilities = ["warrior1", "warrior2", "warrior3"]

class Mage(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Mage"
        self.hp = 60
        self.atk = 60
        self.cr = 30
        self.dr = 30
        self.default_abilities = ["mage1", "mage2", "mage3"]

class Cleric(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Cleric"
        self.hp = 60
        self.atk = 50
        self.cr = 30
        self.dr = 40
        self.default_abilities = ["cleric1", "cleric2", "cleric3"]

class Ninja(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Ninja"
        self.hp = 30
        self.atk = 50
        self.cr = 30
        self.dr = 70
        self.default_abilities = ["ninja1", "ninja2", "ninja3"]

class Paladin(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Paladin"
        self.hp = 70
        self.atk = 60
        self.cr = 30
        self.dr = 20
        self.default_abilities = ["paladin1", "paladin2", "paladin3"]

class Trapper(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Trapper"
        self.hp = 70
        self.atk = 80
        self.cr = 10
        self.dr = 20
        self.default_abilities = ["trapper1", "trapper2", "trapper3"]

class Archer(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Archer"
        self.hp = 50
        self.atk = 50
        self.cr = 40
        self.dr = 40
        self.default_abilities = ["archer1", "archer2", "archer3"]

class Berserker(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Berserker"
        self.hp = 90
        self.atk = 60
        self.cr = 20
        self.dr = 10
        self.default_abilities = ["berserker1", "berserker2", "berserker3"]

class Bard(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Bard"
        self.hp = 60
        self.atk = 40
        self.cr = 40
        self.dr = 40
        self.default_abilities = ["bard1", "bard2", "bard3"]

class Necromancer(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Necromancer"
        self.hp = 60
        self.atk = 70
        self.cr = 20
        self.dr = 30
        self.default_abilities = ["necromancer1", "necromancer2", "necromancer3"]

class Gambler(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Gambler"
        self.hp = 60
        self.atk = 40
        self.cr = 40
        self.dr = 40
        self.gold = 0
        self.default_abilities = ["gambler1", "gambler2", "gambler3"]

class Spirit(ClassDefault):
    def __init__(self):
        super().__init__()
        self.name = "Spirit"
        self.hp = 30
        self.atk = 70
        self.cr = 30
        self.dr = 50
        self.default_abilities = ["spirit1", "spirit2", "spirit3"]

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