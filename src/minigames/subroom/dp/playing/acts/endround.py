import asyncio
import random

from src.vars import Varlist
from src.sending import respondRoom

class PostRound():
    def __init__(self, idGame, room, playersClasses, team1_classes, team2_classes, team1_dead, team2_dead) -> None:
        self.idGame = idGame
        self.room = room
        self.sql_commands = Varlist.sql_commands
        self.dpGames = Varlist.dpGames
        self.playersClasses = playersClasses
        self.team1_classes = team1_classes
        self.team2_classes = team2_classes
        self.team1_dead = team1_dead
        self.team2_dead = team2_dead

        self.end_game = False
    
    def makeAction(self, action):
        self.sql_commands.insert_dp_action(self.idGame, action)

    def controller(self):
        self.round_final_moves()
        return self.end_game

    def rollPlus(self, maxRoll, add):
        roll = random.randint(1, maxRoll)
        roll += add
        self.makeAction(f"Roll 1 de {maxRoll} + {add}: {roll}")
        return roll
    
    def check_death(self, player):
        player_class = self.players_classes[player]
        if player_class.hp <= 0:
            player_class.hp = 0
            if player not in self.players_dead:
                self.players_classes.pop(player)
                if player in self.team1_classes: 
                    self.team1_classes.pop(player)
                    self.team1_dead[player] = player_class
                else: 
                    self.team2_classes.pop(player)
                    self.team2_dead[player] = player_class
                player_class.positive_effects.clear()
                player_class.negative_effects.clear()
                player_class.other_effects.clear()
                player_class.gold = 0
                player_class.cooldowns.clear()
            return True
        else:
            return
    
    def check_end(self):
        if not (self.team1_classes) or not (self.team2_classes):
            self.end_game = True
            return True
        return

    def round_final_moves(self):
        for player in self.playersClasses:
            player_class = self.playersClasses[player]
            if player in self.team1_classes:
                playerTeam = self.team1_classes
                enemyTeam = self.team2_classes
            else:
                playerTeam = self.team2_classes
                enemyTeam = self.team1_classes
            
            if "IMUNIDADE" in player_class.other_effects:
                rounds = player_class.other_effects["IMUNIDADE"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.other_effects.pop("IMUNIDADE")
                else:
                    player_class.other_effects["IMUNIDADE"]["ROUNDS"] = rounds
            
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
            
            if "ENVENENADO" in player_class.negative_effects:
                self.makeAction(f"{player} está envenenado, pode tomar de 5 a 9 de dano")
                roll = self.rollPlus(5, 4)
                player_class.hp -= roll
                self.makeAction(f"{player} tomou {roll} de dano")
                if self.check_death(player):
                    continue
                if self.check_end():
                    break
                rounds = player_class.other_effects["ENVENENADO"]["ROUNDS"]
                rounds -= 1
                if rounds == 0:
                    player_class.other_effects.pop("ENVENENADO")
                else:
                    player_class.other_effects["ENVENENADO"]["ROUNDS"] = rounds

            if "QUEIMADO" in player_class.negative_effects:
                self.makeAction(f"{player} tomou 7 de dano por conta da queimadura")
                player_class.hp -= 7
                if self.check_death(player):
                    continue
                if self.check_end():
                    break

    async def writing_actions(self):
        actions = self.sql_commands.select_dp_actions(self.idGame)
        for act in actions:
            act = act[0]
            time_sleep = len(act) / 5.5
            respondRoom(f"**{act}**", self.room)
            await asyncio.sleep(time_sleep)
        
        self.final_code_func()

    def final_code_func(self):
        final_code = "Equipe 1:\n"
        for player in self.team1_classes:
            player_class = self.playersClasses[player]
            hp = player_class.hp
            hp_original = player_class.__class__().hp
            negative_effects = player_class.negative_effects
            postiive_effects = player_class.positive_effects
            gold = player_class.gold
            cooldowns = player_class.cooldowns
            final_code += f"{player} | {player_class.name}\nHP:{hp}/{hp_original}\nEfeitos Negativos: {list(negative_effects)}\nEfeitos Positivos: {list(postiive_effects)}\n"
            if player_class.name == "Gambler":
                final_code += f"Ouro: {gold}"
            final_code += f"{cooldowns}\n\n"
        for player in self.team1_dead:
            player_class = self.team1_dead[player]
            final_code += f"{player} | {player_class.name}\nMORTO\n\n"
        final_code += "\nEquipe 2:\n"
        for player in self.team2_classes:
            player_class = self.playersClasses[player]
            hp = player_class.hp
            hp_original = player_class.__class__().hp
            negative_effects = player_class.negative_effects
            postiive_effects = player_class.positive_effects
            gold = player_class.gold
            cooldowns = player_class.cooldowns
            final_code += f"{player} | {player_class.name}\nHP:{hp}/{hp_original}\nEfeitos Negativos: {list(negative_effects)}\nEfeitos Positivos: {list(postiive_effects)}\n"
            if player_class.name == "Gambler":
                final_code += f"Ouro: {gold}"
            final_code += f"{cooldowns}\n\n"
        for player in self.team2_dead:
            player_class = self.team1_dead[player]
            final_code += f"{player} | {player_class.name}\nMORTO\n\n"

        respondRoom(f"!code {final_code}", self.room)

        self.sql_commands.delete_dp_actions(self.idGame)