import asyncio
import random

import data.dp.abilities.abilities as abilities
import src.sending as sending
import src.vars as vars


class PostRound:
	def __init__(
		self,
		idGame,
		room,
		playersClasses,
		team1_classes,
		team2_classes,
		players_dead,
		team1_dead,
		team2_dead,
	) -> None:
		self.idGame = idGame
		self.room = room
		self.sql_commands = vars.Varlist.sql_commands
		self.dpGames = vars.Varlist.dpGames
		self.playersClasses = playersClasses
		self.team1_classes = team1_classes
		self.team2_classes = team2_classes
		self.players_dead = players_dead
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

	def check_all(self, player):
		if self.check_end():
			return "END"
		death = self.check_death(player)
		if self.check_end():
			return "END"
		if death:
			return "DEATH"
		return

	def check_death(self, player):
		player_class = self.playersClasses[player]
		if player_class.hp <= 0:
			player_class.hp = 0
			if player not in self.players_dead:
				self.playersClasses.pop(player)
				self.players_dead[player] = player_class
				if player in self.team1_classes:
					self.team1_classes.pop(player)
					self.team1_dead[player] = player_class
				else:
					self.team2_classes.pop(player)
					self.team2_dead[player] = player_class
				if "POSSUIDO" in player_class.other_effects:
					possessor = player_class.other_effects["POSSUIDO"]
					possessor_class = self.playersClasses[possessor]
					possessor_class.other_effects.pop("POSSUINDO")
				if "POSSUINDO" in player_class.other_effects:
					possesssing = player_class.other_effects["POSSUINDO"]
					possessing_class = self.playersClasses[possesssing]
					possessing_class.other_effects.pop("POSSUIDO")
				player_class.positive_effects.clear()
				player_class.negative_effects.clear()
				player_class.other_effects.clear()
				player_class.gold = 0
				player_class.cooldowns.clear()
				self.makeAction(f"{player} foi abatido!!")
			return True
		return

	def check_end(self):
		if not (self.team1_classes) or not (self.team2_classes):
			self.end_game = True
			return True
		return

	def round_final_moves(self):
		players_classes = self.playersClasses.copy()
		for player in players_classes:
			check = self.check_all(player)
			if check == "DEATH":
				continue
			elif check == "END":
				return
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

			if "ESCUDO" in player_class.positive_effects:
				rounds = player_class.positive_effects["ESCUDO"]["ROUNDS"]
				rounds -= 1
				if rounds == 0:
					player_class.positive_effects.pop("ESCUDO")
				else:
					player_class.positive_effects["ESCUDO"]["ROUNDS"] = rounds

			if "PROTEGIDO" in player_class.positive_effects:
				rounds = player_class.positive_effects["PROTEGIDO"]["ROUNDS"]
				rounds -= 1
				if rounds == 0:
					player_class.positive_effects.pop("PROTEGIDO")
				else:
					player_class.positive_effects["PROTEGIDO"]["ROUNDS"] = (
						rounds
					)

			if "FORTALECIDO" in player_class.positive_effects:
				rounds = player_class.positive_effects["FORTALECIDO"]["ROUNDS"]
				rounds -= 1
				if rounds == 0:
					player_class.positive_effects.pop("FORTALECIDO")
				else:
					player_class.positive_effects["FORTALECIDO"]["ROUNDS"] = (
						rounds
					)

			if "ROUBOVIDA" in player_class.positive_effects:
				rounds = player_class.positive_effects["ROUBOVIDA"]["ROUNDS"]
				rounds -= 1
				if rounds == 0:
					player_class.positive_effects.pop("ROUBOVIDA")
				else:
					player_class.positive_effects["ROUBOVIDA"]["ROUNDS"] = (
						rounds
					)

			if "VULNERAVEL" in player_class.negative_effects:
				rounds = player_class.negative_effects["VULNERAVEL"]["ROUNDS"]
				rounds -= 1
				if rounds == 0:
					player_class.negative_effects.pop("VULNERAVEL")
				else:
					player_class.negative_effects["VULNERAVEL"]["ROUNDS"] = (
						rounds
					)

			if "ENFRAQUECIDO" in player_class.negative_effects:
				rounds = player_class.negative_effects["ENFRAQUECIDO"][
					"ROUNDS"
				]
				rounds -= 1
				if rounds == 0:
					player_class.negative_effects.pop("ENFRAQUECIDO")
				else:
					player_class.negative_effects["ENFRAQUECIDO"]["ROUNDS"] = (
						rounds
					)

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
					player_class.dr = player_class.other_effects["NINJA2"][
						"DR_ORIG"
					]
					player_class.other_effects.pop("NINJA2")
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
				self.makeAction(
					f"{player} está envenenado, pode tomar de 5 a 9 de dano"
				)
				roll = self.rollPlus(5, 4)
				player_class.hp -= roll
				self.makeAction(f"{player} tomou {roll} de dano")
				check = self.check_all(player)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				rounds = player_class.negative_effects["ENVENENADO"]["ROUNDS"]
				rounds -= 1
				if rounds == 0:
					player_class.negative_effects.pop("ENVENENADO")
				else:
					player_class.negative_effects["ENVENENADO"]["ROUNDS"] = (
						rounds
					)

			if "QUEIMADO" in player_class.negative_effects:
				self.makeAction(
					f"{player} tomou 7 de dano por conta da queimadura"
				)
				player_class.hp -= 7
				check = self.check_all(player)
				if check == "DEATH":
					continue
				elif check == "END":
					return

			cooldowns = player_class.cooldowns.copy()
			for ability in cooldowns:
				ability_cooldown = player_class.cooldowns[ability]
				if ability_cooldown == 0:
					player_class.cooldowns.pop(ability)

	async def writing_actions(self):
		actions = self.sql_commands.select_dp_action(self.idGame)
		for act in actions:
			act = act[0]
			time_sleep = len(act) / 6.7
			sending.respondRoom(f"**{act}**", self.room)
			await asyncio.sleep(time_sleep)

		self.final_code_func()

	def alive_players_final_code(self, team, final_code):
		for player in team:
			player_class = self.playersClasses[player]
			hp = player_class.hp
			hp_original = player_class.__class__().hp
			negative_effects = player_class.negative_effects

			format_negative = []
			for negative in negative_effects:
				if negative == "ATORDOADO":
					format_negative.append("Atordoado")
				elif negative == "PROVOCADO":
					taunter = negative_effects[negative]["JOGADOR"]
					format_negative.append(f"Provocado por {taunter}")
				elif negative == "QUEIMADO":
					format_negative.append("Queimado")
				elif negative == "ENVENENADO":
					format_negative.append("Envenenado")
				elif negative == "VULNERAVEL":
					value = negative_effects[negative]["VALOR"]
					format_negative.append(f"Vulnerável: {value}%")
				elif negative == "ENFRAQUECIDO":
					value = negative_effects[negative]["VALOR"]
					format_negative.append(f"Enfraquecido: {value}%")

			format_negative = ", ".join(format_negative)

			positive_effects = player_class.positive_effects
			format_positive = []

			for positive in positive_effects:
				if positive == "ESCUDO":
					value = positive_effects[positive]["VALOR"]
					format_positive.append(f"Escudo: {value}")
				elif positive == "PROTEGIDO":
					value = positive_effects[positive]["VALOR"]
					format_positive.append(f"Protegido: {value}%")
				elif positive == "FORTALECIDO":
					value = positive_effects[positive]["VALOR"]
					format_positive.append(f"Fortalecido: {value}%")
				elif positive == "ROUBOVIDA":
					value = positive_effects[positive]["VALOR"]
					format_positive.append(f"Roubo de vida: {value}%")

			format_positive = ", ".join(format_positive)

			other_effects = player_class.other_effects
			possession = []

			for other in other_effects:
				if other == "POSSUIDO":
					possessor = other_effects[other]
					possession.append(f"Possuído por: {possessor}")
				elif other == "POSSUINDO":
					possessing = other_effects[other]
					possession.append(f"Possuindo {possessing}")

			possession = ", ".join(possession)

			gold = player_class.gold
			cooldowns = player_class.cooldowns

			format_cooldowns = []
			for ability in cooldowns:
				ability_class = abilities.abilities_dict[ability]
				ability_name = ability_class.type_name
				rounds = cooldowns[ability]
				format_cooldowns.append(f"{ability_name}: {rounds} rounds")

			format_cooldowns = ", ".join(format_cooldowns)

			final_code += f"{player} | {player_class.name}\nHP:{hp}/{hp_original}\nEfeitos Negativos: {format_negative}\nEfeitos Positivos: {format_positive}\n"

			if possession:
				final_code += f"{possession}\n"

			if player_class.name == "Gambler":
				final_code += f"Ouro: {gold}\n"
			final_code += f"Cooldowns:\n{format_cooldowns}\n\n"
		return final_code

	def final_code_func(self):
		final_code = "Equipe 1:\n"
		final_code = self.alive_players_final_code(
			self.team1_classes, final_code
		)

		for player in self.team1_dead:
			player_class = self.team1_dead[player]
			final_code += f"{player} | {player_class.name}\n0 HP\n\n"

		final_code += "\nEquipe 2:\n"
		final_code = self.alive_players_final_code(
			self.team2_classes, final_code
		)

		for player in self.team2_dead:
			player_class = self.team2_dead[player]
			final_code += f"{player} | {player_class.name}\n0 HP\n\n"

		sending.respondRoom(f"!code {final_code}", self.room)

		self.sql_commands.delete_dp_action(self.idGame)

		if self.end_game:
			self.sql_commands.delete_dp_game(self.idGame)
