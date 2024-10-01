import random

from data.dp.classes.classes import classes_dict

from src.vars import Varlist
from src.sending import *
from src.leaderboard.commands import *
from src.minigames.subroom.dp.playing.acts.startround import StartRound
from src.minigames.subroom.dp.playing.acts.calc import ActsCalculator
from src.minigames.subroom.dp.playing.acts.endround import PostRound

class GameCommands():
    def __init__(self, host):
        self.idGame: int
        self.round: int = 0
        self.host = host
        self.room = Varlist.room
        self.players = []
        self.team1 = []
        self.team2 = []
        self.priorityTeam = []
        self.playersClasses = {}
        self.team1_classes = {}
        self.team2_classes = {}
        self.playersDead = {}
        self.team1_dead = {}
        self.team2_dead = {}
        self.abilities_order = {}
        self.startRound = False

        self.sql_commands = Varlist.sql_commands
        self.dpGames = Varlist.dpGames

    def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.commandParams = Varlist.commandParams
        func = getattr(inst, name_func)
        func()

    async def asyncio_sleep_func(self, time):
        await asyncio.sleep(time)

    def startdp(self):
        self.sql_commands.insert_dp_game(self.room, self.host)
        self.idGame = self.sql_commands.select_dp_games()[-1][0]
        respondRoom("O jogo de Dungeons & Pokémon foi iniciado! Para definir os jogadores, o host do jogo terá que digitar @defplayers [jogadores] aqui no chat, e eu mesmo irei sortear os jogadores por equipe.", self.room)
        respondRoom("Post oficial do fórum de Dungeons & Pokémon, caso tenha dúvidas em relação ao jogo: https://pspt.boards.net/thread/701/projeto-dungeons-pokemon", self.room)

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
        self.priorityTeam = random.choice([self.team1, self.team2])
        team = "Equipe 1" if self.priorityTeam == self.team1 else "Equipe 2"
        respondRoom(f"A equipe que terá prioridade de habilidades no primeiro round será a: {team}", self.room)
        
        asyncio.create_task(self.asyncio_sleep_func(2))
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

        if len(list(self.playersClasses)) == len(self.players):
            respondPM(self.senderID, "Todas as classes foram atribuídas!")

    def act(self):
        player = self.commandParams[1].strip()
        act = self.commandParams[2].strip()
        targets = ""
        if len(self.commandParams) > 3:
            targets = self.commandParams[3:]
        act: ActsCalculator = ActsCalculator(self.idGame, player, act, targets, self.playersClasses, self.team1_classes, self.team2_classes)
        self.abilities_order[player] = act

    def actsconfirm(self):
        if self.startRound:
            start_round: StartRound = StartRound()
            start_round.actionsRound()
        abilitiesPriority = {}
        for player in self.abilities_order:
            act = self.abilities_order[player]
            ability = act.ability_class
            abilityPriority = ability.priority
            if player in self.priorityTeam:
                abilityPriority += 0.5
            abilitiesPriority[act] = abilityPriority
        actsSequence = dict(sorted(abilitiesPriority.items(), key=lambda item: item[1], reverse=True))
        for act in actsSequence:
            self.playersClasses, self.playersDead, self.team1_dead, self.team2_dead = act.controller()
        postRoundInstance: PostRound = PostRound(self.idGame, self.room, self.playersClasses, self.team1_classes, self.team2_classes)
        postRoundInstance.controller()
        asyncio.create_task(postRoundInstance.writing_actions())
        self.abilities_order.clear()
        self.round += 1
            
    def spirit(self):
        player_spirit = self.commandParams[1].strip()
        player_possessed = self.commandParams[-1].strip()
        spirit_class = self.playersClasses[player_spirit]
        possessed_class = self.playersClasses[player_possessed]
        spirit_class.other_effects["POSSUINDO"]  = player_possessed
        shield_value = 10
        if "ESCUDO" in possessed_class.positive_effects:
            shield_value += possessed_class.positive_effects["ESCUDO"]
        possessed_class.positive_effects["ESCUDO"] = {"VALOR": shield_value, "ROUNDS": 2}


    def trapper(self):
        player = self.commandParams[1].strip()
        target = self.commandParams[2].strip()
        target_class = self.playersClasses[target]
        target_class.other_effects["TRAPPER00"] = {"ROUNDS": 1}