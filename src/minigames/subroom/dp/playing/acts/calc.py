import random

from src.vars import Varlist
from src.sending import respondRoom
from src.minigames.subroom.dp.data.abilities.abilities import *

class ActsCalculator():
    def __init__(self, idGame, player, act, targets, players_classes: dict) -> None:
        self.idGame = idGame
        self.player = player
        self.act = act
        self.targets = targets
        self.players_classes = players_classes
        self.sql_commands = Varlist.sql_commands
        self.room = Varlist.room
    
    def makeAction(self, action):
        self.sql_commands.insert_dp_action(self.idGame, action)
    
    def act_calc(self):
        player_class = self.players_classes[self.player]
        act_class = abilities_dict[self.act]
        if self.act == "warrior1":
            for target in self.targets:
                target_class = self.players_classes[target]
                dodge_rate = target_class.dr
                roll = random.randint(1, 100)
                self.makeAction(f"Roll 1 de 100: {roll}")
                if not(roll <= dodge_rate):
                    critical_rate = player_class.cr
                    roll = random.randint(1, 100)
                    self.makeAction(f"Roll 1 de 100: {roll}")
                    if not (roll <= critical_rate):
                        target_class.hp -= 10
                    else:
                        target_class.hp -= 15