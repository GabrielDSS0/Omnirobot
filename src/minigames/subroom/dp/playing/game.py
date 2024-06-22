import random

from config import username, prefix
from src.vars import Varlist
from src.sending import *
from src.leaderboard.commands import *

class GameCommands():
    def __init__(self, host):
        self.host = host
        self.room = Varlist.room
        self.players = []

        self.sql_commands = Varlist.sql_commands
        self.questions = Varlist.questions

    def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.commandParams = Varlist.commandParams
        func = getattr(inst, name_func)
        func()

    def start(self):
        respondRoom("O jogo de Dungeons & Pokémon foi iniciado! Para definir os jogadores, o host do jogo terá que digitar @defplayers [jogadores] aqui no chat, e eu mesmo irei sortear os jogadores por equipe.", self.room)

    def defplayers(self):
        players = self.commandParams
        for player in players:
            player = player.strip()
            self.players.append(player)


    def defclass(self):
        pass

    def act(self):
        pass

    def actsconfirm(self):
        pass