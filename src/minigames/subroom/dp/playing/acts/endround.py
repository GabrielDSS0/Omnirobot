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
    
    def rollPlusMinus(self, maxRoll, add):
        roll = random.randint(1, maxRoll)
        roll += add
        return roll

    def round_final_moves(self):
        for player in self.playersClasses:
            player_class = self.playersClasses[player]
            if player in self.team1_classes:
                playerTeam = self.team1_classes
                enemyTeam = self.team2_classes
            else:
                playerTeam = self.team2_classes
                enemyTeam = self.team1_classes
            
            if "ENVENENADO" in player_class.negative_effects:
                roll = self.rollPlusMinus(5, 4)
                player_class.hp -= roll

            if "TRAPPER00" in player_class.other_effects:
                rounds = player_class.other_effects["TRAPPER00"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.other_effects.pop("TRAPPER00")
                else:
                    player_class.other_effects["TRAPPER00"]["ROUNDS"] = rounds
            
            if "TRAPPER2" in player_class.other_effects:
                rounds = player_class.other_effects["TRAPPER2"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.other_effects.pop("TRAPPER2")
                else:
                    player_class.other_effects["TRAPPER2"]["ROUNDS"] = rounds
            
            if "ARCHER2" in player_class.other_effects:
                rounds = player_class.other_effects["ARCHER2"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.other_effects.pop("ARCHER2")
                    player_class.cr -= 10
                else:
                    player_class.other_effects["ARCHER2"]["ROUNDS"] = rounds
            
            if "PROTEGIDO" in player_class.positive_effects:
                rounds = player_class.positive_effects["PROTEGIDO"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.positive_effects.pop("PROTEGIDO")
                else:
                    player_class.positive_effects["PROTEGIDO"]["ROUNDS"] = rounds

            if "FORTALECIDO" in player_class.positive_effects:
                rounds = player_class.positive_effects["FORTALECIDO"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.positive_effects.pop("FORTALECIDO")
                else:
                    player_class.positive_effects["FORTALECIDO"]["ROUNDS"] = rounds

            if "VULNERAVEL" in player_class.negative_effects:
                rounds = player_class.negative_effects["VULNERAVEL"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.negative_effects.pop("VULNERAVEL")
                else:
                    player_class.negative_effects["VULNERAVEL"]["ROUNDS"] = rounds

            if "ENFRAQUECIDO" in player_class.negative_effects:
                rounds = player_class.negative_effects["ENFRAQUECIDO"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.negative_effects.pop("ENFRAQUECIDO")
                else:
                    player_class.negative_effects["ENFRAQUECIDO"]["ROUNDS"] = rounds
            
            if "QUEIMADO" in player_class.negative_effects:
                player_class.hp -= 7
            
            if "NINJA2" in player_class.other_effects:
                rounds = player_class.other_effects["NINJA2"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.other_effects.pop("NINJA2")
                    player_class.dr = player_class.other_effects["NINJA2"]["DR_ORIG"]
                else:
                    player_class.other_effects["NINJA2"]["ROUNDS"] = rounds
            
            if "NINJA3" in player_class.other_effects:
                rounds = player_class.other_effects["NINJA3"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.other_effects.pop("NINJA3")
                    player_class.atk -= 10
                    player_class.cr -= 10
                    player_class.dr -= 10
                else:
                    player_class.other_effects["NINJA3"]["ROUNDS"] = rounds

    async def writing_actions(self):
        actions = self.sql_commands.select_dp_actions(self.idGame)
        for act in actions:
            await asyncio.sleep(2)
            act = act[0]
            respondRoom(f"**{act}**", self.room)

        self.sql_commands.delete_dp_actions(self.idGame)