import random

from src.vars import Varlist
from src.sending import *
from src.leaderboard.commands import *
from src.minigames.subroom.dp.data.classes.classes import classes_dict
from src.minigames.subroom.dp.playing.acts.calc import ActsCalculator
from src.minigames.subroom.dp.playing.acts.endround import PostRound

class GameCommands():
    def __init__(self, host):
        self.host = host
        self.room = Varlist.room
        self.players = []
        self.team1 = []
        self.team2 = []
        self.playersClasses = {}
        self.team1_classes = {}
        self.team2_classes = {}

        self.writings = Varlist.writing

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
        self.playersClasses[player] = player_class
        if player in self.team1:
            self.team1_classes[player] = player_class
        else:
            self.team2_classes[player] = player_class
        respondPM(self.senderID, "Classe atribuída!")

    def act(self):
        player = self.commandParams[1].strip()
        act = self.commandParams[2].strip()
        targets = ""
        if len(self.commandParams) > 3:
            targets = self.commandParams[3:]
        print(self.playersClasses)
        act: ActsCalculator = ActsCalculator(player, act, targets, self.playersClasses)
        call_command(act.act_calc())

    def actsconfirm(self):
        postRoundInstance: PostRound = PostRound()
        self.writings[self.room] = postRoundInstance