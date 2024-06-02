import json

from config  import *
from src.vars import Varlist
from src.commands_list import commands_mq

from src.minigames.megaquiz.playing.game import *
from src.minigames.megaquiz.playing.other import *

from showdown.utils import name_to_id

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = Varlist.websocket
        self.db = Varlist.db
        self.cursor = Varlist.cursor

        self.msgSplited = Varlist.msgSplited

        self.room = Varlist.room
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.content = Varlist.content
        self.msgType = Varlist.msgType

        self.command = Varlist.command
        self.commandParams = Varlist.commandParams

        self.questions = Varlist.questions
        self.questionsRoom = Varlist.questionsRoom

    async def redirect_to_function(self):
        command_permission = commands_mq[self.command]['perm']

        if command_permission == "host" or command_permission == "adm" or (command_permission == "general" and self.msgType == "room"):
            permission = await self.verify_perm(self.room, self.senderID)
            if permission == "INVALID":
                await self.websocket.send(f"|/pm {self.senderID}, Você não tem permissão para executar este comando.")
                return self.return_question()

            elif permission == "INVALIDROOM":
                await self.websocket.send(f"|/pm {self.senderID}, O bot não está nessa room.")
                return self.return_question()

        if commands_mq[self.command]['type'] == 'pm' and self.msgType == 'room':
            await self.websocket.send(f"|/pm {self.senderID}, Este comando deve ser executado somente por PM.")
            return self.return_question()

        if command_permission == 'host':
            if self.senderID not in self.questions:
                question: GameCommands = GameCommands(self.senderID)
                Varlist.host = self.senderID
                self.questions[self.senderID] =  {
                    self.room: question
                }
            
            inst = self.questions[self.senderID][self.room]
            await inst.redirect_command(inst, self.command)

        elif commands_mq[self.command]['perm'] == 'user':
            hoster = name_to_id(self.commandParams[1])
            if hoster in self.questions:
                inst = self.questions[self.senderID][self.room]
                await inst.redirect_command(inst, self.command)

        elif commands_mq[self.command]['perm'] == 'adm':
            inst = OtherCommands()
            await inst.redirect_command(inst, self.command)

        elif commands_mq[self.command]['perm'] == 'general':
            inst = OtherCommands()
            await inst.redirect_command(inst, self.command)

        return self.return_question()

    async def verify_perm(self, room, senderID):
        if room in rooms:
            await self.websocket.send(f"|/query roominfo {room}")
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

    def return_question(self):
        Varlist.questions = self.questions
        Varlist.questionsRoom = self.questionsRoom