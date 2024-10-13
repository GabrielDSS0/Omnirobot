from src.vars import Varlist
from src.sending import *

class Server_Messages():
    def __init__(self):
        self.msgSplited = Varlist.msgSplited
        self.websocket = Varlist.websocket
    
    def check(self):
        if len(self.msgSplited) > 2:
            if self.msgSplited[0].strip():
                if self.msgSplited[0].strip().startswith(">") and self.msgSplited[1] == "expire":
                    room = self.msgSplited[0][1:].strip()
                    dpGames = Varlist.dpGames.copy()
                    for host in dpGames:
                        rooms = Varlist.hosts_groupchats[host]
                        if room in rooms:
                            del Varlist.dpGames[host][room]
                            Varlist.hosts_groupchats[host].remove(room)
                        if not (Varlist.dpGames[host]):
                            del Varlist.dpGames[host]
                            del Varlist.hosts_groupchats[host]