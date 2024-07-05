class ClassDefault:
    name: str
    hp: float
    atk: float
    cr: float
    dr: float
    gold: float = -1
    shield: dict = {}
    positive_effects: dict = {}
    negative_effects: dict = {}
    other_effects: dict = {}

class Warrior(ClassDefault):
    name = "Warrior"
    hp = 70
    atk = 70
    cr = 20
    dr = 20

class Mage(ClassDefault):
    name = "Mage"
    hp = 60
    atk = 60
    cr = 30
    dr = 30

class Cleric(ClassDefault):
    name = "Cleric"
    hp = 60
    atk = 50
    cr = 30
    dr = 40

class Ninja(ClassDefault):
    name = "Ninja"
    hp = 30
    atk = 50
    cr = 30
    dr = 70

class Paladin(ClassDefault):
    name = "Paladin"
    hp = 70
    atk = 60
    cr = 30
    dr = 20

class Trapper(ClassDefault):
    name = "Trapper"
    hp = 70
    atk = 80
    cr = 10
    dr = 20

class Archer(ClassDefault):
    name = "Archer"
    hp = 50
    atk = 50
    cr = 40
    dr = 40

class Berserker(ClassDefault):
    name = "Berserker"
    hp = 90
    atk = 60
    cr = 20
    dr = 10

class Bard(ClassDefault):
    name = "Bard"
    hp = 60
    atk = 40
    cr = 40
    dr = 40

class Necromancer(ClassDefault):
    name = "Necromancer"
    hp = 60
    atk = 70
    cr = 20
    dr = 30

class Gambler(ClassDefault):
    name = "Gambler"
    hp = 60
    atk = 40
    cr = 40
    dr = 40
    gold = 0

class Spirit(ClassDefault):
    name = "Spirit"
    hp = 30
    atk = 70
    cr = 30
    dr = 50

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