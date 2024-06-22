from data.classes import classes

class SwordSlash():
    NAME = "Sword Slash"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 1
    DAMAGE = 10
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {"ATORDOAR": 10}

class DefenseForce():
    NAME = "Defense Force"
    TARGET = False
    PRIORITY = 0
    COOLDOWN = 2
    DAMAGES = {}
    EFFECTS = {}

class Taunt():
    NAME = "Taunt"
    TARGET = False
    PRIORITY = 3
    COOLDOWN = 2
    DAMAGES = {}
    EFFECTS = {}

class FireFall():
    NAME = "Fire Fall"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 1
    DAMAGE = 6
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class BelieveOfBurn():
    NAME = "Believe of Burn"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 1
    DAMAGES = {}
    EFFECTS = {}

class Ignite():
    NAME = "Ignite"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 2
    DAMAGE = 8
    CRITICAL_DAMAGE = DAMAGE * 1.5
    BURNED_DAMAGE = DAMAGE * 2
    CRITICAL_BURNED_DAMAGE = BURNED_DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
        "BURNED_DAMAGE": BURNED_DAMAGE,
        "CRITICAL_BURNED_DAMAGE": CRITICAL_BURNED_DAMAGE,
    }
    EFFECTS = {}

class SpiritualExchange():
    NAME = "Spiritual Exchange"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 1
    DAMAGES = {}
    EFFECTS = {}

class Equilibrium():
    NAME = "Equilibrium"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 2
    DAMAGE = 10
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class BeBrave():
    NAME = "Be Brave"
    TARGET = False
    PRIORITY = 1
    COOLDOWN = 3
    DAMAGES = {}
    EFFECTS = {}

class Shuriken():
    NAME = "Shuriken"
    TARGET = True
    PRIORITY = 1
    COOLDOWN = 1
    DAMAGE = 6
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class DeathDance():
    NAME = "Death Dance"
    TARGET = True
    PRIORITY = 1
    COOLDOWN = 1
    DAMAGE = classes.Ninja().atkb
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class SmokeBomb():
    NAME = "Smoke Bomb"
    TARGET = True
    PRIORITY = 4
    COOLDOWN = 2
    DAMAGES = {}
    EFFECTS = {}

class Barel():
    NAME = "BAAAAAAAArel"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 1
    DAMAGE = 3
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE
    }
    EFFECTS = {}

class GivingScars():
    NAME = "Giving Scars"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 1
    DAMAGE = 2
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class HookArm():
    NAME = "Hook Arm"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 2
    DAMAGE = 4
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class DualVine():
    NAME = "Dual Vine"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 1
    DAMAGE = 5
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class MagicPlant():
    NAME = "Magic Plant"
    TARGET = False
    PRIORITY = 0
    COOLDOWN = 1
    DAMAGES = {}
    EFFECTS = {}

class WildPower():
    NAME = "Wild Power"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 2
    DAMAGE = 15
    DAMAGES = {
        "DAMAGE": DAMAGE,
    }
    EFFECTS = {}

class LevelUpAtk():
    NAME = "Level Up (ATK BOOST)"
    TARGET = False
    PRIORITY = 0
    COOLDOWN = 5
    DAMAGES = {}
    EFFECTS = {}

class LevelUpTc():
    NAME = "Level Up (Taxa de Crítico BOOST)"
    TARGET = False
    PRIORITY = 0
    COOLDOWN = 5
    DAMAGES = {}
    EFFECTS = {}

class LevelUpTd():
    NAME = "Level Up (Taxa de Desvio BOOST)"
    TARGET = False
    PRIORITY = 0
    COOLDOWN = 5
    DAMAGES = {}
    EFFECTS = {}

class TheSacredSacrifice():
    NAME = "The Sacred Sacrifice"
    TARGET = False
    PRIORITY = -2
    COOLDOWN = 0
    DAMAGES = {}
    EFFECTS = {}

class DamageReflection():
    NAME = "Damage Reflection"
    TARGET = True
    PRIORITY = 2
    COOLDOWN = 2
    DAMAGE = 0
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class StandUnited():
    NAME = "Stand United"
    TARGET = True
    PRIORITY = 2
    COOLDOWN = 2
    DAMAGES = {}
    EFFECTS = {}

class BloodBet():
    NAME = "Blood Shards"
    TARGET = False
    PRIORITY = 0
    COOLDOWN = 2
    DAMAGE = classes.Vampire().atkb
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class Batification():
    NAME = "Batification"
    TARGET = True
    PRIORITY = 2
    COOLDOWN = 2
    DAMAGES = {}
    EFFECTS = {}

class Transfusion():
    NAME = "Transfusion"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 5
    DAMAGES = {}
    EFFECTS = {}

class Stealthy():
    NAME = "Stealthy"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = 1
    DAMAGE = classes.Assassin().atkb
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class Stakeout():
    NAME = "Stakeout"
    TARGET = True
    PRIORITY = 1
    COOLDOWN = 1
    DAMAGE = 7
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class Silence():
    NAME = "Silence"
    TARGET = True
    PRIORITY = 4
    COOLDOWN = 3
    DAMAGES = {}
    EFFECTS = {}

class Karma():
    NAME = "Karma"
    TARGET = True
    PRIORITY = 2
    COOLDOWN = -1
    DAMAGE = 6
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class Prevision():
    NAME = "Prevision"
    TARGET = True
    PRIORITY = 2
    COOLDOWN = 1
    DAMAGE = 8
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

class CrystalBall():
    NAME = "Crystal Ball"
    TARGET = True
    PRIORITY = -2
    COOLDOWN = 2
    DAMAGES = {}
    EFFECTS = {}

class MiracleEye():
    NAME = "Miracle Eye"
    TARGET = False
    PRIORITY = 0
    COOLDOWN = 3
    DAMAGES = {}
    EFFECTS = {}

class BasicAtk():
    NAME = "Ataque Básico"
    TARGET = True
    PRIORITY = 0
    COOLDOWN = -1
    DAMAGE = 0
    CRITICAL_DAMAGE = DAMAGE * 1.5
    DAMAGES = {
        "DAMAGE": DAMAGE,
        "CRITICAL": CRITICAL_DAMAGE,
    }
    EFFECTS = {}

classMove = {
      "Warrior": {"swordslash": SwordSlash, "defenseforce": DefenseForce, "taunt": Taunt},
      "Mage": {"firefall": FireFall, "believeofburn": BelieveOfBurn, "ignite": Ignite},
      "Cleric": {"spiritualexchange": spiritualexchange, "equilibrium": equilibrium, "bebrave": bebrave},
      "Ninja": {"shuriken": shuriken, "deathdance": deathdance, "smokebomb": smokebomb},
      "Pirate": {"barel": barel, "givingscars": givingscars, "hookarm": hookarm},
      "Druid": {"dualvine": dualvine, "magicplant": magicplant, "wildpower": wildpower},
      "Archer": {"levelupatk": levelupatk, "leveluptc": leveluptc, "leveluptd": leveluptd},
      "Squire": {"thesacredsacrifice": thesacredsacrifice, "damagereflection": damagereflection, "standunited": standunited},
      "Vampire": {"bloodbet": bloodbet, "batification": batification, "transfusion": transfusion},
      "Assassin": {"stealthy": stealthy, "stakeout": stakeout, "silence": silence},
      "Clairvoyant": {"karma": karma, "prevision": prevision, "crystalball": crystalball, "miracleeye": miracleeye},
}

moveAndClasse = {
    'swordslash': swordslash(),
    'defenseforce': defenseforce(),
    'taunt': taunt(),
    'firefall': firefall(),
    'believeofburn': believeofburn(),
    'ignite': ignite(),
    'spiritualexchange': spiritualexchange(),
    'equilibrium': equilibrium(),
    'bebrave': bebrave(),
    'shuriken': shuriken(),
    'deathdance': deathdance(),
    'smokebomb': smokebomb(),
    'barel': barel(),
    'givingscars': givingscars(),
    'hookarm': hookarm(),
    'dualvine': dualvine(),
    'magicplant': magicplant(),
    'wildpower': wildpower(),
    'levelupatk': levelupatk(),
    'leveluptc': leveluptc(),
    'leveluptd': leveluptd(),
    'thesacredsacrifice': thesacredsacrifice(),
    'damagereflection': damagereflection(),
    'standunited': standunited(),
    'bloodbet': bloodbet(),
    'batification': batification(),
    'transfusion': transfusion(),
    'stealthy': stealthy(),
    'stakeout': stakeout(),
    'silence': silence(),
    'karma': karma(),
    'prevision': prevision(),
    'crystalball': crystalball(),
    'miracleeye': miracleeye(),
    'atkb': atkb(),
}

movesTaunted = [swordslash, firefall, believeofburn, ignite, spiritualexchange, equilibrium, shuriken, deathdance, smokebomb,
givingscars, hookarm, dualvine, batification, transfusion, stealthy, stakeout, prevision, crystalball, atkb]

movesDodgeables = [swordslash, firefall, believeofburn, ignite, equilibrium, shuriken, deathdance, barel,
givingscars, hookarm, dualvine, batification, transfusion, stealthy, stakeout, karma, prevision, crystalball, atkb]

damageMoves = [swordslash, firefall, ignite, equilibrium, shuriken, deathdance, barel, givingscars, hookarm, dualvine, batification,
stealthy, stakeout, karma, prevision, crystalball, atkb]