import asyncio
import inspect
import json
import random
import threading

from psclient import toID

import config
import data.dp.abilities.abilities as abilities
import data.dp.classes.classes as classes
import src.minigames.subroom.dp.playing.acts.calc as calc
import src.minigames.subroom.dp.playing.acts.endround as endround
import src.sending as sending
import src.vars as vars


class GameCommands:
	def __init__(self, host, groupchat_name_complete):
		self.idGame: int
		self.round: int = 0
		self.host = host
		self.groupchat_name_complete = groupchat_name_complete
		self.room = vars.Varlist.room
		self.msgType = vars.Varlist.msgType
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

		self.sql_commands = vars.Varlist.sql_commands
		self.dpGames = vars.Varlist.dpGames

	async def redirect_command(self, inst, name_func: str):
		self.sender = vars.Varlist.sender
		self.senderID = vars.Varlist.senderID
		self.commandParams = vars.Varlist.commandParams
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

	def startdp(self):
		if self.started:
			return sending.respondPM(self.senderID, "O jogo já começou!")
		self.sql_commands.insert_dp_game(self.room)
		self.idGame = self.sql_commands.select_dp_games()[-1][0]
		self.started = True
		sending.respondRoom(
			"O jogo de Dungeons & Pokémon foi iniciado! Para definir os jogadores, o host do jogo terá que digitar @defplayers [jogadores] aqui no chat, e eu mesmo irei sortear os jogadores por equipe.",
			self.room,
		)
		sending.respondRoom(
			"Post oficial do fórum de Dungeons & Pokémon, caso tenha dúvidas em relação ao jogo: https://pspt.boards.net/thread/701/projeto-dungeons-pokemon",
			self.room,
		)

	def defplayers(self):
		if not self.started:
			return sending.respondPM(
				self.senderID,
				"Não há um jogo de Dungeons & Pokémon ocorrendo agora.",
			)

		players = self.commandParams

		for player in players:
			player = player.strip()
			self.players.append(player)

		if not self.players:
			self.players.clear()
			return sending.respond(
				self.msgType,
				f"Uso do comando: {config.prefix}defplayers [jogadores separados por vírgula]",
				self.senderID,
				self.room,
			)
		if (len(players) % 2) != 0:
			self.players.clear()
			return sending.respond(
				self.msgType,
				"O número de jogadores deve ser par.",
				self.senderID,
				self.room,
			)

		half = int(len(self.players) / 2)

		random.shuffle(self.players)
		self.team1 = self.players[half:]
		self.team2 = self.players[:half]

		sending.respondRoom(
			f"Equipe 1: {', '.join(self.team1)} \n Equipe 2: {', '.join(self.team2)}",
			self.room,
		)
		self.priorityTeam = random.choice([self.team1, self.team2])
		team = "Equipe 1" if self.priorityTeam == self.team1 else "Equipe 2"
		sending.respondRoom(
			f"A equipe que terá prioridade de habilidades no primeiro round será a: {team}",
			self.room,
		)

		self.threading_timer(
			2,
			sending.respondRoom,
			[
				"Equipes definidas! Peço agora ao host para que defina as classes dos respectivos jogadores com o comando @defclass em minha PM.",
				self.room,
			],
		)

	def defclass(self):
		if not self.started:
			return sending.respondPM(
				self.senderID,
				"Não há um jogo de Dungeons & Pokémon ocorrendo agora.",
			)
		if not self.players:
			return sending.respondPM(
				self.senderID, "Os jogadores ainda não foram definidos."
			)

		player = self.commandParams[0].strip()
		player_class = toID(self.commandParams[-1].strip())

		if player not in self.players:
			return sending.respondPM(
				self.senderID, "O usuário indicado não está na sala indicada."
			)
		if player_class not in classes.classes_dict:
			return sending.respondPM(
				self.senderID, "A classe indicada não existe."
			)

		player_class = classes.classes_dict[player_class]()
		self.playersClasses[player] = player_class
		if player in self.team1:
			self.team1_classes[player] = player_class
		else:
			self.team2_classes[player] = player_class
		sending.respondPM(self.senderID, "Classe atribuída!")
		if len(list(self.playersClasses)) == len(self.players):
			sending.respondPM(
				self.senderID, "Todas as classes foram atribuídas!"
			)
			code = "Classes:\n"
			for player in self.playersClasses:
				player_class_name = self.playersClasses[player].name
				code += f"{player}: {player_class_name}\n"

			sending.respondPM(self.senderID, f"!code {code}")
			self.threading_timer(
				3,
				sending.respondPM,
				[
					self.senderID,
					"Estas são as classes que deseja? Caso sim, digite @confirmclass para confirmar.",
				],
			)

	def confirmclass(self):
		if not self.started:
			return sending.respondPM(
				self.senderID,
				"Não há um jogo de Dungeons & Pokémon ocorrendo agora.",
			)
		if not self.players:
			return sending.respondPM(
				self.senderID, "Os jogadores ainda não foram definidos."
			)
		if not (len(list(self.playersClasses)) == len(self.players)):
			return sending.respondPM(
				self.senderID, "As classes ainda não foram todas definidas."
			)

		if len(list(self.playersClasses)) == len(self.players):
			sending.respondPM(
				self.senderID, "Todas as classes estão definidas!"
			)
			for player in self.playersClasses:
				player_class = self.playersClasses[player]
				special_ability = player_class.default_abilities[-1]
				special_ability_cooldown = abilities.abilities_dict[
					special_ability
				].cooldown
				if not (special_ability_cooldown == 0):
					player_class.cooldowns[special_ability] = (
						special_ability_cooldown
					)
			self.round = 1
			self.verify_spirit_trapper()

			code = "Classes:\n"
			for player in self.playersClasses:
				player_class_name = self.playersClasses[player].name
				code += f"{player}: {player_class_name}\n"
			sending.respondRoom(f"!code {code}", self.room)

	def act(self):
		if not self.started:
			return sending.respondPM(
				self.senderID,
				"Não há um jogo de Dungeons & Pokémon ocorrendo agora.",
			)
		if not self.players:
			return sending.respondPM(
				self.senderID, "Os jogadores ainda não foram definidos."
			)
		if not (
			len(set(self.playersClasses).union(set(self.playersDead)))
			== len(self.players)
		):
			return sending.respondPM(
				self.senderID, "As classes ainda não foram todas definidas"
			)

		player = self.commandParams[0].strip()
		if player not in self.playersClasses:
			return sending.respondPM(
				self.senderID, f"{player} não está na partida."
			)

		player_class = self.playersClasses[player]
		act_name = self.commandParams[1].strip()
		if act_name not in abilities.abilities_dict:
			return sending.respondPM(
				self.senderID, f"{act_name} não é uma habilidade válida."
			)

		targets = []
		if len(self.commandParams) > 2:
			targets = self.commandParams[2:]

		expected_targets = abilities.abilities_dict[act_name].expected_targets
		if expected_targets:
			if not (targets):
				return sending.respondPM(
					self.senderID,
					"Deveria haver ao menos um alvo para esta habilidade.",
				)
			if not (len(expected_targets) == len(targets)):
				return sending.respondPM(
					self.senderID,
					"Esta habilidade não está com o número de alvos correto.",
				)
			for enum, expected in enumerate(expected_targets):
				target = targets[enum]

				if expected == "enemyPlayer":
					if not (
						(target in self.team1 and player in self.team2)
						or (target in self.team2 and player in self.team1)
					):
						return sending.respondPM(
							self.senderID, "O alvo deveria ser um inimigo."
						)
				elif expected == "allyPlayer":
					if not (
						(
							target in self.team1_classes
							and player in self.team1_classes
						)
						or (
							target in self.team2_classes
							and player in self.team2_classes
						)
					):
						return sending.respondPM(
							self.senderID, "O alvo deveria ser um aliado"
						)
				elif expected == "ability":
					if target not in abilities.abilities_dict:
						return sending.respondPM(
							self.senderID,
							"O segundo alvo deveria ser uma habilidade.",
						)
				elif expected == "stat":
					if not (
						(target == "atk")
						or (target == "td")
						or (target == "tc")
					):
						return sending.respondPM(
							self.senderID,
							"O stat deve ser: **atk**, **td** ou **tc**.",
						)
				elif expected == "sameTeam":
					if not (
						(target in self.team1 and player in self.team1)
						or (target in self.team2 and player in self.team2)
					):
						return sending.respondPM(
							self.senderID, "O alvo deveria ser um aliado."
						)

		if act_name in player_class.cooldowns:
			return sending.respondPM(
				self.senderID, "Essa habilidade está em cooldown."
			)
		act: calc.ActsCalculator = calc.ActsCalculator(
			self.idGame,
			player,
			act_name,
			targets,
			self.playersClasses,
			self.team1_classes,
			self.team2_classes,
			self.playersDead,
			self.team1_dead,
			self.team2_dead,
			self.round,
		)
		if targets:
			sending.respondPM(
				self.senderID,
				f"{player} utilizará a habilidade {act_name}. Alvos: {', '.join(targets)}",
			)
		else:
			sending.respondPM(
				self.senderID, f"{player} utilizará a habilidade {act_name}."
			)
		self.abilities_order[player] = act

	def cancelact(self):
		if not self.abilities_order:
			return sending.respondPM(
				self.senderID, "Não há ações a serem canceladas."
			)

		self.abilities_order.pop(list(self.abilities_order)[-1])
		return sending.respondPM(self.senderID, "A última ação foi removida!")

	def actsconfirm(self):
		if not self.started:
			return sending.respondPM(
				self.senderID,
				"Não há um jogo de Dungeons & Pokémon ocorrendo agora.",
			)
		if not self.players:
			return sending.respondPM(
				self.senderID, "Os jogadores ainda não foram definidos."
			)
		if (
			not (
				len(set(self.playersClasses).union(set(self.playersDead)))
				== len(self.players)
			)
			or self.round < 1
		):
			return sending.respondPM(
				self.senderID, "As classes ainda não foram todas definidas"
			)

		abilitiesPriority = {}
		for player in self.abilities_order:
			act = self.abilities_order[player]
			ability = act.ability_class
			abilityPriority = ability.priority
			if player in self.priorityTeam:
				abilityPriority += 0.5
			abilitiesPriority[act] = abilityPriority
		actsSequence = dict(
			sorted(
				abilitiesPriority.items(),
				key=lambda item: item[1],
				reverse=True,
			)
		)

		for act in actsSequence:
			if not (self.startRound):
				self.startRound = True
				act.startRound()
			(
				self.playersClasses,
				self.team1_classes,
				self.team2_classes,
				self.playersDead,
				self.team1_dead,
				self.team2_dead,
				self.end_game,
			) = act.controller()
			if self.end_game:
				break

		postRoundInstance: endround.PostRound = endround.PostRound(
			self.idGame,
			self.room,
			self.playersClasses,
			self.team1_classes,
			self.team2_classes,
			self.playersDead,
			self.team1_dead,
			self.team2_dead,
		)
		if not (self.end_game):
			self.end_game = postRoundInstance.controller()
		if self.end_game:
			self.end_game_func()
		else:
			self.abilities_order.clear()
			self.round += 1
			self.startRound = False
			self.priorityTeam = (
				self.team1 if self.priorityTeam == (self.team2) else self.team2
			)
		asyncio.create_task(postRoundInstance.writing_actions())

	def verify_spirit_trapper(self):
		for player in self.playersClasses:
			player_class = self.playersClasses[player]
			if player_class.name == "Spirit" and self.round == 1:
				sending.respondPM(
					self.senderID,
					f"É necessário anexar um possuído para o Spirit {player}. Digite @spirit [jogador], [possúido]",
				)
			if player_class.name == "Trapper":
				sending.respondPM(
					self.senderID,
					f"É necessário plantar uma armadilha de Trapper em um aliado de {player}. Digite @trapper [jogador Trapper], [jogador-armadilha]",
				)

	def spirit(self):
		player_spirit = self.commandParams[0].strip()
		if player_spirit not in self.playersClasses:
			return sending.respondPM(
				self.senderID,
				f"{player_spirit} não está entre os jogadores da partida.",
			)
		player_possessed = self.commandParams[-1].strip()
		if player_spirit not in self.playersClasses:
			return sending.respondPM(
				self.senderID,
				f"{player_possessed} não está entre os jogadores da partida.",
			)
		spirit_class = self.playersClasses[player_spirit]
		possessed_class = self.playersClasses[player_possessed]
		possessed_class.other_effects["POSSUIDO"] = player_spirit
		spirit_class.other_effects["POSSUINDO"] = player_possessed
		spirit_class.other_effects["IMUNIDADE"] = {"ROUNDS": -1}
		shield_value = 10
		if "ESCUDO" in possessed_class.positive_effects:
			shield_value += possessed_class.positive_effects["ESCUDO"]
		possessed_class.positive_effects["ESCUDO"] = {
			"VALOR": shield_value,
			"ROUNDS": 2,
		}
		sending.respondPM(
			self.senderID,
			f"{player_possessed} foi possuído por {player_spirit}!",
		)

	def trapper(self):
		target = self.commandParams[1].strip()
		if target not in self.playersClasses:
			return sending.respondPM(
				self.senderID,
				f"{target} não está dentre os jogadores da partida.",
			)
		target_class = self.playersClasses[target]
		target_class.other_effects["TRAPPER00"] = {"ROUNDS": 1, "VEZES": 2}
		sending.respondPM(self.senderID, f"{target} está com a armadilha!!")

	async def makehost(self):
		if not self.started:
			return sending.respond(
				self.msgType,
				"Não há jogo de Dungeons & Pokémon nesta subroom atualmente.",
				self.senderID,
				self.room,
			)

		new_host = self.commandParams[-1]
		new_host_id = toID(new_host)
		if new_host_id in self.dpGames:
			return sending.respond(
				self.msgType,
				"Este usuário já é um dos hosts dessa sala.",
				self.senderID,
				self.room,
			)
		response = await sending.query("userdetails", f"{new_host}")

		rooms = json.loads(response[3])["rooms"]

		if not rooms:
			return sending.respond(
				self.msgType,
				"Este usuário não está na sala.",
				self.senderID,
				self.room,
			)

		rooms = list(rooms.keys())
		substringRoom = f"{self.groupchat_name_complete}"

		for room in rooms:
			if not (room[0].isalnum()):
				room = room[1:]
			if substringRoom == room:
				sending.respond(
					self.msgType,
					f"Novo host: {new_host}",
					self.senderID,
					self.groupchat_name_complete,
				)
				instance = self.dpGames[self.host][
					self.groupchat_name_complete
				]
				vars.Varlist.dpGames[new_host_id] = {
					self.groupchat_name_complete: instance
				}

				if new_host_id in vars.Varlist.hosts_groupchats:
					groupchats: list = vars.Varlist.hosts_groupchats[
						new_host_id
					]
					groupchats.append(room)
					vars.Varlist.hosts_groupchats[new_host_id] = groupchats
				else:
					vars.Varlist.hosts_groupchats[new_host_id] = [
						self.groupchat_name_complete
					]
				return True
		return

	def finishdp(self):
		if not self.started:
			return sending.respondPM(
				self.senderID,
				"Não há jogo de Dungeons & Pokémon nesta subroom atualmente.",
			)

		sending.respondRoom(
			"O jogo de Dungeons & Pokémon foi encerrado.", self.room
		)
		self.delete_game()

	def end_game_func(self):
		equipeVencedora = ""
		if not (self.team1_classes):
			equipeVencedora = "equipe 2"
		else:
			equipeVencedora = "equipe 1"
		self.sql_commands.insert_dp_action(
			self.idGame, f"Acabou!! A {equipeVencedora} venceu a partida!!!!!!"
		)

		self.delete_game()

	def delete_game(self):
		dpGames = vars.Varlist.dpGames.copy()
		for host in dpGames:
			rooms = vars.Varlist.hosts_groupchats[host]
			if self.groupchat_name_complete in rooms:
				del vars.Varlist.dpGames[host][self.groupchat_name_complete]
			if not (vars.Varlist.dpGames[host]):
				del vars.Varlist.dpGames[host]
