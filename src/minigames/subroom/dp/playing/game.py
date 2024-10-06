import random

from data.dp.classes.classes import classes_dict
from data.dp.abilities.abilities import abilities_dict

from src.vars import Varlist
from src.sending import *
from src.leaderboard.commands import *
from src.minigames.subroom.dp.playing.acts.calc import ActsCalculator
from src.minigames.subroom.dp.playing.acts.endround import PostRound

class GameCommands():
    def __init__(self, host, room_simplified):
        self.idGame: int
        self.round: int = 0
        self.host = host
        self.room_simplified = room_simplified
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

        self.end_game = False

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
            for player in self.playersClasses:
                player_class = self.playersClasses[player]
                special_ability = player_class.default_abilities[-1]
                special_ability_cooldown = abilities_dict[special_ability].cooldown
                if not (special_ability_cooldown == 0):
                    player_class.cooldowns[special_ability] = special_ability_cooldown
            self.round = 1
            self.verify_spirit_trapper()
    
    def verify_spirit_trapper(self):
        for player in self.playersClasses:
            player_class = self.playersClasses[player]
            if player_class.name == "Spirit" and self.round == 1:
                respondPM(self.host, f"É necessário anexar um possuído para o Spirit {player}. Digite @spirit [sala], [jogador], [possúido]")
            if player_class.name == "Trapper":
                respondPM(self.host, f"É necessário plantar uma armadilha de Trapper em um aliado de {player}. Digite @trapper [sala], [jogador Trapper], [jogador-armadilha]")

    def act(self):
        player = self.commandParams[1].strip()
        player_class = self.playersClasses[player]
        act_name = self.commandParams[2].strip()
        targets = ""
        if len(self.commandParams) > 3:
            targets = self.commandParams[3:]
        if act_name in player_class.cooldowns:
            return respondPM(self.senderID, "Essa habilidade está em cooldown.")
        act: ActsCalculator = ActsCalculator(self.idGame, player, act_name, targets, self.playersClasses, self.team1_classes, self.team2_classes, self.playersDead,
                                     self.team1_dead, self.team2_dead, self.round)
        if targets:
            respondPM(self.senderID, f"{player} utilizará a habilidade {act_name}. Alvos: {', '.join(targets)}")
        else:
            respondPM(self.senderID, f"{player} utilizará a habilidade {act_name}.")
        self.abilities_order[player] = act

    def actsconfirm(self):
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
            if not (self.startRound):
                self.startRound = True
                act.startRound()
            self.playersClasses, self.team1_classes, self.team2_classes, self.playersDead, self.team1_dead, self.team2_dead, self.end_game = act.controller()
            if self.end_game:
                break
        postRoundInstance: PostRound = PostRound(self.idGame, self.room, self.playersClasses, self.team1_classes, self.team2_classes, self.team1_dead, self.team2_dead)
        if not (self.end_game):
            self.end_game = postRoundInstance.controller()
        asyncio.create_task(postRoundInstance.writing_actions())
        if self.end_game:
            self.end_game_func()
            return
        self.abilities_order.clear()
        self.round += 1
        self.startRound = False
        self.verify_spirit_trapper()

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
        target = self.commandParams[2].strip()
        target_class = self.playersClasses[target]
        target_class.other_effects["TRAPPER00"] = {"ROUNDS": 1}
    
    def end_game_func(self):
        equipeVencedora = ""
        if not (self.team1_classes):
            equipeVencedora = "equipe 2"
        else:
            equipeVencedora = "equipe 1"
        respondRoom(f"A partida acabou!! A {equipeVencedora} venceu!!", self.room)
        del self.dpGames[self.host][self.room_simplified]
        if not (self.dpGames[self.host]):
            del self.dpGames[self.host]