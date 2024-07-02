from src.minigames.subroom.dp.data.abilities.abilities import *

class ActsCalculator():
    def __init__(self, player, act, targets) -> None:
        self.player = player
        self.act = act
        self.targets = targets
    def act_calc(self):
        act_class = abilities_dict[self.act]
        if self.act == "warrior1":
            