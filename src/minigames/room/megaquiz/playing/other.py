import src.sending as sending
import src.vars as vars

class OtherCommands():
    def __init__(self):
        self.msgType = vars.Varlist.msgType
        self.room = vars.Varlist.room

        self.sql_commands = vars.Varlist.sql_commands

    def redirect_command(self, inst, name_func: str):
        self.sender = vars.Varlist.sender
        self.senderID = vars.Varlist.senderID
        self.command = vars.Varlist.command
        self.commandParams = vars.Varlist.commandParams
        func = getattr(inst, name_func)
        func()

    def definetimer(self):
        timer = self.commandParams[-1]
        try:
            timer = float(timer)
        except:
            return sending.respond(self.msgType, "O tempo inserido não é um número.", self.senderID, self.room)
        
        if timer <= 0:
            return sending.respond(self.msgType, "O tempo inserido não é um número positivo.", self.senderID, self.room)

        self.sql_commands.update_timer(timer, self.room)
        sending.respond(self.msgType, f"O tempo foi alterado para {timer} segundos!", self.senderID, self.room)