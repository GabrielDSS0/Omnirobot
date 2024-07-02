import random

from src.vars import Varlist
from src.sending import *
from src.leaderboard.commands import *
from src.minigames.subroom.dp.data.classes.classes import classes_dict

class GameCommands():
    def __init__(self, host):
        self.host = host
        self.room = Varlist.room
        self.players = []
        self.team1 = []
        self.team2 = []
        self.playerClass = {}

        self.sql_commands = Varlist.sql_commands
        self.dpGames = Varlist.dpGames

    def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.commandParams = Varlist.commandParams
        func = getattr(inst, name_func)
        func()

    def startdp(self):
        respondRoom("O jogo de Dungeons & Pokémon foi iniciado! Para definir os jogadores, o host do jogo terá que digitar @defplayers [jogadores] aqui no chat, e eu mesmo irei sortear os jogadores por equipe.", self.room)

    def defplayers(self):
        players = self.commandParams
        for player in players:
            player = player.strip()
            self.players.append(player)

        half = int(len(self.players) / 2)

        random.shuffle(self.players)
        self.team1 = self.players[half:]
        self.team2 = self.players[:half]

        respondRoom(f"Equipe 1: {', '.join(self.team1)} \n Equipe 2: {', '.join(self.team2)}", self.room)
        respondRoom(f"Equipes definidas! Peço agora ao host para que defina as classes dos respectivos jogadores com o comando @defclass em minha PM.", self.room)
    
    def defclass(self):
        player = self.commandParams[1].strip()
        player_class = self.commandParams[-1].strip()
        player_class = classes_dict[player_class]()
        self.playerClass[player] = player_class
        respondPM(self.senderID, "Classe atribuída!")

    def act(self):
        player = self.commandParams[1].strip()
        act = self.commandParams[2].strip()
        targets = ""
        if len(self.commandParams) > 3:
            targets = self.commandParams[3:]

    def actsconfirm(self):
        pass