import random

class StartRound():
    def __init__(self, players_classes, team1_classes, team2_classes) -> None:
        self.players_classes = players_classes
        self.team1_classes = team1_classes
        self.team2_classes = team2_classes

    def roll(self, maxRoll):
        roll = random.randint(1, maxRoll)
        return roll

    def actionsRound(self):
        for player in self.players_classes:
            player_class = self.players_classes[player]
            if self.player in self.team1_classes:
                playerTeam = self.team1_classes
                enemyTeam = self.team2_classes
            else:
                playerTeam = self.team2_classes
                enemyTeam = self.team1_classes

            self.hpAllies = {}
            for player in playerTeam:
                player_class = self.players_classes[player]
                self.hpAllies[player] = player_class.hp

            if player_class.name == "Cleric":
                roll = roll(100)
                if roll <= 30:
                    minHp = min(self.hpAllies, key=self.hpAllies.get)
                    targets = [minHp]
                    for target in targets:
                        target_class = self.players_classes[target]
                    
                    target_class.hp += 7
                    if target_class.hp > target_class.__class__.hp:
                        target_class.hp = target_class.__class__.hp

            if "BERSERKER3" in player_class.other_effects:
                self.player_class.hp += 15
                if player_class.hp > player_class.__class__.hp:
                    player_class.hp = player_class.__class__.hp
                rounds = self.players_classes.other_effects["ROUNDS"]
                self.players_classes.other_effects["ROUNDS"] = (rounds - 1)
                if rounds == 1:
                    self.players_classes.other_effects.pop("BERSERKER3")