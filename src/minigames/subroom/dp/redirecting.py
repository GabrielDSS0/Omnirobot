import config
import src.commands_list as cmd_list
import src.minigames.subroom.dp.playing.game as dp_game
import src.sending as sending
import src.vars as vars


class RedirectingFunction:
	def __init__(self) -> None:
		self.websocket = vars.Varlist.websocket

		self.room = vars.Varlist.room
		self.groupchat_name_complete = vars.Varlist.groupchat_name_complete
		self.senderID = vars.Varlist.senderID
		self.msgType = vars.Varlist.msgType

		self.command = vars.Varlist.command
		self.commandParams = vars.Varlist.commandParams

		self.hosts_groupchats = vars.Varlist.hosts_groupchats
		self.dpGames = vars.Varlist.dpGames

	async def redirect_to_function(self):
		if self.msgType == "room" and self.room[:9] != "groupchat":
			return sending.respondRoom(
				"Este comando não pode ser executado em salas públicas.",
				self.room,
			)

		if self.senderID in self.dpGames and self.msgType == "pm":
			self.groupchat_name_complete = list(self.dpGames[self.senderID])[0]

		elif self.senderID in self.hosts_groupchats:
			if len(self.hosts_groupchats[self.senderID]) == 1:
				self.groupchat_name_complete = self.hosts_groupchats[
					self.senderID
				][0]

		command_permission = cmd_list.commands_dp[self.command]["perm"]
		command_params_default = cmd_list.commands_dp[self.command]["params"]
		need_room = cmd_list.commands_dp[self.command]["need_room"]

		if (
			need_room
			and self.msgType == "room"
			and len(self.commandParams) < (len(command_params_default) - 1)
		):
			return sending.respondRoom(
				f"Uso: {config.prefix}{self.command} **{', '.join(command_params_default[1:])}**",
				self.groupchat_name_complete,
			)

		elif (
			self.msgType != "room"
			and len(self.commandParams) < len(command_params_default)
			and self.senderID in self.hosts_groupchats
		):
			return sending.respond(
				self.msgType,
				f"Uso: {config.prefix}{self.command} **{', '.join(command_params_default)}**",
				self.senderID,
				self.groupchat_name_complete,
			)

		if (
			command_permission == "host"
			or command_permission == "adm"
			or (command_permission == "general" and self.msgType == "room")
		):
			permission = await self.verify_perm(self.senderID)
			if permission == "INVALID":
				return sending.respondPM(
					self.senderID,
					"Você não tem permissão para executar este comando.",
				)

			elif permission == "INVALIDROOM":
				return sending.respondPM(
					self.senderID, "O bot não está nessa room."
				)

		if (
			cmd_list.commands_dp[self.command]["type"] == "pm"
			and self.msgType == "room"
		):
			return sending.respondPM(
				self.senderID,
				"Este comando deve ser executado somente por PM.",
			)

		if command_permission == "host":
			if self.senderID not in self.dpGames and self.command != "startdp":
				return sending.respondPM(
					self.senderID,
					"Não há um jogo de Dungeons & Pokémon ativo na subsala atualmente.",
				)

			if self.senderID in self.dpGames and self.msgType == "room":
				if (
					self.groupchat_name_complete
					not in self.dpGames[self.senderID]
				):
					return sending.respondPM(
						self.senderID,
						"Você já está hosteando um jogo de Dugenons & Pokémon em outra sala.",
					)

			if (
				self.senderID not in self.dpGames
				or self.groupchat_name_complete
				not in self.dpGames[self.senderID]
			) and self.command == "startdp":
				dpGame: dp_game.GameCommands = dp_game.GameCommands(
					self.senderID, self.groupchat_name_complete
				)
				vars.Varlist.host = self.senderID
				if self.senderID not in self.dpGames:
					self.dpGames[self.senderID] = {
						self.groupchat_name_complete: dpGame
					}
				else:
					self.dpGames[self.senderID].update(
						{self.groupchat_name_complete: dpGame}
					)

			inst = self.dpGames[self.senderID][self.groupchat_name_complete]
			await inst.redirect_command(inst, self.command)

	async def verify_perm(self, senderID):
		if senderID in self.hosts_groupchats:
			rooms = self.hosts_groupchats[senderID]
		else:
			return "INVALID"

		if self.groupchat_name_complete not in rooms:
			return "INVALIDROOM"
