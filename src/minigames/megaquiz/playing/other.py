from src.sending import *
from src.vars import Varlist

class OtherCommands():
    def __init__(self):
        self.msgSplited = Varlist.msgSplited
        self.websocket = Varlist.websocket
        self.db = Varlist.db
        self.cursor = Varlist.cursor
        self.msgType = Varlist.msgType
        self.room = Varlist.room

        self.sql_commands = Varlist.sql_commands

    def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.command = Varlist.command
        self.commandParams = Varlist.commandParams
        func = getattr(inst, name_func)
        func()

    def definetimer(self):
        timer = self.commandParams[-1]
        self.sql_commands.update_timer(timer, self.room)
        respond(self.msgType, f"O tempo foi alterado para {timer} segundos!", self.senderID, self.room)