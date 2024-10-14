import json

import src.vars as vars
import src.commands_list as cmd_list
import config

import src.misc_commands.commands as src_misc
import src.sending as sending

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = vars.Varlist.websocket

        self.room = vars.Varlist.room
        self.senderID = vars.Varlist.senderID
        self.msgType = vars.Varlist.msgType

        self.command = vars.Varlist.command
        self.commandParams = vars.Varlist.commandParams

    async def redirect_to_function(self):
        command_permission = cmd_list.commands_misc[self.command]['perm']
        command_params_default = cmd_list.commands_misc[self.command]['params']
        need_room = cmd_list.commands_misc[self.command]['need_room']

        if need_room and self.msgType == "room" and len(self.commandParams) < (len(command_params_default) - 1):
            return sending.respondRoom(f"Uso: {config.prefix}{self.command} **{', '.join(command_params_default[1:])}**", self.room)
        
        elif need_room and self.msgType != "room" and len(self.commandParams) < len(command_params_default):
            return sending.respond(self.msgType, f"Uso: {config.prefix}{self.command} **{', '.join(command_params_default)}**", self.senderID, self.room)

        if command_permission == "adm" or (command_permission == "general" and self.msgType == "room"):
            permission = await self.verify_perm(self.room, self.senderID)
            if permission == "INVALID":
                return sending.respondPM(self.senderID, "Você não tem permissão para executar este comando.")

            elif permission == "INVALIDROOM":
                return sending.respondPM(self.senderID, "O bot não está nessa room.")


        inst = src_misc.Misc_Commands()
        await inst.redirect_command(inst, self.command)

    async def verify_perm(self, room, senderID):
        rooms = config.rooms.copy()

        if senderID in vars.Varlist.hosts_groupchats:
            rooms.extend(vars.Varlist.hosts_groupchats[senderID])
    
        if room in rooms:
            sending.call_command(self.websocket.send(f"|/query roominfo {room}"))
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