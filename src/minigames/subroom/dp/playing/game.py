import random
import threading

from psclient import toID

from data.dp.classes.classes import classes_dict
from data.dp.abilities.abilities import abilities_dict

from src.vars import Varlist
from src.sending import *
from src.leaderboard.commands import *
from src.minigames.subroom.dp.playing.acts.calc import ActsCalculator
from src.minigames.subroom.dp.playing.acts.endround import PostRound

class GameCommands():
    def __init__(self, host, groupchat_name_complete):
        self.idGame: int
        self.round: int = 0
        self.host = host
        self.groupchat_name_complete = groupchat_name_complete
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
        if self.groupchat_name_complete in self.commandParams:
            self.commandParams.remove(self.groupchat_name_complete)
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
        
        if (len(self.players) % 2) != 0:
            return respondRoom(f"O número de jogadores deve ser par.")

        half = int(len(self.players) / 2)

        random.shuffle(self.players)
        self.team1 = self.players[half:]
        self.team2 = self.players[:half]

        respondRoom(f"Equipe 1: {', '.join(self.team1)} \n Equipe 2: {', '.join(self.team2)}", self.room)
        self.priorityTeam = random.choice([self.team1, self.team2])
        team = "Equipe 1" if self.priorityTeam == self.team1 else "Equipe 2"
        respondRoom(f"A equipe que terá prioridade de habilidades no primeiro round será a: {team}", self.room)
        
        thread_timer = threading.Timer(2, respondRoom, args=["Equipes definidas! Peço agora ao host para que defina as classes dos respectivos jogadores com o comando @defclass em minha PM.", self.room])
        thread_timer.start()
    
    def defclass(self):
        player = self.commandParams[0].strip()
        player_class = toID(self.commandParams[-1].strip())

        if player not in self.players:
            return respondPM(self.senderID, "O usuário indicado não está na sala indicada.")
        if not (player_class in classes_dict):
            return respondPM(self.senderID, "A classe indicada não existe.")

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
        player = self.commandParams[0].strip()
        if not (player in self.playersClasses):
            return respondPM(self.host, f"{player} não está na partida.")
        
        player_class = self.playersClasses[player]
        act_name = self.commandParams[1].strip()
        if not (act_name in abilities_dict):
            return respondPM(self.host, f"{act_name} não é uma habilidade válida.")
        
        targets = []
        if len(self.commandParams) > 2:
            targets = self.commandParams[2:]
        for target in targets:
            if not (target.strip() in self.players):
                return respondPM(self.host, f"{target} não está entre os jogadores da partida.")
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
            print(act)
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
        self.priorityTeam = self.team1 if self.priorityTeam == (self.team2) else self.team2
        self.verify_spirit_trapper()

    def spirit(self):
        player_spirit = self.commandParams[0].strip()
        if not (player_spirit in self.playersClasses):
            return respondPM(self.host, f"{player_spirit} não está entre os jogadores da partida.")
        player_possessed = self.commandParams[-1].strip()
        if not (player_spirit in self.playersClasses):
            return respondPM(self.host, f"{player_possessed} não está entre os jogadores da partida.")
        spirit_class = self.playersClasses[player_spirit]
        possessed_class = self.playersClasses[player_possessed]
        spirit_class.other_effects["POSSUINDO"]  = player_possessed
        spirit_class.other_effects["IMUNIDADE"] = {"ROUNDS": -1}
        shield_value = 10
        if "ESCUDO" in possessed_class.positive_effects:
            shield_value += possessed_class.positive_effects["ESCUDO"]
        possessed_class.positive_effects["ESCUDO"] = {"VALOR": shield_value, "ROUNDS": 2}
        respondPM(self.host, f"{player_possessed} foi possuído por {player_spirit}!")

    def trapper(self):
        target = self.commandParams[1].strip()
        if not (target in self.playersClasses):
            return respondPM(self.host, f"{self.senderID} não está dentre os jogadores da partida.")
        target_class = self.playersClasses[target]
        target_class.other_effects["TRAPPER00"] = {"ROUNDS": 1, "VEZES": 2}
        respondPM(self.host, f"{target} está com a armadilha!!")
    
    def end_game_func(self):
        equipeVencedora = ""
        if not (self.team1_classes):
            equipeVencedora = "equipe 2"
        else:
            equipeVencedora = "equipe 1"
        respondRoom(f"A partida acabou!! A {equipeVencedora} venceu!!", self.room)
        del self.dpGames[self.host][self.groupchat_name_complete]
        if not (self.dpGames[self.host]):
            del self.dpGames[self.host]