from config import *
from src.vars import Varlist
from src.commands_list import commands_dp

from src.minigames.subroom.dp.playing.game import *

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = Varlist.websocket

        self.groupchat_name_complete = Varlist.groupchat_name_complete
        self.senderID = Varlist.senderID
        self.msgType = Varlist.msgType

        self.command = Varlist.command
        self.commandParams = Varlist.commandParams

        self.hosts_groupchats = Varlist.hosts_groupchats
        self.dpGames = Varlist.dpGames

    async def redirect_to_function(self):
        if self.senderID in self.hosts_groupchats:
            if len(self.hosts_groupchats[self.senderID]) == 1:
                self.groupchat_name_complete = self.hosts_groupchats[self.senderID][0]

        command_permission = commands_dp[self.command]['perm']
        command_params_default = commands_dp[self.command]['params']
        need_room = commands_dp[self.command]['need_room']

        if need_room and self.msgType == "room" and len(self.commandParams) < (len(command_params_default) - 1):
            return respondRoom(f"Uso: {prefix}{self.command} **{', '.join(command_params_default[1:])}**", self.groupchat_name_complete)

        elif need_room and self.msgType != "room" and len(self.commandParams) < len(command_params_default) and len(self.hosts_groupchats[self.senderID]) > 1:
            return respond(self.msgType, f"Uso: {prefix}{self.command} **{', '.join(command_params_default)}**", self.senderID, self.groupchat_name_complete)

        if command_permission == "host" or command_permission == "adm" or (command_permission == "general" and self.msgType == "room"):
            permission = await self.verify_perm(self.senderID)
            if permission == "INVALID":
                return respondPM(self.senderID, "Você não tem permissão para executar este comando.")

            elif permission == "INVALIDROOM":
                return respondPM(self.senderID, "O bot não está nessa room.")

        if commands_dp[self.command]['type'] == 'pm' and self.msgType == 'room':
            return respondPM(self.senderID, "Este comando deve ser executado somente por PM.")

        if command_permission == 'host':
            if self.senderID not in self.dpGames or not (self.groupchat_name_complete in self.dpGames[self.senderID]):
                dpGame: GameCommands = GameCommands(self.senderID, self.groupchat_name_complete)
                Varlist.host = self.senderID
                if not (self.senderID in self.dpGames):
                    self.dpGames[self.senderID] =  {
                        self.groupchat_name_complete: dpGame
                    }
                else:
                    self.dpGames[self.senderID].update({
                        self.groupchat_name_complete: dpGame
                    })

            inst = self.dpGames[self.senderID][self.groupchat_name_complete]
            inst.redirect_command(inst, self.command)

    async def verify_perm(self, senderID):
        if senderID in self.dpGames:
            rooms = self.dpGames[senderID]
        elif senderID in self.hosts_groupchats:
            rooms = self.hosts_groupchats[senderID]
        else:
            return "INVALID"

        if self.groupchat_name_complete in rooms:
            call_command(self.websocket.send(f"|/query roominfo {self.groupchat_name_complete}"))
            response = str(await self.websocket.recv()).split("|")
            if len(response) > 2:
                while response[1] != "queryresponse" and response[2] != "roominfo":
                    response = str(await self.websocket.recv()).split("|")

                auths = list((json.loads(response[3])['auth'].values()))

            substringSender = f"{senderID}"

            for group in auths:
                if substringSender in group:
                    return True
            return "INVALID"
        else:
            return "INVALIDROOM"