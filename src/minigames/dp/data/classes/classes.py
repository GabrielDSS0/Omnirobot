class Warrior():
    def __init__(self) -> None:     
        self.name = 'Warrior'
        self.hp = 70
        self.shield = {"shield": {"value": 20, "round": 1, "infinity": True}}
        self.atk = 70
        self.critical_rate = 20
        self.dodge_rate = 20
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

class Mage():
    def __init__(self) -> None:
        self.name = 'Mage'
        self.hp = 2
        self.shield = {"shield": {"value": 0, "round": -2, "infinity": False}}
        self.atk = 65
        self.critical_rate = 20
        self.dodge_rate = 0
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 0
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

class Cleric():
    def __init__(self) -> None:
        self.name = 'Cleric'
        self.hp = 65
        self.shield = {"shield": {"value": 0, "round": -2, "infinity": False}}
        self.atk = 55
        self.critical_rate = 20
        self.dodge_rate = 40
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 0
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

class Ninja():
    def __init__(self) -> None:
        self.name = 'Ninja'
        self.hp = 30
        self.shield = {"shield": {"value": 0, "round": -2, "infinity": False}}
        self.atk = 50
        self.critical_rate = 40
        self.dodge_rate = 70
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 0
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

class Pirate():
    def __init__(self) -> None:
        self.name = 'Pirate'
        self.hp = 80
        self.shield = {"shield": {"value": 0, "round": -2, "infinity": False}}
        self.atk = 60
        self.critical_rate = 30
        self.dodge_rate = 20
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 0
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

class Druid():
    def __init__(self) -> None:
        self.name = 'Druid'
        self.hp = 65
        self.shield = {"shield": {"value": 0, "round": -2, "infinity": False}}
        self.atk = 60
        self.critical_rate = 20
        self.dodge_rate = 30
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 0
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

class Archer():
    def __init__(self) -> None:
        self.name = 'Archer'
        self.hp = 50
        self.shield = {"shield": {"value": 0, "round": -2, "infinity": False}}
        self.atk = 20
        self.critical_rate = 50
        self.dodge_rate = 50
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 1
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

class Squire():
    def __init__(self) -> None:
        self.name = 'Squire'
        self.hp = 30
        self.shield = {"shield": {"value": 40, "round": 1, "infinity": True}}
        self.atk = 40
        self.critical_rate = 30
        self.dodge_rate = 30
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 0
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

class Vampire():
    def __init__(self) -> None:
        self.name = 'Vampire'
        self.hp = 60
        self.shield = {"shield": {"value": 0, "round": -2, "infinity": False}}
        self.atk = 60
        self.critical_rate = 30
        self.dodge_rate = 30
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 0
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

class Assassin():
    def __init__(self) -> None:
        self.name = 'Assassin'
        self.hp = 50
        self.shield = {"shield": {"value": 0, "round": -2, "infinity": False}}
        self.atk = 60
        self.critical_rate = 30
        self.dodge_rate = 40
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 0
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

class Clairvoyant():
    def __init__(self) -> None:
        self.name = 'Clairvoyant'
        self.hp = 55
        self.shield = {"shield": {"value": 0, "round": -2, "infinity": False}}
        self.atk = 55
        self.critical_rate = 20
        self.dodge_rate = 40
        self.basic_atk = self.atk / 10
        self.keywords = {}
        self.class_effects = {}
        self.stack = 0
        self.levelupatk = 0
        self.levelupcr = 0
        self.levelupdr = 0
        self.sufferedDamage = {}
        self.causedDamage = {}

allClasses = {
    "warrior": Warrior,
    "mage": Mage,
    "cleric": Cleric,
    "ninja": Ninja,
    "pirate": Pirate,
    "druid": Druid,
    "archer": Archer,
    "squire": Squire,
    "vampire": Vampire,
    "assassin": Assassin,
    "clairvoyant": Clairvoyant,
}