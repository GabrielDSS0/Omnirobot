import random

from src.vars import Varlist
from src.minigames.subroom.dp.data.abilities.abilities import *

class ActsCalculator():
    def __init__(self, idGame, player, ability, targets, players_classes) -> None:
        self.idGame = idGame
        self.player = player
        self.ability = ability
        self.targets = targets
        self.players_classes = players_classes
        self.damages = {}
        self.enemyTeam = {}
        self.playerTeam = {}
        self.sql_commands = Varlist.sql_commands
        self.room = Varlist.room

        self.player_class = self.players_classes[self.player]
        self.ability_class = abilities_dict[self.ability]

        self.hpEnemies = {}
        for enemy in self.enemyTeam:
            enemy_class = self.players_classes[enemy]
            self.hpEnemies[enemy] = enemy_class.hp
    
    def makeAction(self, action):
        self.sql_commands.insert_dp_action(self.idGame, action)
    
    def update_damages(self):
        self.damages = abilities_dict[self.ability].damages.copy()

    def roll(self, maxRoll):
        roll = random.randint(1, maxRoll)
        return roll
    
    def dodge(self, dr):
        roll = self.roll(100)
        if not (roll <= dr):
            return
        return True
    
    def critical(self, cr):
        roll = self.roll(100)
        if not (roll <= cr):
            return
        return True

    def make_default_damage(self, target, damage, critical=False):
        shield_value = 0
        shield = False
        
        target_class = self.players_classes[target]
        target_hp = target_class.hp
        if "ESCUDO" in target_class.positive_effects:
            shield_value = target_class.positive_effects["ESCUDO"]["VALOR"]
            shield = True

        if shield_value > 0 and not critical:
            shield_value -= damage
            if shield_value < 0:
                target_hp += shield_value
                shield_value = 0
        else:
            target_hp -= damage

        if shield:
            if shield_value == 0:
                target_class.positive_effects.pop("ESCUDO")
            else:
                target_class.positive_effects["ESCUDO"]["VALOR"] = shield_value

        target_class.hp = target_hp
    
    def basic_attack(self, player, targets):
        damage = self.players_classes[player].atk / 10
        critical = damage * 1.5
        self.damages = {
            "DAMAGE": damage,
            "CRITICAL": critical
        }

        for target in targets:
            target_class = self.players_classes[target]
            dodge_rate = target_class.dr
            dodge = self.dodge(dodge_rate)
            if not dodge:
                critical_rate = self.player_class.cr
                critical = self.critical(critical_rate)
                if critical:
                    damage = self.damages["CRITICAL"]
                else:
                    damage = self.damages["DAMAGE"]
                self.make_default_damage(target, damage)

    def ability_calc(self):
        self.player_class = self.players_classes[self.player]

        if self.ability == "warrior1":
            for target in self.targets:
                target_class = self.players_classes[target]
                dodge_rate = target_class.dr
                dodge = self.dodge(dodge_rate)
                if not dodge:
                    critical_rate = self.player_class.cr
                    critical = self.critical(critical_rate)
                    if critical:
                        damage = self.damages["CRITICAL"]
                    else:
                        damage = self.damages["DAMAGE"]
                    self.make_default_damage(target, damage)
                    if "ENFRAQUECIDO" in target_class.negative_effects:
                        effect_value = target_class.negative_effects["ENFRAQUECIDO"]["VALOR"]
                        effect_value += 20
                        if effect_value > 90:
                            effect_value = 90
                    else:
                        effect_value = 20
                    target_class.negative_effects["ENFRAQUECIDO"] = {"VALOR": effect_value, "ROUNDS": 2}
        
        elif self.ability == "warrior2":
            for target in self.targets:
                target_class = self.players_classes[target]
                if "PROTEGIDO" in target_class.positive_effects:
                    effect_value = target_class.positive_effects["PROTEGIDO"]["VALOR"]
                    effect_value += 60
                    if effect_value > 90:
                            effect_value = 90
                    else:
                        effect_value = 60
                    target_class.negative_effects["PROTEGIDO"] = {"VALOR": effect_value, "ROUNDS": 2}

        elif self.ability == "warrior3":
            maxHp = max(self.hpEnemies, key=self.hpEnemies.get)
            target_class = self.players_classes[maxHp]
            dodge_rate = target_class.dr
            dodge = self.dodge(dodge_rate)
            if not dodge:
                critical_rate = self.player_class.cr
                critical = self.critical(critical_rate)
                if critical:
                    damage = self.damages["CRITICAL"]
                else:
                    damage = self.damages["DAMAGE"]
                self.make_default_damage(target, damage)
        
        elif self.ability == "mage1":
            self.targets = self.enemyTeam
            for target in self.targets:
                target_class = self.players_classes[target]
                dodge_rate = target_class.dr
                dodge = self.dodge(dodge_rate)
                if not dodge:
                    critical_rate = self.player_class.cr
                    critical = self.critical(critical_rate)
                    if critical:
                        damage = self.damages["CRITICAL"]
                    else:
                        damage = self.damages["DAMAGE"]
                    self.make_default_damage(target, damage)
        
        elif self.ability == "mage2":
            for target in self.targets:
                target_class = self.players_classes[target]
                target_class.other_effects["ESCUDO_DE_FOGO"] = {}

        elif self.ability == "mage3":
            for target in self.targets:
                target_class = self.players_classes[target]
                dodge_rate = target_class.dr
                dodge = self.dodge(dodge_rate)
                if not dodge:
                    burned = False
                    if "QUEIMADO" in target_class.negative_effects:
                        burned = True
                    critical_rate = self.player_class.cr
                    critical = self.critical(critical_rate)
                    if critical and burned:
                        damage = self.damages["CRITICAL_BURNED"]
                    elif critical and not burned:
                        damage = self.damages["CRITICAL"]
                    elif not critical and burned:
                        damage = self.damages["DAMAGE_BURNED"]
                    elif not critical and not burned:
                        damage = self.damages["DAMAGE"]
                    self.make_default_damage(target, damage)

                    if not burned:
                        target_class.negative_effects["QUEIMADO"] = {"ROUNDS": -1}
        
        elif self.ability == "cleric1":
            for target in self.targets:
                target_class = self.players_classes[target]
                dodge_rate = target_class.dr
                dodge = self.dodge(dodge_rate)
                if not dodge:
                    critical_rate = self.player_class.cr
                    critical = self.critical(critical_rate)
                    if critical:
                        damage = self.damages["CRITICAL"]
                    else:
                        damage = self.damages["DAMAGE"]
                    self.make_default_damage(target, damage)
            
            for ally in self.playerTeam:
                ally_class = self.players_classes[ally]
                ally_class.hp += 2
                if ally_class.hp > ally_class.__class__.hp:
                    ally_class.hp = ally_class.__class__.hp
        
        elif self.ability == "cleric2":
            for target in self.targets:
                target_class = self.players_classes[target]
                target_class.hp += 8
                if ally_class.hp > ally_class.__class__.hp:
                    ally_class.hp = ally_class.__class__.hp
        
        elif self.ability == "cleric3":
            for target in self.targets:
                target_class = self.players_classes[target]
                target_class.hp += 15
                if ally_class.hp > ally_class.__class__.hp:
                    ally_class.hp = ally_class.__class__.hp
                target_class.negative_effects.clear()
        
        elif self.ability == "ninja1":
            for target in self.targets:
                target_class = self.players_classes[target]
                dodge_rate = target_class.dr
                dodge = self.dodge(dodge_rate)
                if not dodge:
                    negative_effects = False
                    if target_class.negative_effects:
                        negative_effects = True
                    critical_rate = self.player_class.cr
                    critical = self.critical(critical_rate)
                    if critical and negative_effects:
                        damage = self.damages["DOUBLE_CRITICAL"]
                    elif critical and not negative_effects:
                        damage = self.damages["CRITICAL"]
                    elif not critical and negative_effects:
                        damage = self.damages["DOUBLE_DAMAGE"]
                    elif not critical and not negative_effects:
                        damage = self.damages["DAMAGE"]
                    self.make_default_damage(target, damage)
        
        elif self.ability == "ninja2":
            for target in self.targets:
                target_class = self.players_classes[target]
                target_class.other_effects["NINJA2"] = {"ROUNDS": 2, "DR_ORIG": target_class.dr}
                target_class.dr = self.player_class.dr
        
        elif self.ability == "ninja3":
            self.atk += 10
            self.dr += 10
            self.cr += 10
            self.player_class.other_effects["NINJA3"] = {"ROUNDS": 2}
            minHp = min(self.hpEnemies, key=self.hpEnemies.get)
            targets = [minHp]
            self.basic_attack(self.player, targets)
        
        elif self.ability == "paladin1":
            times = 0
            for target in self.targets:
                twice = False 
                maxHp = max(self.hpEnemies, key=self.hpEnemies.get)
                if target == maxHp:
                    twice = True
                if twice:
                    while times != 2:         
                        target_class = self.players_classes[target]
                        dodge_rate = target_class.dr
                        dodge = self.dodge(dodge_rate)
                        if not dodge:
                            times += 1
                            critical_rate = self.player_class.cr
                            critical = self.critical(critical_rate)
                            if critical:
                                damage = self.damages["CRITICAL"]
                            else:
                                damage = self.damages["DAMAGE"]
                            self.make_default_damage(target, damage)
                        else:
                            times = 2
                            break
                else:
                    target_class = self.players_classes[target]
                    dodge_rate = target_class.dr
                    dodge = self.dodge(dodge_rate)
                    if not dodge:
                        times += 1
                        critical_rate = self.player_class.cr
                        critical = self.critical(critical_rate)
                        if critical:
                            damage = self.damages["CRITICAL"]
                        else:
                            damage = self.damages["DAMAGE"]
                        self.make_default_damage(target, damage)
        
        elif self.ability == "paladin2":
            for player in self.playerTeam:
                player_class = self.players_classes[player]
                if "PROTEGIDO" in player_class.positive_effects:
                    effect_value = player_class.negative_effects["PROTEGIDO"]["VALOR"]
                    effect_value += 20
                    if effect_value > 90:
                            effect_value = 90
                else:
                    effect_value = 20
                player_class.negative_effects["PROTEGIDO"] = {"VALOR": effect_value, "ROUNDS": 2}
        
        elif self.ability == "paladin3":
            for target in self.targets:
                if "PROTEGIDO" in target_class.positive_effects:
                    effect_value = target_class.negative_effects["PROTEGIDO"]["VALOR"]
                    effect_value += 50
                    if effect_value > 90:
                            effect_value = 90
                else:
                    effect_value = 50
                target_class.negative_effects["PROTEGIDO"] = {"VALOR": effect_value, "ROUNDS": 2}
                if "FORTALECIDO" in target_class.positive_effects:
                    effect_value = target_class.negative_effects["FORTALECIDO"]["VALOR"]
                    effect_value += 50
                else:
                    effect_value = 50
                target_class.negative_effects["FORTALECIDO"] = {"VALOR": effect_value, "ROUNDS": 2}
        
        elif self.ability == "trapper1":
            if "ESCUDO" in self.player_class.positive_effects:
                shield = self.player_class.positive_effects["ESCUDO"]["VALOR"]
                shield += 10
            else:
                shield = 10
            self.player_class.positive_effects["ESCUDO"] = {"VALOR": shield, "ROUNDS": 1}
            self.player_class.other_effects["TRAPPER1"] = {"ROUNDS": 1}
        
        elif self.ability == "trapper2":
            ability = self.targets[-1]
            for target in self.targets:
                if not (target == self.targets[-1]):
                    target_class = self.players_classes[target]
                    target_class.other_effects["TRAPPER2"] = {"ABILITY": ability, "ROUNDS": 2}
        
        elif self.ability == "trapper3":
            for player in self.playerTeam:
                player_class = self.players_classes[player]
                player_class.other_effects["TRAPPER3"] = {"VALOR": 20,"ROUNDS": 1}
        
        elif self.ability == "archer1":
            for target in self.targets:
                times = 0
                target_class = self.players_classes[target]
                while times != 3:
                    self.basic_attack(self.player, self.targets)
                    times += 1
        
        elif self.ability == "archer2":
            for player in self.playerTeam:
                player_class = self.players_classes[player]
                player_class.other_effects["ARCHER2"] = {"ROUNDS": 1}
            maxHp = max(self.hpEnemies, key=self.hpEnemies.get)
            targets = [maxHp]
            self.basic_attack(self.player, targets)
        
        elif self.ability == "archer3":
            stat = self.targets[0]
            if stat == "atk":
                self.player_class.atk += 10
            elif stat == "tc":
                self.player_class.cr += 10
            elif stat == "td":
                self.player_class.dr += 10
            minHp = min(self.hpEnemies, key=self.hpEnemies.get)
            targets = [minHp]
            self.basic_attack(self.player, targets)
        
        elif self.ability == "berserker1":
            self.player_class.hp -= 10
            aditional_atk = (((self.player_class.hp - self.player_class.__class__.hp) * -1) // 10 % 10) * 2
            for damage in self.damages:
                self.damages[damage] += aditional_atk
            
            for target in self.targets:
                target_class = self.players_classes[target]
                dodge_rate = target_class.dr
                dodge = self.dodge(dodge_rate)
                if not dodge:
                    critical_rate = self.player_class.cr
                    critical = self.critical(critical_rate)
                    if critical:
                        damage = self.damages["CRITICAL"]
                    else:
                        damage = self.damages["DAMAGE"]
                    self.make_default_damage(target, damage)
        
        elif self.ability == "berserker2":
            for player in self.playerTeam:
                player_class = self.players_classes[player]
                player_class.positive_effects["ROUBOVIDA"] = {"VALOR": 50, "ROUNDS": 1}
            self.player_class["BERSERKER2"] = {"ROUNDS": 1}
        
        elif self.ability == "berserker3":
            self.player_class.negative_effects.clear()
            self.player_class.other_effects["BERSERKER3"] = {"ROUNDS": 3}

        elif self.ability == "bard1":
            for target in self.targets:
                target_class = self.players_classes[target]
                dodge_rate = target_class.dr
                dodge = self.dodge(dodge_rate)
                if not dodge:
                    critical_rate = self.player_class.cr
                    critical = self.critical(critical_rate)
                    if critical:
                        damage = self.damages["CRITICAL"]
                    else:
                        damage = self.damages["DAMAGE"]
                    self.make_default_damage(target, damage)
                    self.target_class.positive_effects.clear()
        
        elif self.ability == "bard2":
            for player in self.playerTeam:
                player_class = self.players_classes[player]
                if "FORTALECIDO" in target_class.positive_effects:
                    effect_value = target_class.negative_effects["FORTALECIDO"]["VALOR"]
                    effect_value += 20
                else:
                    effect_value = 20
                target_class.negative_effects["FORTALECIDO"] = {"VALOR": effect_value, "ROUNDS": 2}
                self.player_class.negative_effects.clear()
        
        elif self.ability == "bard3":
            enemies = len(self.targets)
            for target in self.targets:
                target_class = self.players_classes[target]
                if self.targets[0] == target:
                    dodge_rate = target_class.dr
                    dodge = self.dodge(dodge_rate)
                    if not dodge:
                        critical_rate = self.player_class.cr
                        critical = self.critical(critical_rate)
                        if critical:
                            damage = self.damages["CRITICAL"]
                        else:
                            damage = self.damages["DAMAGE"]
                        self.make_default_damage(target, damage)
                        self.target_class.positive_effects.clear()

                if enemies == 2 and self.targets[1] == target:
                    if "ATORDOADO" in target_class.negative_effects:
                        pass
                    else:
                        target_class.negative_effects["ATORDOADO"] = {}

                if enemies == 3 and self.targets[2] == target:
                    if "ENFRAQUECIDO" in target_class.negative_effects:
                        effect_value = target_class.negative_effects["PROTEGIDO"]["VALOR"]
                        effect_value += 50
                        if effect_value > 90:
                                effect_value = 90
                    else:
                        effect_value = 50
                    target_class.negative_effects["PROTEGIDO"] = {"VALOR": effect_value, "ROUNDS": 2}


 
        self.player_class.cooldowns[self.ability] = self.ability_class.cooldown