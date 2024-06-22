import json

from config  import *
from src.vars import Varlist
from src.commands_list import commands_mq

from src.minigames.room.megaquiz.playing.game import *
from src.minigames.room.megaquiz.playing.other import *

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = Varlist.websocket

        self.room = Varlist.room
        self.senderID = Varlist.senderID
        self.msgType = Varlist.msgType

        self.command = Varlist.command
        self.commandParams = Varlist.commandParams

        self.questions = Varlist.questions

    async def redirect_to_function(self):
        command_permission = commands_mq[self.command]['perm']
        command_params_default = commands_mq[self.command]['params']
        need_room = commands_mq[self.command]['need_room']

        if need_room and self.msgType == "room" and len(self.commandParams) < (len(command_params_default) - 1):
            return respondRoom(f"Uso: {prefix}{self.command} **{', '.join(command_params_default[1:])}**", self.room)
        
        elif need_room and self.msgType != "room" and len(self.commandParams) < len(command_params_default):
            return respond(self.msgType, f"Uso: {prefix}{self.command} **{', '.join(command_params_default)}**", self.senderID, self.room)

        if command_permission == "host" or command_permission == "adm" or (command_permission == "general" and self.msgType == "room"):
            permission = await self.verify_perm(self.room, self.senderID)
            if permission == "INVALID":
                return respondPM(self.senderID, "Você não tem permissão para executar este comando.")

            elif permission == "INVALIDROOM":
                return respondPM(self.senderID, "O bot não está nessa room.")

        if commands_mq[self.command]['type'] == 'pm' and self.msgType == 'room':
            return respondPM(self.senderID, "Este comando deve ser executado somente por PM.")

        if command_permission == 'host':
            if self.senderID not in self.questions or not (self.room in self.questions[self.senderID]):
                question: GameCommands = GameCommands(self.senderID)
                Varlist.host = self.senderID
                if not (self.senderID in self.questions):
                    self.questions[self.senderID] =  {
                        self.room: question
                    }
                else:
                    self.questions[self.senderID].update({
                        self.room: question
                    })

            inst = self.questions[self.senderID][self.room]
            inst.redirect_command(inst, self.command)

        elif commands_mq[self.command]['perm'] == 'user':
            hoster = name_to_id(self.commandParams[1])
            if hoster in self.questions:
                inst = self.questions[self.senderID][self.room]
                inst.redirect_command(inst, self.command)

        elif commands_mq[self.command]['perm'] == 'adm':
            inst = OtherCommands()
            inst.redirect_command(inst, self.command)

    async def verify_perm(self, room, senderID):
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