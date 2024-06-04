import json

from config import *
from src.vars import Varlist
from src.commands_list import commands_leaderboard

from src.leaderboard.commands import *

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = Varlist.websocket
        self.db = Varlist.db
        self.cursor = Varlist.cursor

        self.msgSplited = Varlist.msgSplited

        self.room = Varlist.room
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.msgType = Varlist.msgType

        self.command = Varlist.command
        self.commandParams = Varlist.commandParams

        self.questions = Varlist.questions
        self.questionsRoom = Varlist.questionsRoom

    async def redirect_to_function(self):
        command_permission = commands_leaderboard[self.command]['perm']

        if command_permission == "adm" or (command_permission == "general" and self.msgType == "room"):
            permission = await self.verify_perm(self.room, self.senderID)
            if permission == "INVALID":
                respondPM(self.senderID, "Você não tem permissão para executar este comando.")
                return self.return_question()

            elif permission == "INVALIDROOM":
                respondPM(self.senderID, "O bot não está nessa room.")
                return self.return_question()

        inst = Leaderboard_Commands()
        inst.redirect_command(inst, self.command)

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