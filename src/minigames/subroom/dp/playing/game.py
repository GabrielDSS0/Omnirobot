import random
import threading
import json
import inspect

from psclient import toID

from config import prefix

from data.dp.classes.classes import classes_dict
from data.dp.abilities.abilities import abilities_dict

from src.vars import Varlist
from src.sending import *
from src.misc_commands.commands import *
from src.minigames.subroom.dp.playing.acts.calc import ActsCalculator
from src.minigames.subroom.dp.playing.acts.endround import PostRound

class GameCommands():
    def __init__(self, host, groupchat_name_complete):
        self.idGame: int
        self.round: int = 0
        self.host = host
        self.groupchat_name_complete = groupchat_name_complete
        self.room = Varlist.room
        self.msgType = Varlist.msgType
        self.websocket = Varlist.websocket
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

        self.started = False
        self.end_game = False

        self.sql_commands = Varlist.sql_commands
        self.dpGames = Varlist.dpGames

    async def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.commandParams = Varlist.commandParams
        if self.groupchat_name_complete in self.commandParams:
            self.commandParams.remove(self.groupchat_name_complete)
        func = getattr(inst, name_func)
        isAsync = inspect.iscoroutinefunction(func)
        if not isAsync:
            func()
        else:
            await func()

    def threading_timer(self, time, function, args=[]):
        thread_timer = threading.Timer(time, function, args=args)
        thread_timer.start()

    async def query(self, type, params):
        call_command(self.websocket.send(f"|/query {type} {params}"))
        response = str(await self.websocket.recv()).split("|")
        if len(response) > 2:
            while response[1] != "queryresponse" and response[2] != type:
                response = str(await self.websocket.recv()).split("|")

            return response

    def startdp(self):
        if self.started:
            return respondPM(self.senderID, "O jogo já começou!")
        self.sql_commands.insert_dp_game(self.room)
        self.idGame = self.sql_commands.select_dp_games()[-1][0]
        self.started = True
        respondRoom("O jogo de Dungeons & Pokémon foi iniciado! Para definir os jogadores, o host do jogo terá que digitar @defplayers [jogadores] aqui no chat, e eu mesmo irei sortear os jogadores por equipe.", self.room)
        respondRoom("Post oficial do fórum de Dungeons & Pokémon, caso tenha dúvidas em relação ao jogo: https://pspt.boards.net/thread/701/projeto-dungeons-pokemon", self.room)

    def defplayers(self):
        if not self.started:
            return respondPM(self.senderID, "Não há um jogo de Dungeons & Pokémon ocorrendo agora.")

        players = self.commandParams

        for player in players:
            player = player.strip()
            self.players.append(player)

        if not self.players:
            self.players.clear()
            return respond(self.msgType, f"Uso do comando: {prefix}defplayers [jogadores separados por vírgula]", self.senderID, self.room)
        if (len(players) % 2) != 0:
            self.players.clear()
            return respond(self.msgType, f"O número de jogadores deve ser par.", self.senderID, self.room)

        half = int(len(self.players) / 2)

        random.shuffle(self.players)
        self.team1 = self.players[half:]
        self.team2 = self.players[:half]

        respondRoom(f"Equipe 1: {', '.join(self.team1)} \n Equipe 2: {', '.join(self.team2)}", self.room)
        self.priorityTeam = random.choice([self.team1, self.team2])
        team = "Equipe 1" if self.priorityTeam == self.team1 else "Equipe 2"
        respondRoom(f"A equipe que terá prioridade de habilidades no primeiro round será a: {team}", self.room)
        
        self.threading_timer(2, respondRoom, ["Equipes definidas! Peço agora ao host para que defina as classes dos respectivos jogadores com o comando @defclass em minha PM.", self.room])
    
    def defclass(self):
        if not self.started:
            return respondPM(self.senderID, "Não há um jogo de Dungeons & Pokémon ocorrendo agora.")
        if not self.players:
            return respondPM(self.senderID, f"Os jogadores ainda não foram definidos.")

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
            code = "Classes:\n"
            for player in self.playersClasses:
                player_class_name = self.playersClasses[player].name
                code += f"{player}: {player_class_name}\n"

            respondPM(self.senderID, f"!code {code}")
            self.threading_timer(3, respondPM, [self.senderID, "Estas são as classes que deseja? Caso sim, digite @confirmclass para confirmar."])

    def confirmclass(self):
        if not self.started:
            return respondPM(self.senderID, "Não há um jogo de Dungeons & Pokémon ocorrendo agora.")
        if not self.players:
            return respondPM(self.senderID, f"Os jogadores ainda não foram definidos.")
        if not (len(list(self.playersClasses)) == len(self.players)):
            return respondPM(self.senderID, f"As classes ainda não foram todas definidas.")
        
        if len(list(self.playersClasses)) == len(self.players):
            respondPM(self.senderID, "Todas as classes estão definidas!")
            for player in self.playersClasses:
                player_class = self.playersClasses[player]
                special_ability = player_class.default_abilities[-1]
                special_ability_cooldown = abilities_dict[special_ability].cooldown
                if not (special_ability_cooldown == 0):
                    player_class.cooldowns[special_ability] = special_ability_cooldown
            self.round = 1
            self.verify_spirit_trapper()

            code = "Classes:\n"
            for player in self.playersClasses:
                player_class_name = self.playersClasses[player].name
                code += f"{player}: {player_class_name}\n"
            respondRoom(f"!code {code}", self.room)

    def act(self):
        if not self.started:
            return respondPM(self.senderID, "Não há um jogo de Dungeons & Pokémon ocorrendo agora.")
        if not self.players:
            return respondPM(self.senderID, f"Os jogadores ainda não foram definidos.")
        if not (len(set(self.playersClasses).union(set(self.playersDead))) == len(self.players)):
            return respondPM(self.senderID, f"As classes ainda não foram todas definidas")

        player = self.commandParams[0].strip()
        if not (player in self.playersClasses):
            return respondPM(self.senderID, f"{player} não está na partida.")
        
        player_class = self.playersClasses[player]
        act_name = self.commandParams[1].strip()
        if not (act_name in abilities_dict):
            return respondPM(self.senderID, f"{act_name} não é uma habilidade válida.")

        targets = []
        if len(self.commandParams) > 2:
            targets = self.commandParams[2:]
        if act_name in player_class.cooldowns:
            return respondPM(self.senderID, "Essa habilidade está em cooldown.")
        act: ActsCalculator = ActsCalculator(self.idGame, player, act_name, targets, self.playersClasses, self.team1_classes, self.team2_classes, self.playersDead,
                                     self.team1_dead, self.team2_dead, self.round)
        if targets:
            respondPM(self.senderID, f"{player} utilizará a habilidade {act_name}. Alvos: {', '.join(targets)}")
        else:
            respondPM(self.senderID, f"{player} utilizará a habilidade {act_name}.")
        self.abilities_order[player] = act
    
    def cancelact(self):
        if not self.abilities_order:
            return respondPM(self.senderID, "Não há ações a serem canceladas.")

        self.abilities_order.pop(list(self.abilities_order)[-1])
        return respondPM(self.senderID, "A última ação foi removida!")

    def actsconfirm(self):
        if not self.started:
            return respondPM(self.senderID, "Não há um jogo de Dungeons & Pokémon ocorrendo agora.")
        if not self.players:
            return respondPM(self.senderID, f"Os jogadores ainda não foram definidos.")
        if not (len(set(self.playersClasses).union(set(self.playersDead))) == len(self.players)):
            return respondPM(self.senderID, f"As classes ainda não foram todas definidas")
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

        postRoundInstance: PostRound = PostRound(self.idGame, self.room, self.playersClasses, self.team1_classes, self.team2_classes, self.playersDead, self.team1_dead, self.team2_dead)
        if not (self.end_game):
            self.end_game = postRoundInstance.controller()
        if self.end_game:
            self.end_game_func()
        else:
            self.abilities_order.clear()
            self.round += 1
            self.startRound = False
            self.priorityTeam = self.team1 if self.priorityTeam == (self.team2) else self.team2
        asyncio.create_task(postRoundInstance.writing_actions())

    def verify_spirit_trapper(self):
        for player in self.playersClasses:
            player_class = self.playersClasses[player]
            if player_class.name == "Spirit" and self.round == 1:
                respondPM(self.senderID, f"É necessário anexar um possuído para o Spirit {player}. Digite @spirit [jogador], [possúido]")
            if player_class.name == "Trapper":
                respondPM(self.senderID, f"É necessário plantar uma armadilha de Trapper em um aliado de {player}. Digite @trapper [jogador Trapper], [jogador-armadilha]")

    def spirit(self):
        player_spirit = self.commandParams[0].strip()
        if not (player_spirit in self.playersClasses):
            return respondPM(self.senderID, f"{player_spirit} não está entre os jogadores da partida.")
        player_possessed = self.commandParams[-1].strip()
        if not (player_spirit in self.playersClasses):
            return respondPM(self.senderID, f"{player_possessed} não está entre os jogadores da partida.")
        spirit_class = self.playersClasses[player_spirit]
        possessed_class = self.playersClasses[player_possessed]
        possessed_class.other_effects["POSSUIDO"] = player_spirit
        spirit_class.other_effects["POSSUINDO"]  = player_possessed
        spirit_class.other_effects["IMUNIDADE"] = {"ROUNDS": -1}
        shield_value = 10
        if "ESCUDO" in possessed_class.positive_effects:
            shield_value += possessed_class.positive_effects["ESCUDO"]
        possessed_class.positive_effects["ESCUDO"] = {"VALOR": shield_value, "ROUNDS": 2}
        respondPM(self.senderID, f"{player_possessed} foi possuído por {player_spirit}!")

    def trapper(self):
        target = self.commandParams[1].strip()
        if not (target in self.playersClasses):
            return respondPM(self.senderID, f"{self.senderID} não está dentre os jogadores da partida.")
        target_class = self.playersClasses[target]
        target_class.other_effects["TRAPPER00"] = {"ROUNDS": 1, "VEZES": 2}
        respondPM(self.senderID, f"{target} está com a armadilha!!")

    async def makehost(self):
        if not self.started:
            return respondPM(self.senderID, "Não há jogo de Dungeons & Pokémon nesta subroom atualmente.")

        new_host = self.commandParams[-1]
        new_host_id = toID(new_host)
        if new_host_id in self.dpGames:
            return respond("Este usuário já é um dos hosts dessa sala.")
        response = await self.query("userdetails", f"{new_host}")

        rooms = list((json.loads(response[3])['rooms'].keys()))
        substringRoom = f"{self.groupchat_name_complete}"

        for room in rooms:
            if not (room[0].isalnum()):
                room = room[1:]
            if substringRoom == room:
                respond(self.msgType, f"Novo host: {new_host}", self.senderID, self.groupchat_name_complete)
                instance = self.dpGames[self.host][self.groupchat_name_complete]
                Varlist.dpGames[new_host_id] = {self.groupchat_name_complete: instance}

                if new_host_id in Varlist.hosts_groupchats:
                    groupchats: list = Varlist.hosts_groupchats[new_host_id]
                    groupchats.append(room)
                    Varlist.hosts_groupchats[new_host_id] = groupchats
                else:
                    Varlist.hosts_groupchats[new_host_id] = [self.groupchat_name_complete]
                return True
        return

    def finishdp(self):
        if not self.started:
            return respondPM(self.senderID, "Não há jogo de Dungeons & Pokémon nesta subroom atualmente.")

        respondRoom("O jogo de Dungeons & Pokémon foi encerrado.", self.room)
        self.delete_game()

    def end_game_func(self):
        equipeVencedora = ""
        if not (self.team1_classes):
            equipeVencedora = "equipe 2"
        else:
            equipeVencedora = "equipe 1"
        self.sql_commands.insert_dp_action(self.idGame, f"Acabou!! A {equipeVencedora} venceu a partida!!!!!!")
        
        self.delete_game()

    def delete_game(self):
        dpGames = Varlist.dpGames.copy()
        for host in dpGames:
            rooms = Varlist.hosts_groupchats[host]
            if self.groupchat_name_complete in rooms:
                del Varlist.dpGames[host][self.groupchat_name_complete]
            if not (Varlist.dpGames[host]):
                del Varlist.dpGames[host]