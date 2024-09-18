import asyncio
import random

from src.vars import Varlist
from src.sending import respondRoom

class PostRound():
    def __init__(self, idGame, room, playersClasses, team1_classes, team2_classes) -> None:
        self.idGame = idGame
        self.room = room
        self.sql_commands = Varlist.sql_commands
        self.dpGames = Varlist.dpGames
        self.playersClasses = playersClasses
        self.team1_classes = team1_classes
        self.team2_classes = team2_classes

    def controller(self):
        self.round_final_moves()
        self.startRound = True
        return self.startRound

    def round_final_moves(self):
        for player in self.playersClasses:
            player_class = self.playersClasses[player]
            if player in self.team1_classes:
                playerTeam = self.team1_classes
                enemyTeam = self.team2_classes
            else:
                playerTeam = self.team2_classes
                enemyTeam = self.team1_classes

            if "TRAPPER00" in player_class.other_effects:
                player_class.other_effects.pop("TRAPPER00")

            if player_class.name == "Trapper":
                ally_chosen = random.choice(list(self.playersClasses))
                ally_chosen_class = self.playersClasses[ally_chosen]
                ally_chosen_class.other_effects["TRAPPER00"] = {"ROUNDS": 1}

    async def writing_actions(self):
        actions = self.sql_commands.select_dp_actions(self.idGame)
        for act in actions:
            await asyncio.sleep(2)
            act = act[0]
            respondRoom(f"**{act}**", self.room)

        self.sql_commands.delete_dp_actions(self.idGame)