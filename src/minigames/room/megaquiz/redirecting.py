import json

import src.vars as vars
import src.commands_list as cmd_list
import src.sending as sending
import config

import src.minigames.room.megaquiz.playing.game as mq_game
import src.minigames.room.megaquiz.playing.other as mq_other

from psclient import toID

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = vars.Varlist.websocket

        self.room = vars.Varlist.room
        self.senderID = vars.Varlist.senderID
        self.msgType = vars.Varlist.msgType

        self.command = vars.Varlist.command
        self.commandParams = vars.Varlist.commandParams

        self.questions = vars.Varlist.questions

    async def redirect_to_function(self):
        if self.senderID in self.questions:
            if len(self.questions[self.senderID]) == 1:
                self.room = list(self.questions[self.senderID])[0]

        command_permission = cmd_list.commands_mq[self.command]['perm']
        command_params_default = cmd_list.commands_mq[self.command]['params']
        need_room = cmd_list.commands_mq[self.command]['need_room']

        if need_room and self.msgType == "room" and len(self.commandParams) < (len(command_params_default) - 1):
            return sending.respondRoom(f"Uso: {config.prefix}{self.command} **{', '.join(command_params_default[1:])}**", self.room)
        
        elif need_room and self.msgType != "room" and len(self.commandParams) < len(command_params_default) and self.senderID not in self.questions:
            return sending.respond(self.msgType, f"Uso: {config.prefix}{self.command} **{', '.join(command_params_default)}**", self.senderID, self.room)

        if command_permission == "host" or command_permission == "adm" or (command_permission == "general" and self.msgType == "room"):
            permission = await self.verify_perm(self.room, self.senderID)
            if permission == "INVALID":
                return sending.respondPM(self.senderID, "Você não tem permissão para executar este comando.")

            elif permission == "INVALIDROOM":
                return sending.respondPM(self.senderID, "O bot não está nessa room.")

        if cmd_list.commands_mq[self.command]['type'] == 'pm' and self.msgType == 'room':
            return sending.respondPM(self.senderID, "Este comando deve ser executado somente por PM.")

        if command_permission == 'host':
            if self.senderID not in self.questions and self.command != "makequestion":
                return sending.respondPM(self.senderID, "Não há uma questão ativa na sala atualmente.")
        
            if self.senderID in self.questions and self.command == "makequestion":
                return sending.respondPM(self.senderID, "Você já está com uma questão aberta. Caso queira cancelar, digite @cancelquestion.")

            if self.senderID not in self.questions or not (self.room in self.questions[self.senderID]) and self.command == "makequestion":
                question: mq_game.GameCommands = mq_game.GameCommands(self.senderID)
                vars.Varlist.host = self.senderID
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

        elif cmd_list.commands_mq[self.command]['perm'] == 'user':
            hoster = toID(self.commandParams[1])
            if hoster in self.questions:
                inst = self.questions[hoster][self.room]
                inst.redirect_command(inst, self.command)

        elif cmd_list.commands_mq[self.command]['perm'] == 'adm':
            inst = mq_other.OtherCommands()
            inst.redirect_command(inst, self.command)

    async def verify_perm(self, room, senderID):
        rooms = config.rooms
        
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