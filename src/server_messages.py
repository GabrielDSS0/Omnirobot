import src.vars as vars


class Server_Messages:
	def __init__(self):
		self.msgSplited = vars.Varlist.msgSplited
		self.websocket = vars.Varlist.websocket

	def check(self):
		if len(self.msgSplited) > 2:
			if self.msgSplited[0].strip():
				if (
					self.msgSplited[0].strip().startswith(">")
					and self.msgSplited[1] == "expire"
				):
					room = self.msgSplited[0][1:].strip()
					dpGames = vars.Varlist.dpGames.copy()
					for host in dpGames:
						rooms = vars.Varlist.hosts_groupchats[host]
						if room in rooms:
							del vars.Varlist.dpGames[host][room]
							vars.Varlist.hosts_groupchats[host].remove(room)
						if not (vars.Varlist.dpGames[host]):
							del vars.Varlist.dpGames[host]
							del vars.Varlist.hosts_groupchats[host]
