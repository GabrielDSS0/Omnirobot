from config  import *
from src.vars import Varlist
from src.commands_list import commands_dp

from src.minigames.subroom.dp.playing.game import *

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = Varlist.websocket

        self.room = Varlist.room
        self.groupchat_simplified = Varlist.groupchat_name_simplified
        self.senderID = Varlist.senderID
        self.msgType = Varlist.msgType

        self.command = Varlist.command
        self.commandParams = Varlist.commandParams

        self.dpGames = Varlist.dpGames

    async def redirect_to_function(self):
        command_permission = commands_dp[self.command]['perm']

        if command_permission == 'host':
            if self.senderID not in self.dpGames or not (self.groupchat_simplified in self.dpGames[self.senderID]):
                dpGame: GameCommands = GameCommands(self.senderID, self.groupchat_simplified)
                Varlist.host = self.senderID
                if not (self.senderID in self.dpGames):
                    self.dpGames[self.senderID] =  {
                        self.groupchat_simplified: dpGame
                    }
                else:
                    self.dpGames[self.senderID].update({
                        self.groupchat_simplified: dpGame
                    })

            inst = self.dpGames[self.senderID][self.groupchat_simplified]
            inst.redirect_command(inst, self.command)