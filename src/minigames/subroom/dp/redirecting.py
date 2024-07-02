from config  import *
from src.vars import Varlist
from src.commands_list import commands_dp

from src.minigames.subroom.dp.playing.game import *

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = Varlist.websocket

        self.room = Varlist.room
        self.senderID = Varlist.senderID
        self.msgType = Varlist.msgType

        self.command = Varlist.command
        self.commandParams = Varlist.commandParams

        self.dpGames = Varlist.dpGames

    async def redirect_to_function(self):
        command_permission = commands_dp[self.command]['perm']

        if command_permission == 'host':
            if self.senderID not in self.dpGames or not (self.room in self.dpGames[self.senderID]):
                dpGame: GameCommands = GameCommands(self.senderID)
                Varlist.host = self.senderID
                if not (self.senderID in self.dpGames):
                    self.dpGames[self.senderID] =  {
                        self.room: dpGame
                    }
                else:
                    self.dpGames[self.senderID].update({
                        self.room: dpGame
                    })

            inst = self.dpGames[self.senderID][self.room]
            inst.redirect_command(inst, self.command)