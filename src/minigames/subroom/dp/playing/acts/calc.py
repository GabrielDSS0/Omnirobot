import random

import data.dp.abilities.abilities as abilities
import data.dp.abilities.extra_abilities as extra_abilities
import data.dp.classes.classes as classes
import src.vars as vars


class ActsCalculator:
	def __init__(
		self,
		idGame,
		player,
		ability,
		targets,
		players_classes,
		team1_classes,
		team2_classes,
		players_dead,
		team1_dead,
		team2_dead,
		round,
	) -> None:
		self.idGame = idGame
		self.player = player
		self.ability = ability
		self.targets = targets
		self.team1_classes = team1_classes
		self.team2_classes = team2_classes
		self.players_classes = players_classes
		self.players_dead = players_dead
		self.team1_dead = team1_dead
		self.team2_dead = team2_dead
		self.round = round
		self.damages = {}
		self.damagePerTarget = {}
		self.enemyTeam = {}
		self.playerTeam = {}
		self.originalDodgeRate = {}
		self.sql_commands = vars.Varlist.sql_commands
		self.room = vars.Varlist.room

		self.end_game = False

		self.player_class = self.players_classes[self.player]
		self.ability_class = abilities.abilities_dict[self.ability]

		if self.player in team1_classes:
			self.playerTeam = team1_classes
			self.enemyTeam = team2_classes
		else:
			self.playerTeam = team2_classes
			self.enemyTeam = team1_classes

		self.hpEnemies = {}
		self.hpAllies = {}

		for enemy in self.enemyTeam:
			enemy_class = self.players_classes[enemy]
			self.hpEnemies[enemy] = enemy_class.hp

		for player in self.playerTeam:
			player_class = self.players_classes[player]
			self.hpAllies[player] = player_class.hp

	def makeAction(self, action):
		self.sql_commands.insert_dp_action(self.idGame, action)

	def returnAll(self):
		return (
			self.players_classes,
			self.team1_classes,
			self.team2_classes,
			self.players_dead,
			self.team1_dead,
			self.team2_dead,
			self.end_game,
		)

	def controller(self):
		if not self.check_conditions():
			return self.returnAll()
		self.targets = self.update_targets(self.player, self.targets)
		self.damages, self.damagePerTarget = self.update_damages_and_status(
			self.player, self.ability, self.targets
		)
		self.player_class.cooldowns[self.ability] = self.ability_class.cooldown
		self.ability_calc()
		self.check_end()
		return self.returnAll()

	def check_conditions(self):
		check = self.check_all(self.player)
		if check == "DEATH":
			return
		elif check == "END":
			return

		if "ATORDOADO" in self.player_class.negative_effects:
			self.player_class.negative_effects.pop("ATORDOADO")
			self.makeAction(
				f"{self.player} não utilizará sua habilidade pois está atordoado!"
			)
			return
		if "TRAPPER2" in self.player_class.other_effects:
			ability = self.player_class.other_effects["TRAPPER2"]["ABILITY"]
			if ability == self.ability:
				self.makeAction(
					f"{self.player} não utilizará sua {self.ability_class.type_name}, já que está com o efeito de bloqueio do Trapper!"
				)
				return
		return True

	def update_targets(self, player, targets):
		player_class = self.players_classes[player]
		if "PROVOCADO" in player_class.negative_effects:
			taunter = player_class.negative_effects["PROVOCADO"]["JOGADOR"]
			if taunter in self.players_dead:
				player_class.negative_effects.pop("PROVOCADO")
				return targets
			enemyTeam = (
				self.enemyTeam
				if player not in self.enemyTeam
				else self.playerTeam
			)
			targets_set = set(targets)
			enemies_set = set(enemyTeam)
			intersection = targets_set.intersection(enemies_set)
			if intersection:
				targets = list(targets_set - enemies_set)
				targets.extend([taunter])
				player_class.negative_effects.pop("PROVOCADO")

		return targets

	def update_damages_and_status(self, player, ability, targets, damages={}):
		player_class = self.players_classes[player]
		if not damages:
			damages = (
				abilities.abilities_dict[ability].damages.copy()
				if ability in abilities.abilities_dict
				else extra_abilities.extrabilities_dict[ability].damages.copy()
			)
		damagesPerTarget = {}
		enemyTeam = (
			self.enemyTeam if player not in self.enemyTeam else self.playerTeam
		)

		for damage in damages:
			damage_value = damages[damage]
			if "FORTALECIDO" in player_class.positive_effects:
				value = player_class.positive_effects["FORTALECIDO"]["VALOR"]
				damage_value += damage_value * (value / 100)
			if "ENFRAQUECIDO" in player_class.negative_effects:
				value = player_class.negative_effects["ENFRAQUECIDO"]["VALOR"]
				damage_value -= damage_value * (value / 100)
			damages[damage] = damage_value

		for target in targets:
			if target not in enemyTeam:
				continue
			target_class = self.players_classes[target]

			damagesPerTarget[target] = {}

			for damage in damages:
				damage_value = damages[damage]
				if "PROTEGIDO" in target_class.positive_effects:
					value = target_class.positive_effects["PROTEGIDO"]["VALOR"]
					damage_value -= damage_value * (value / 100)
				if "VULNERAVEL" in target_class.negative_effects:
					value = target_class.negative_effects["VULNERAVEL"][
						"VALOR"
					]
					damage_value += damage_value * (value / 100)
				damagesPerTarget[target][damage] = damage_value

		return damages, damagesPerTarget

	def roll(self, maxRoll):
		roll = random.randint(1, maxRoll)
		self.makeAction(f"Roll 1 de {maxRoll}: {roll}")
		return roll

	def dodge(self, target, player):
		player_class = self.players_classes[player]
		target_class = self.players_classes[target]
		self.makeAction(
			f"{player} pode errar a habilidade que utilizará em {target}!"
		)
		dr = target_class.dr
		if player_class.name == "Archer":
			dr -= 10
		self.makeAction(f"Chance de desvio: {dr}%")

		roll = self.roll(100)
		if roll <= dr:
			self.makeAction("Desviou!!")
			if target_class.name == "Ninja":
				self.makeAction(
					f"Como {target} é um Ninja {player} levará 7 de dano!"
				)
				damage = 7
				self.make_default_damage(player, damage, target)
			elif target_class.name == "Gambler":
				self.makeAction(f"{target} ganhará 5 de ouro pelo desvio.")
				target_class.gold += 5
			return True

		if target_class.name == "Gambler":
			self.makeAction(
				f"{target} não desviou, mas como ele é um Gambler ele tem uma chance a mais"
			)
			roll = self.roll(100)
			if roll <= dr:
				self.makeAction("Desviou!!")
				self.makeAction(f"{target} ganhará 5 de ouro pelo desvio.")
				target_class.gold += 5
				return True

		self.makeAction(f"{target} não desviou")
		return

	def critical(self, cr, player):
		self.makeAction(f"{player} pode causar dano crítico!!")
		self.makeAction(f"Chance de crítico: {cr}%")
		player_class = self.players_classes[player]
		roll = self.roll(100)
		if roll <= cr:
			self.makeAction("Crítico!!!")
			if player_class.name == "Gambler":
				self.makeAction(f"{player} ganhará 5 de ouro pelo crítico.")
				player_class.gold += 5
			return True

		if player_class.name == "Gambler":
			self.makeAction(
				f"{player} não causou crítico, mas como é um Gambler ele tem mais uma chance"
			)
			roll = self.roll(100)
			if roll <= cr:
				self.makeAction("Crítico!!!")
				if player_class.name == "Gambler":
					self.makeAction(
						f"{player} ganhará 5 de ouro pelo crítico."
					)
					player_class.gold += 5
				return True

		self.makeAction("Nada de crítico.")
		return

	def check_all(self, player):
		if self.check_end():
			return "END"
		death = self.check_death(player)
		if self.check_end():
			return "END"
		if death:
			return "DEATH"
		elif self.check_immunity(player):
			return "IMMUNITY"
		return

	def check_death(self, player):
		if player in self.players_classes:
			player_class = self.players_classes[player]
		elif player in self.players_dead:
			return True
		else:
			return
		if player_class.hp <= 0:
			player_class.hp = 0
			if player not in self.players_dead:
				self.players_classes.pop(player)
				self.players_dead[player] = player_class
				if player in self.team1_classes:
					self.team1_classes.pop(player)
					self.team1_dead[player] = player_class
				else:
					self.team2_classes.pop(player)
					self.team2_dead[player] = player_class
				if "POSSUIDO" in player_class.other_effects:
					possessor = player_class.other_effects["POSSUIDO"]
					possessor_class = self.players_classes[possessor]
					possessor_class.other_effects.pop("POSSUINDO")
				if "POSSUINDO" in player_class.other_effects:
					possesssing = player_class.other_effects["POSSUINDO"]
					possessing_class = self.players_classes[possesssing]
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

	def check_immunity(self, player):
		player_class = self.players_classes[player]
		if "IMUNIDADE" in player_class.other_effects:
			return True
		return

	def check_trapper3(self, team):
		trap_hp = 0
		for player in team:
			player_class = self.players_classes[player]
			trap_hp += player_class.other_effects["TRAPPER3"]["VALOR"]
		difference = 20 - ((20 * len(team)) - trap_hp)
		return difference

	def bard_passive(self, team, player_target):
		for player in team:
			player_class = team[player]
			if player_class.name == "Bard":
				player_target_class = team[player_target]
				shield = "ESCUDO" in player_target_class.positive_effects
				if shield:
					shield_value = player_target_class.positive_effects[
						"ESCUDO"
					]["VALOR"]
					shield_value += 3
				else:
					shield_value = 3
				self.makeAction(
					f"{player_target} ganhará mais 3 de escudo já que {player} é um Bard!!"
				)
				player_target_class.positive_effects["ESCUDO"] = {
					"VALOR": shield_value,
					"ROUNDS": 2,
				}

	def warrior_passive(self, player, target):
		player_class = self.players_classes[player]
		target_class = self.players_classes[target]
		if player_class.name == "Warrior":
			target_class.negative_effects["PROVOCADO"] = {"JOGADOR": player}
			self.makeAction(
				f"A passiva de {player} fez com que {target} fosse provocado!!"
			)

	def mage_passive(self, player, target, critical):
		player_class = self.players_classes[player]
		target_class = self.players_classes[target]
		if player_class.name == "Mage":
			if critical:
				burned = False
				if "QUEIMADO" in target_class.negative_effects:
					burned = True
				if not burned:
					target_class.negative_effects["QUEIMADO"] = {"ROUNDS": -1}
					self.makeAction(
						f"{target} está queimado agora por conta da passiva de {player}!!"
					)

	def mage_2(self, player, target):
		player_class = self.players_classes[player]
		if "ESCUDO_DE_FOGO" in player_class.other_effects:
			ability_name = "escudodefogo"
			target = self.update_targets(player, [target])[0]
			player_class.other_effects.pop("ESCUDO_DE_FOGO")
			self.makeAction(
				f"{player} tinha um escudo de fogo e ele estourou!"
			)
			damages, damagePerAlvo = self.update_damages_and_status(
				player, ability_name, [target]
			)
			self.extra_ability_calc(player, ability_name, [target], damages)

	def paladin_passive(self, player, damage):
		player_class = self.players_classes[player]
		if not (player_class.name == "Paladin"):
			return
		if player in self.team1_classes:
			playerTeam = self.team1_classes
		else:
			playerTeam = self.team2_classes

		hpAllies = {}
		for teamPlayer in playerTeam:
			teamPlayer_class = self.players_classes[teamPlayer]
			hpAllies[teamPlayer] = teamPlayer_class.hp

		minHp = min(hpAllies, key=hpAllies.get)
		targets = [minHp]

		for target in targets:
			target_class = self.players_classes[target]
			target_class_hp = target_class.hp
			if target_class_hp < target_class.__class__().hp:
				target_class.hp += damage / 2
				if target_class.hp > target_class.__class__().hp:
					target_class.hp = target_class.__class__().hp
			if player == target:
				self.makeAction(
					f"{player} se curou por conta de sua passiva!!"
				)
			else:
				self.makeAction(
					f"{target} foi curado por conta da passiva de {player}!!"
				)

	def trapper_passive(self, player, target):
		target_class = self.players_classes[target]
		if "TRAPPER00" in target_class.other_effects:
			damage = 7
			self.makeAction(
				f"{target} estava com a armadilha do Trapper! {player} tomará 7 de dano fixo!!"
			)
			times = target_class.other_effects["TRAPPER00"]["VEZES"]
			if times == 1:
				target_class.other_effects.pop("TRAPPER00")
			else:
				target_class.other_effects["TRAPPER00"]["VEZES"] = times - 1
			self.make_default_damage(player, damage, target)

	def startRound(self):
		self.makeAction(f"ROUND {self.round}")
		players_classes = self.players_classes.copy()
		for player in players_classes:
			check = self.check_all(player)
			if check == "DEATH":
				continue
			elif check == "END":
				return

			player_class = self.players_classes[player]

			cooldowns_to_remove = []
			for move in player_class.cooldowns:
				cooldown = player_class.cooldowns[move]
				if cooldown <= 0:
					cooldowns_to_remove.append(move)
				else:
					player_class.cooldowns[move] = cooldown - 1

			for move in cooldowns_to_remove:
				player_class.cooldowns.pop(move)

			if player in self.team1_classes:
				playerTeam = self.team1_classes
				enemyTeam = self.team2_classes
			else:
				playerTeam = self.team2_classes
				enemyTeam = self.team1_classes

			hpAllies = {}
			for teamPlayer in playerTeam:
				teamPlayer_class = self.players_classes[teamPlayer]
				hpAllies[teamPlayer] = teamPlayer_class.hp

			hpEnemies = {}
			for enemyPlayer in enemyTeam:
				enemyPlayer_class = self.players_classes[enemyPlayer]
				hpEnemies[enemyPlayer] = enemyPlayer_class.hp

			if player_class.name == "Cleric" and self.round != 1:
				self.makeAction(
					f"{player} pode curar o aliado com menos hp em 7 de hp, 30% de chance"
				)
				roll = self.roll(100)
				if roll <= 30:
					minHp = min(hpAllies, key=hpAllies.get)
					targets = [minHp]
					for target in targets:
						target_class = self.players_classes[target]
						self.makeAction(f"{target} foi curado em 7 de hp!!")
						target_class.hp += 7
						if target_class.hp > target_class.__class__().hp:
							target_class.hp = target_class.__class__().hp

			if "TRAPPER1" in player_class.other_effects:
				self.makeAction(f"{player} ativou sua habilidade de ataque!")
				ability_name = "trapper1_on"
				enemy = random.choice(list(enemyTeam))
				self.makeAction(f"Inimigo escolhido: {enemy}")
				damages, damagePerAlvo = self.update_damages_and_status(
					player, ability_name, [enemy]
				)
				self.extra_ability_calc(player, ability_name, [enemy], damages)
				player_class.other_effects.pop("TRAPPER1")

			if "TRAPPER3" in player_class.other_effects:
				difference = self.check_trapper3(playerTeam)

				if difference > 0:
					player_trapper = player_class.other_effects["TRAPPER3"][
						"JOGADOR"
					]
					self.makeAction(
						f"Ainda há {difference} do escudo de vida do Trapper sobrando!!"
					)
					self.makeAction(
						f"{player_trapper} dará então {difference} de dano no inimigo com menos Hp!!"
					)

					for teamPlayer in playerTeam:
						teamPlayer_class = playerTeam[teamPlayer]
						teamPlayer_class.other_effects.pop("TRAPPER3")

					ability_name = "trapper3_on"
					minHp = min(hpEnemies, key=hpEnemies.get)
					targets = [minHp]
					damages = {
						"DAMAGE": difference,
						"CRITICAL": difference * 1.5,
					}
					damages, damagePerAlvo = self.update_damages_and_status(
						player_trapper, ability_name, targets, damages
					)
					self.extra_ability_calc(
						player_trapper, ability_name, targets, damages
					)

			if "BERSERKER2" in player_class.other_effects:
				rounds = player_class.other_effects["BERSERKER2"]["ROUNDS"]
				rounds -= 1
				if rounds == 0:
					player_class.other_effects.pop("BERSERKER2")
					player_class.positive_effects["ROUBOVIDA"] = {
						"VALOR": 50,
						"ROUNDS": 1,
					}
				else:
					player_class.other_effects["BERSERKER2"]["ROUNDS"] = rounds

			if "BERSERKER3" in player_class.other_effects:
				player_class.hp += 15
				self.makeAction(
					f"{player} se curará em 15 de HP (habilidade especial)!"
				)
				if player_class.hp > player_class.__class__().hp:
					player_class.hp = player_class.__class__().hp
				rounds = player_class.other_effects["BERSERKER3"]["ROUNDS"]
				player_class.other_effects["BERSERKER3"]["ROUNDS"] = rounds - 1
				if rounds == 0:
					player_class.other_effects.pop("BERSERKER3")

	def make_default_damage(self, target, damage, player="", critical=False):
		if not player:
			player = self.player
		player_class = self.players_classes[player]

		if player in self.team1_classes:
			enemyTeam = self.team2_classes
		else:
			enemyTeam = self.team1_classes

		self.makeAction(f"{player} causou {damage} de dano em {target}!!")

		shield_value = 0
		trapper3_value = 0

		shield = False
		trapper3 = False

		target_class = self.players_classes[target]
		target_hp = target_class.hp

		if "TRAPPER3" in target_class.other_effects:
			trapper3_value = self.check_trapper3(enemyTeam)
			if trapper3_value > 0:
				trapper3 = True
				self.makeAction(
					f"O dano em {target} atingiu na armadilha defensiva do Trapper!!!"
				)

		if "ESCUDO" in target_class.positive_effects:
			shield_value = target_class.positive_effects["ESCUDO"]["VALOR"]
			shield = True

		if trapper3:
			trapper3_value -= damage
			damage = trapper3_value
			target_class.other_effects["TRAPPER3"]["VALOR"] = trapper3_value
			if trapper3_value < 0 and damage < 0:
				damage *= -1
				target_class.other_effects["TRAPPER3"]["VALOR"] = 0
				if shield_value > 0 and not critical:
					self.makeAction(
						f"A armadilha defensiva do Trapper quebrou, o dano restante ({damage}) incidirá no escudo de {target}!!"
					)
					shield_value -= damage
					damage = shield_value
					if shield_value < 0 and damage < 0:
						damage *= -1
						self.makeAction(
							f"O escudo de {target} quebrou, o dano restante ({damage}) incidirá no HP do próprio!!"
						)
						target_hp -= damage
						shield_value = 0

				elif shield_value > 0 and critical:
					self.makeAction(
						"Pelo dano ser crítico, o dano que iria ser no escudo irá ser no HP!!"
					)
					target_hp -= damage

				else:
					target_hp -= damage

		elif shield:
			if shield_value > 0 and not critical:
				self.makeAction(f"O dano atingirá o escudo de {target}!")
				shield_value -= damage
				damage = shield_value
				if shield_value < 0 and damage < 0:
					damage *= -1
					self.makeAction(
						f"O escudo de {target} quebrou, o dano restante ({damage}) incidirá no HP do próprio!!"
					)
					target_hp -= damage
					shield_value = 0

			elif shield_value > 0 and critical:
				self.makeAction(
					"Pelo dano ser crítico, o dano que iria ser no escudo irá ser no HP!!"
				)
				target_hp -= damage

		else:
			target_hp -= damage

		if shield:
			if shield_value == 0:
				target_class.positive_effects.pop("ESCUDO")
			else:
				target_class.positive_effects["ESCUDO"]["VALOR"] = shield_value

		target_class.hp = target_hp

		if "ROUBOVIDA" in player_class.positive_effects:
			lifesteal = player_class.positive_effects["ROUBOVIDA"]["VALOR"]
			hp_stolen = damage * (lifesteal / 100)
			player_class.hp += hp_stolen
			if player_class.hp > player_class.__class__().hp:
				player_class.hp = player_class.__class__().hp
			self.makeAction(
				f"{player} está com roubo de vida e roubou {hp_stolen} de {target}!!"
			)

		if self.check_death(target):
			return

		self.warrior_passive(player, target)
		self.mage_passive(player, target, critical)
		self.paladin_passive(player, damage)
		self.mage_2(target, player)
		self.trapper_passive(player, target)

	def basic_attack(self, player, ability, targets):
		player_class = self.players_classes[player]
		damage = player_class.atk / 10
		critical = damage * 1.5
		damages = {"DAMAGE": damage, "CRITICAL": critical}

		damages, damagesPerAlvo = self.update_damages_and_status(
			player, ability, targets, damages
		)

		for target in targets:
			check = self.check_all(target)
			if check == "DEATH":
				self.makeAction(f"{target} seria golpeado mas está abatido!!")
				continue
			elif check == "END":
				return
			elif check == "IMMUNITY":
				self.makeAction(
					f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
				)
				continue

			self.makeAction(f"Alvo: {target}")
			dodge = self.dodge(target, player)
			if not dodge:
				critical_rate = player_class.cr
				critical = self.critical(critical_rate, player)
				if critical:
					damage = damages["CRITICAL"]
				else:
					damage = damages["DAMAGE"]
				self.make_default_damage(target, damage, player, critical)

	def ability_calc(self):
		self.player_class = self.players_classes[self.player]

		if not (self.ability == "batk") and (
			self.ability in self.player_class.default_abilities
		):
			self.makeAction(
				f"{self.player} usa sua {self.ability_class.type_name}!!"
			)
		elif self.ability not in self.player_class.default_abilities:
			class_original = classes.classes_dict[self.ability[:-1]]().name
			self.makeAction(
				f"{self.player} utiliza a {self.ability_class.type_name} de {class_original}!"
			)
		else:
			self.makeAction(
				f"{self.player} usa seu {self.ability_class.type_name}!!"
			)

		if self.ability == "warrior1":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue

				self.makeAction(f"{target} vai ser atacado!!")
				target_class = self.players_classes[target]
				dodge = self.dodge(target, self.player)
				if not dodge:
					critical_rate = self.player_class.cr
					critical = self.critical(critical_rate, self.player)
					if critical:
						damage = self.damages["CRITICAL"]
					else:
						damage = self.damages["DAMAGE"]
					self.make_default_damage(
						target, damage, self.player, critical
					)
					if self.check_death(target):
						continue
					if "ENFRAQUECIDO" in target_class.negative_effects:
						effect_value = target_class.negative_effects[
							"ENFRAQUECIDO"
						]["VALOR"]
						effect_value += 20
						if effect_value > 90:
							effect_value = 90
					else:
						effect_value = 20

					self.makeAction(f"{target} foi enfraquecido em 20%")
					target_class.negative_effects["ENFRAQUECIDO"] = {
						"VALOR": effect_value,
						"ROUNDS": 2,
					}

		elif self.ability == "warrior2":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				if "PROTEGIDO" in target_class.positive_effects:
					effect_value = target_class.positive_effects["PROTEGIDO"][
						"VALOR"
					]
					effect_value += 60
					if effect_value > 90:
						effect_value = 90
					else:
						effect_value = 60
				else:
					effect_value = 60

				self.makeAction(
					f"{target} ficará 60% mais protegido durante esta rodada e a próxima"
				)
				target_class.positive_effects["PROTEGIDO"] = {
					"VALOR": effect_value,
					"ROUNDS": 2,
				}
				self.bard_passive(self.playerTeam, target)

		elif self.ability == "warrior3":
			maxHp = max(self.hpEnemies, key=self.hpEnemies.get)
			target_class = self.players_classes[maxHp]

			check = self.check_all(maxHp)
			if check == "DEATH":
				return
			elif check == "END":
				return
			elif check == "IMMUNITY":
				self.makeAction(
					f"{maxHp} seria o alvo mas está imune!! Nada o afetará nesta rodada"
				)
				return

			self.makeAction(
				f"{maxHp} é o inimigo com mais HP, ele que levará o dano da habilidade"
			)
			dodge = self.dodge(maxHp, self.player)
			if not dodge:
				critical_rate = self.player_class.cr
				critical = self.critical(critical_rate, self.player)
				if critical:
					damage = self.damages["CRITICAL"]
				else:
					damage = self.damages["DAMAGE"]
				self.make_default_damage(maxHp, damage, self.player, critical)

		elif self.ability == "mage1":
			self.targets = list(self.enemyTeam)
			self.damages, self.damagePerTarget = (
				self.update_damages_and_status(
					self.player, self.ability, self.targets
				)
			)

			self.makeAction("Todos os adversários serão atingidos")
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue

				self.makeAction(f"Alvo: {target}")
				target_class = self.players_classes[target]
				dodge = self.dodge(target, self.player)
				if not dodge:
					critical_rate = self.player_class.cr
					critical = self.critical(critical_rate, self.player)
					if critical:
						damage = self.damagePerTarget[target]["CRITICAL"]
					else:
						damage = self.damagePerTarget[target]["DAMAGE"]
					self.make_default_damage(
						target, damage, self.player, critical
					)

		elif self.ability == "mage2":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue

				self.makeAction(
					f"{target} recebeu um escudo de fogo de {self.player}"
				)
				target_class = self.players_classes[target]
				target_class.other_effects["ESCUDO_DE_FOGO"] = {}

		elif self.ability == "mage3":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				dodge = self.dodge(target, self.player)
				if not dodge:
					burned = False
					if "QUEIMADO" in target_class.negative_effects:
						burned = True
					critical_rate = self.player_class.cr
					critical = self.critical(critical_rate, self.player)
					if critical and burned:
						self.makeAction(
							f"{target} está queimado, então não só levará crítico como também um dano em dobro"
						)
						damage = self.damages["CRITICAL_BURNED"]
					elif critical and not burned:
						damage = self.damages["CRITICAL"]
					elif not critical and burned:
						self.makeAction(
							f"{target} levará dano em dobro por estar queimado"
						)
						damage = self.damages["DAMAGE_BURNED"]
					elif not critical and not burned:
						damage = self.damages["DAMAGE"]
					self.make_default_damage(
						target, damage, self.player, critical
					)

					if self.check_death(target):
						continue

					if not burned:
						self.makeAction(f"{target} está agora queimado!!")
						target_class.negative_effects["QUEIMADO"] = {
							"ROUNDS": -1
						}

		elif self.ability == "cleric1":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				self.makeAction(
					f"Ele utilizou a habilidade de dano em {target}"
				)
				target_class = self.players_classes[target]
				dodge = self.dodge(target, self.player)
				if not dodge:
					critical_rate = self.player_class.cr
					critical = self.critical(critical_rate, self.player)
					if critical:
						damage = self.damages["CRITICAL"]
					else:
						damage = self.damages["DAMAGE"]
					self.make_default_damage(
						target, damage, self.player, critical
					)

			self.targets = list(self.playerTeam)

			self.makeAction(
				f"Todos os alidos de {self.player} serão curados em 2 de HP"
			)
			for ally in self.targets:
				check = self.check_all(ally)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					continue
				ally_class = self.players_classes[ally]
				ally_class.hp += 2
				if ally_class.hp > ally_class.__class__().hp:
					ally_class.hp = ally_class.__class__().hp

		elif self.ability == "cleric2":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} ganharia 8 de hp mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				target_class.hp += 8
				self.makeAction(f"{target} ganhará 8 de hp!!")
				if target_class.hp > target_class.__class__().hp:
					target_class.hp = target_class.__class__().hp

				self.makeAction(
					f"Os aliados de {target} ganharão também 3 de hp!!"
				)
				for ally in self.playerTeam:
					if ally != target:
						ally_class = self.players_classes[ally]
						ally_class.hp += 3
						if ally_class.hp > ally_class.__class__().hp:
							ally_class.hp = ally_class.__class__().hp

		elif self.ability == "cleric3":
			self.targets = list(self.playerTeam)
			self.makeAction(
				f"Todos os aliados de {self.player} ganharão 15 pontos de HP"
			)

			self.makeAction("terão também seus efeitos negativos removidos")
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					continue
				target_class = self.players_classes[target]
				target_class.hp += 15
				if target_class.hp > target_class.__class__().hp:
					target_class.hp = target_class.__class__().hp
				target_class.negative_effects.clear()

		elif self.ability == "ninja1":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				self.makeAction(f"{self.player} atingirá {target}")
				target_class = self.players_classes[target]
				dodge = self.dodge(target, self.player)
				if not dodge:
					negative_effects = False
					if target_class.negative_effects:
						negative_effects = True
					critical_rate = self.player_class.cr
					critical = self.critical(critical_rate, self.player)
					if critical and negative_effects:
						damage = self.damagePerTarget[target][
							"DOUBLE_CRITICAL"
						]
					elif critical and not negative_effects:
						damage = self.damagePerTarget[target]["CRITICAL"]
					elif not critical and negative_effects:
						damage = self.damagePerTarget[target]["DOUBLE_DAMAGE"]
					elif not critical and not negative_effects:
						damage = self.damagePerTarget[target]["DAMAGE"]
					self.make_default_damage(
						target, damage, self.player, critical
					)

		elif self.ability == "ninja2":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				target_class.other_effects["NINJA2"] = {
					"ROUNDS": 2,
					"DR_ORIG": target_class.dr,
				}
				target_class.dr = self.player_class.dr
				self.makeAction(
					f"{target} ficará com a mesma taxa de desvio de {self.player} agora"
				)

		elif self.ability == "ninja3":
			self.player_class.atk += 10
			self.player_class.dr += 10
			self.player_class.cr += 10

			self.makeAction(
				f"{self.player} aumentou seu ataque, taxa de desvio e taxa crítica em 10 cada um"
			)
			self.player_class.other_effects["NINJA3"] = {"ROUNDS": 2}
			minHp = min(self.hpEnemies, key=self.hpEnemies.get)
			targets = [minHp]

			self.makeAction(
				f"{self.player} utilizará um ataque básico agora em {minHp}!"
			)
			self.basic_attack(self.player, self.ability, targets)

		elif self.ability == "paladin1":
			times = 0
			for target in self.targets:
				maxHp = ""
				maxHp_value = max(self.hpEnemies.values())
				if self.hpEnemies[target] == maxHp_value:
					maxHp = target
				self.makeAction(f"{target} é o alvo")
				while times != 2:
					check = self.check_all(target)
					if check == "DEATH":
						self.makeAction(
							f"{target} seria golpeado mas está abatido!!"
						)
						break
					elif check == "END":
						return
					elif check == "IMMUNITY":
						self.makeAction(
							f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
						)
						break

					target_class = self.players_classes[target]
					dodge = self.dodge(target, self.player)
					if not dodge:
						critical_rate = self.player_class.cr
						critical = self.critical(critical_rate, self.player)
						if critical:
							damage = self.damages["CRITICAL"]
						else:
							damage = self.damages["DAMAGE"]
						self.make_default_damage(
							target, damage, self.player, critical
						)
					else:
						break

					times += 1

					if maxHp == target and times != 2:
						self.makeAction(
							f"{self.player} utilizará o golpe mais uma vez, já que {target} era o inimigo com mais HP"
						)
					else:
						break

		elif self.ability == "paladin2":
			self.targets = list(self.playerTeam)
			for player in self.targets:
				check = self.check_all(player)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				player_class = self.players_classes[player]
				if "PROTEGIDO" in player_class.positive_effects:
					effect_value = player_class.positive_effects["PROTEGIDO"][
						"VALOR"
					]
					effect_value += 20
					if effect_value > 90:
						effect_value = 90
				else:
					effect_value = 20
				self.makeAction(f"{player} foi protegido em 20%")
				player_class.positive_effects["PROTEGIDO"] = {
					"VALOR": effect_value,
					"ROUNDS": 2,
				}
				self.bard_passive(self.playerTeam, player)

		elif self.ability == "paladin3":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				if "PROTEGIDO" in target_class.positive_effects:
					effect_value = target_class.positive_effects["PROTEGIDO"][
						"VALOR"
					]
					effect_value += 50
					if effect_value > 90:
						effect_value = 90
				else:
					effect_value = 50
				target_class.positive_effects["PROTEGIDO"] = {
					"VALOR": effect_value,
					"ROUNDS": 2,
				}
				self.bard_passive(self.playerTeam, target)
				if "FORTALECIDO" in target_class.positive_effects:
					effect_value = target_class.positive_effects[
						"FORTALECIDO"
					]["VALOR"]
					effect_value += 50
				else:
					effect_value = 50
				target_class.positive_effects["FORTALECIDO"] = {
					"VALOR": effect_value,
					"ROUNDS": 2,
				}
				self.makeAction(
					f"Durante esta rodada e a próxima, {target} ficará 50% protegido e 50% fortalecido"
				)
				self.bard_passive(self.playerTeam, target)

		elif self.ability == "trapper1":
			if "ESCUDO" in self.player_class.positive_effects:
				shield = self.player_class.positive_effects["ESCUDO"]["VALOR"]
				shield += 10
			else:
				shield = 10
			self.player_class.positive_effects["ESCUDO"] = {
				"VALOR": shield,
				"ROUNDS": 1,
			}
			self.player_class.other_effects["TRAPPER1"] = {"ROUNDS": 1}
			self.makeAction(f"{self.player} ganhou 10 de escudo")

		elif self.ability == "trapper2":
			target = self.targets[0]
			ability = self.targets[-1]
			ability_name = abilities.abilities_dict[ability].type_name

			check = self.check_all(target)
			if check == "DEATH":
				return
			elif check == "END":
				return
			elif check == "IMMUNITY":
				self.makeAction(
					f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
				)
				return

			target_class = self.players_classes[target]
			target_class.other_effects["TRAPPER2"] = {
				"ABILITY": ability,
				"ROUNDS": 2,
			}
			self.makeAction(
				f"{target} teve sua {ability_name} bloqueada durante essa rodada e a próxima"
			)

		elif self.ability == "trapper3":
			self.targets = list(self.playerTeam)

			for player in self.targets:
				check = self.check_all(player)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				player_class = self.players_classes[player]
				player_class.other_effects["TRAPPER3"] = {
					"VALOR": 20,
					"JOGADOR": self.player,
				}
			self.makeAction(
				f"A equipe de {self.player} está com um escudo de vida de 20HP agora"
			)

		elif self.ability == "archer1":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				times = 0
				target_class = self.players_classes[target]
				self.makeAction(
					f"Três ataques básicos serão utilizados em {target}!!"
				)

				while times != 3:
					check = self.check_all(target)
					if check == "DEATH":
						self.makeAction(
							f"{target} seria golpeado novamente mas está abatido!!"
						)
						break
					elif check == "END":
						return
					if times == 0:
						self.makeAction("Primeiro ataque:")
					elif times == 1:
						self.makeAction("Segundo ataque:")
					elif times == 2:
						self.makeAction("Terceiro ataque:")
					self.basic_attack(self.player, self.ability, self.targets)
					times += 1

		elif self.ability == "archer2":
			self.targets = list(self.playerTeam)
			for player in self.targets:
				check = self.check_all(player)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					continue
				player_class = self.players_classes[player]
				player_class.cr += 10
				player_class.other_effects["ARCHER2"] = {"ROUNDS": 1}
			self.makeAction(
				f"Todos os aliados de {self.player} tiveram sua taxa crítica aumentada em 10!!"
			)
			maxHp = max(self.hpEnemies, key=self.hpEnemies.get)
			targets = [maxHp]
			self.makeAction(f"{self.player} dará um ataque básico em {maxHp}")
			self.basic_attack(self.player, self.ability, targets)

		elif self.ability == "archer3":
			stat = self.targets[0]
			if stat == "atk":
				self.player_class.atk += 10
				self.makeAction("Aumentou seu ataque em 10!!")
			elif stat == "tc":
				self.player_class.cr += 10
				self.makeAction("Aumentou sua taxa crítica em 10!!")
			elif stat == "td":
				self.player_class.dr += 10
				self.makeAction("Aumentou sua taxa de desvio em 10!!")
			minHp = min(self.hpEnemies, key=self.hpEnemies.get)
			targets = [minHp]
			self.makeAction(
				f"{minHp} receberá um ataque básico de {self.player}"
			)
			self.basic_attack(self.player, self.ability, targets)

		elif self.ability == "berserker1":
			self.player_class.hp -= 10
			self.makeAction(f"{self.player} perdeu 10 de HP")
			check = self.check_all(self.player)
			if check == "DEATH":
				return
			elif check == "END":
				return
			aditional_atk = (
				(
					(self.player_class.hp - self.player_class.__class__().hp)
					* -1
				)
				// 10
				% 10
			) * 2
			for damage in self.damages:
				self.damages[damage] += aditional_atk
			if aditional_atk:
				self.makeAction(
					f"{self.player} terá {aditional_atk} a mais de ataque na sua habilidade"
				)

			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				dodge = self.dodge(target, self.player)
				if not dodge:
					critical_rate = self.player_class.cr
					critical = self.critical(critical_rate, self.player)
					if critical:
						damage = self.damages["CRITICAL"]
					else:
						damage = self.damages["DAMAGE"]
					self.make_default_damage(
						target, damage, self.player, critical
					)

		elif self.ability == "berserker2":
			self.player_class.hp -= 10
			self.makeAction(f"{self.player} perdeu 10 de HP")
			check = self.check_all(self.player)
			if check == "DEATH":
				return
			elif check == "END":
				return

			self.targets = list(self.playerTeam)

			for player in self.playerTeam:
				if player == self.player:
					continue
				check = self.check_all(player)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					continue
				player_class = self.players_classes[player]
				player_class.positive_effects["ROUBOVIDA"] = {
					"VALOR": 50,
					"ROUNDS": 1,
				}
			self.makeAction(
				"Toda a sua equipe agora tem 50% de roubo de vida, ele terá na próxima rodada também"
			)
			self.player_class.other_effects["BERSERKER2"] = {"ROUNDS": 1}

		elif self.ability == "berserker3":
			self.player_class.hp -= 30
			self.makeAction("Ele perdeu 30 de hp")
			check = self.check_all(self.player)
			if check == "DEATH":
				return
			elif check == "END":
				return

			self.player_class.negative_effects.clear()
			self.player_class.other_effects["BERSERKER3"] = {"ROUNDS": 3}
			self.makeAction(
				"Ele limpou seus efeitos negativos e ganhará 15 de HP durante as próximas 3 rodadas"
			)

		elif self.ability == "bard1":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				self.makeAction(f"{target} é o alvo")
				target_class = self.players_classes[target]
				dodge = self.dodge(target, self.player)
				if not dodge:
					critical_rate = self.player_class.cr
					critical = self.critical(critical_rate, self.player)
					if critical:
						damage = self.damages["CRITICAL"]
					else:
						damage = self.damages["DAMAGE"]
					self.make_default_damage(
						target, damage, self.player, critical
					)
					target_class.positive_effects.clear()
					self.makeAction(
						f"{target} teve seus efeitos positivos limpos"
					)

		elif self.ability == "bard2":
			self.targets = list(self.playerTeam)
			self.makeAction(
				"Todos os aliados foram fortalecidos e não tem mais efeitos negativos"
			)

			for player in self.targets:
				check = self.check_all(player)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					continue
				player_class = self.players_classes[player]
				if "FORTALECIDO" in player_class.positive_effects:
					effect_value = player_class.positive_effects[
						"FORTALECIDO"
					]["VALOR"]
					effect_value += 20
				else:
					effect_value = 20
				player_class.positive_effects["FORTALECIDO"] = {
					"VALOR": effect_value,
					"ROUNDS": 2,
				}
				self.bard_passive(self.playerTeam, player)
				self.player_class.negative_effects.clear()

		elif self.ability == "bard3":
			for e, target in enumerate(self.targets, start=1):
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(f"{target} seria alvo mas está abatido!!")
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				if e == 1:
					self.makeAction(f"{target} é o alvo do dano da habilidade")
					dodge = self.dodge(target, self.player)
					if not dodge:
						critical_rate = self.player_class.cr
						critical = self.critical(critical_rate, self.player)
						if critical:
							damage = self.damages["CRITICAL"]
						else:
							damage = self.damages["DAMAGE"]
						self.make_default_damage(
							target, damage, self.player, critical
						)
						if self.check_death(target):
							continue

				if e == 2:
					if "ATORDOADO" in target_class.negative_effects:
						self.makeAction(
							f"{target} iria ser atordoado pela habilidade, mas já está"
						)
					else:
						self.makeAction(
							f"{target} foi atordoado pela habilidade!!"
						)
						target_class.negative_effects["ATORDOADO"] = {}

				if e == 3:
					if "ENFRAQUECIDO" in target_class.negative_effects:
						effect_value = target_class.negative_effects[
							"ENFRAQUECIDO"
						]["VALOR"]
						effect_value += 50
						if effect_value > 90:
							effect_value = 90
					else:
						effect_value = 50

					self.makeAction(
						f"{target} foi enfraquecido em 50% pela habilidade!!!"
					)
					target_class.negative_effects["ENFRAQUECIDO"] = {
						"VALOR": effect_value,
						"ROUNDS": 2,
					}

		elif self.ability == "necromancer1":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue

				self.makeAction(f"O dano incidirá em {target}")
				target_class = self.players_classes[target]
				dodge = self.dodge(target, self.player)
				if not dodge:
					critical_rate = self.player_class.cr
					critical = self.critical(critical_rate, self.player)
					if critical:
						damage = self.damages["CRITICAL"]
					else:
						damage = self.damages["DAMAGE"]
					self.make_default_damage(
						target, damage, self.player, critical
					)
					if self.check_death(target):
						continue
					if "ENVENENADO" in target_class.negative_effects:
						self.makeAction(
							f"{target} seria envenenado, mas já está envenenado"
						)
					else:
						self.makeAction(
							f"{target} foi envenenado por duas rodadas!!"
						)
						target_class.negative_effects["ENVENENADO"] = {
							"ROUNDS": 2
						}

		elif self.ability == "necromancer2":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				if "ENFRAQUECIDO" in target_class.negative_effects:
					effect_value = target_class.negative_effects[
						"ENFRAQUECIDO"
					]["VALOR"]
					effect_value += 50
					if effect_value > 90:
						effect_value = 90
				else:
					effect_value = 50

				self.makeAction(f"{target} foi enfraquecido em 50%!!")
				target_class.negative_effects["ENFRAQUECIDO"] = {
					"VALOR": effect_value,
					"ROUNDS": 2,
				}
				target_class.positive_effects.clear()

				self.makeAction("Teve seus efeitos positivos também limpos")

		elif self.ability == "necromancer3":
			for target in self.targets:
				check = self.check_all(target)
				if check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria curado mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				dead = True if target in self.players_dead else False
				if dead:
					target_class = self.players_dead[target]
				else:
					target_class = self.players_classes[target]

				if dead:
					target_class.hp = target_class.__class__().hp * 0.3
					target_class.negative_effects["ENVENENADO"] = {
						"ROUNDS": -1
					}
					self.players_classes[target] = target_class
					self.players_dead.pop(target)
					if target in self.team1_dead:
						self.team1_classes[target] = target_class
						self.team1_dead.pop(target)
						for player in self.team1_classes:
							player_class = self.players_classes[player]
							if "TRAPPER3" in player_class.other_effects:
								player_trapper3 = player_class.other_effects[
									"TRAPPER3"
								]
								target_class.other_effects["TRAPPER3"] = {
									"VALOR": 20,
									"JOGADOR": player_trapper3,
								}
					else:
						self.team2_classes[target] = target_class
						self.team2_dead.pop(target)
						for player in self.team2_classes:
							player_class = self.players_classes[player]
							if "TRAPPER3" in player_class.other_effects:
								player_trapper3 = player_class.other_effects[
									"TRAPPER3"
								]
								target_class.other_effects["TRAPPER3"] = {
									"VALOR": 20,
									"JOGADOR": player_trapper3,
								}
					self.makeAction(f"{self.player} reviveu {target}!!")
					self.makeAction(
						f"{target} está com 30% de seu HP e envenenado!"
					)

				elif target in self.players_classes:
					target_class.positive_effects["FORTALECIDO"] = {
						"VALOR": 100,
						"ROUNDS": 2,
					}
					self.bard_passive(self.playerTeam, target)
					target_class.negative_effects["ENVENENADO"] = {"ROUNDS": 2}
					self.makeAction(
						f"{self.player} optou por deixar seu aliado {target} envenenado e fortalecido em 100% por duas rodadas!!"
					)

		elif self.ability == "gambler1":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				self.makeAction(f"O alvo é {target}")
				dodge = self.dodge(target, self.player)
				if not dodge:
					self.makeAction(
						f"{target} será atingido, o dano será baseado numa rolagem de dois dados"
					)
					roll1 = self.roll(10)
					roll2 = self.roll(10)
					damages = [roll1, roll2]
					for e, damage in enumerate(damages, start=1):
						self.damages = {
							"DAMAGE": damage,
							"CRITICAL": damage * 1.5,
						}
						self.makeAction(f"Dado {e}:")
						self.damages, damagePerTarget = (
							self.update_damages_and_status(
								self.player,
								self.ability,
								[target],
								self.damages,
							)
						)
						critical_rate = self.player_class.cr
						critical = self.critical(critical_rate, self.player)
						if critical:
							damage = self.damages["CRITICAL"]
						else:
							damage = self.damages["DAMAGE"]
						self.make_default_damage(
							target, damage, self.player, critical
						)
						check = self.check_all(target)
						if check == "DEATH":
							break
						elif check == "END":
							return

		elif self.ability == "gambler2":
			self.player_class.other_effects["IMUNIDADE"] = {"ROUNDS": 1}
			self.player_class.gold += 10
			self.makeAction(
				f"{self.player} ficou imune por esta rodada, e ganhou 10 de ouro"
			)

		elif self.ability == "gambler3":
			for target in self.targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				self.player_class.gold -= 30
				self.makeAction(f"{self.player} dará roll 2 vezes")
				roll1 = self.roll(20)
				roll2 = self.roll(20)
				best_roll = max([roll1, roll2])
				self.makeAction(
					f"Se {target} tirar um resultado menor do que o maior deles ({best_roll}), perderá metade da vida"
				)
				roll3 = self.roll(20)
				if roll3 < best_roll:
					self.makeAction(
						f"{target} ficará com metade de sua vida perdida!!"
					)
					target_class = self.players_classes[target]
					target_class.hp /= 2
				else:
					self.makeAction(f"{target} ganhou na roll!!")

		elif self.ability == "spirit1":
			if "POSSUINDO" not in self.player_class.other_effects:
				self.makeAction(
					"Não há jogador que ele esteja possuindo neste momento, no entanto"
				)
				return
			player = self.player_class.other_effects["POSSUINDO"]
			player_class = self.players_classes[player]
			maxHp = max(self.hpEnemies, key=self.hpEnemies.get)
			act = player_class.default_abilities[1]
			targets = [maxHp]
			act: ActsCalculator = ActsCalculator(
				self.idGame,
				player,
				act,
				targets,
				self.players_classes,
				self.team1_classes,
				self.team2_classes,
				self.players_dead,
				self.team1_dead,
				self.team2_dead,
				self.round,
			)
			(
				self.playersClasses,
				self.team1_classes,
				self.team2_classes,
				self.playersDead,
				self.team1_dead,
				self.team2_dead,
				self.end_game,
			) = act.controller()

		elif self.ability == "spirit2":
			new_possessed = self.targets[0]
			check = self.check_all(new_possessed)
			if check == "DEATH":
				self.makeAction(
					f"{new_possessed} seria possuído mas está abatido!!"
				)
				return
			elif check == "END":
				return
			elif check == "IMMUNITY":
				self.makeAction(
					f"{new_possessed} seria o alvo mas está imune!! Nada o afetará nesta rodada"
				)
				return
			if "POSSUINDO" in self.player_class.other_effects:
				possessed = self.player_class.other_effects["POSSUINDO"]
				possessed_class = self.players_classes[possessed]
				possessed_class.hp += 5
				possessed_class.other_effects.pop("POSSUIDO")
				self.makeAction(
					f"{self.player} saiu de {possessed} e o curou com 5 de hp!!"
				)
			self.player_class.other_effects["POSSUINDO"] = new_possessed
			target_class = self.players_classes[new_possessed]
			target_class.other_effects["POSSUIDO"] = self.player
			self.makeAction(f"{self.player} agora possuirá {new_possessed}!!")
			if "ESCUDO" in target_class.positive_effects:
				shield = target_class.positive_effects["ESCUDO"]["VALOR"]
				shield += 10
			else:
				shield = 10
			target_class.positive_effects["ESCUDO"] = {
				"VALOR": shield,
				"ROUNDS": 2,
			}

		elif self.ability == "spirit3":
			if "POSSUINDO" not in self.player_class.other_effects:
				self.makeAction(
					"Não há jogador que ele esteja possuindo neste momento, no entanto"
				)
				return
			possessed = self.player_class.other_effects["POSSUINDO"]
			possessed_class = self.players_classes[possessed]
			possessed_class.hp = possessed_class.__class__().hp
			possessed_class.negative_effects.clear()
			self.player_class.hp = 0
			self.check_death(self.player)
			self.makeAction(
				f"{self.player} se sacrificou e {possessed} está totalmente restaurado!!"
			)

		elif self.ability == "batk":
			self.basic_attack(self.player, self.ability, self.targets)

	def extra_ability_calc(self, player, ability, targets, damages):
		player_class = self.players_classes[player]

		if ability == "escudodefogo":
			for target in targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				dodge = self.dodge(target, player)
				if not dodge:
					critical_rate = player_class.cr
					critical = self.critical(critical_rate, player)
					if critical:
						damage = damages["CRITICAL"]
					else:
						damage = damages["DAMAGE"]
					self.make_default_damage(target, damage, player, critical)
					if "ENFRAQUECIDO" in target_class.negative_effects:
						effect_value = target_class.negative_effects[
							"ENFRAQUECIDO"
						]["VALOR"]
						effect_value += 20
						if effect_value > 90:
							effect_value = 90
					else:
						effect_value = 20
					target_class.negative_effects["ENFRAQUECIDO"] = {
						"VALOR": effect_value,
						"ROUNDS": 2,
					}

		if ability == "trapper1_on":
			for target in targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				dodge = self.dodge(target, player)
				if not dodge:
					if "ESCUDO" in player_class.positive_effects:
						shield_value = player_class.positive_effects["ESCUDO"][
							"VALOR"
						]
						damages_copy = damages.copy()
						for damage in damages_copy:
							damage = damages[damage]
							damages[damage] = damage + shield_value
					critical_rate = player_class.cr
					critical = self.critical(critical_rate, player)
					if critical:
						damage = damages["CRITICAL"]
					else:
						damage = damages["DAMAGE"]
					self.make_default_damage(target, damage, player, critical)

		if ability == "trapper3_on":
			for target in targets:
				check = self.check_all(target)
				if check == "DEATH":
					self.makeAction(
						f"{target} seria golpeado mas está abatido!!"
					)
					continue
				elif check == "END":
					return
				elif check == "IMMUNITY":
					self.makeAction(
						f"{target} seria o alvo mas está imune!! Nada o afetará nesta rodada"
					)
					continue
				target_class = self.players_classes[target]
				dodge = self.dodge(target, player)
				if not dodge:
					critical_rate = player_class.cr
					critical = self.critical(critical_rate, player)
					if critical:
						damage = damages["CRITICAL"]
					else:
						damage = damages["DAMAGE"]
					self.make_default_damage(target, damage, player, critical)
