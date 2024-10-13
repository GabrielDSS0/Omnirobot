import json

from config import *
from src.vars import Varlist
from src.commands_list import commands_misc

from src.misc_commands.commands import *

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = Varlist.websocket

        self.room = Varlist.room
        self.senderID = Varlist.senderID
        self.msgType = Varlist.msgType

        self.command = Varlist.command
        self.commandParams = Varlist.commandParams

    async def redirect_to_function(self):
        command_permission = commands_misc[self.command]['perm']
        command_params_default = commands_misc[self.command]['params']
        need_room = commands_misc[self.command]['need_room']

        if need_room and self.msgType == "room" and len(self.commandParams) < (len(command_params_default) - 1):
            return respondRoom(f"Uso: {prefix}{self.command} **{', '.join(command_params_default[1:])}**", self.room)
        
        elif need_room and self.msgType != "room" and len(self.commandParams) < len(command_params_default):
            return respond(self.msgType, f"Uso: {prefix}{self.command} **{', '.join(command_params_default)}**", self.senderID, self.room)

        if command_permission == "adm" or (command_permission == "general" and self.msgType == "room"):
            permission = await self.verify_perm(self.room, self.senderID)
            if permission == "INVALID":
                return respondPM(self.senderID, "Você não tem permissão para executar este comando.")

            elif permission == "INVALIDROOM":
                return respondPM(self.senderID, "O bot não está nessa room.")


        inst = Misc_Commands()
        await inst.redirect_command(inst, self.command)

    async def verify_perm(self, room, senderID):
        if senderID in Varlist.hosts_groupchats:
            rooms.extend(Varlist.hosts_groupchats[senderID])
    
        if room in rooms:
            call_command(self.websocket.send(f"|/query roominfo {room}"))
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