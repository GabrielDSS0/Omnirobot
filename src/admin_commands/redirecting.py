

from config import owner
from src.vars import Varlist

from src.sending import respondPM
from src.admin_commands.commands import *

from psclient import toID

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = Varlist.websocket

        self.senderID = Varlist.senderID
        self.command = Varlist.command


    async def redirect_to_function(self):
        if self.senderID != toID(owner):
            return respondPM(self.senderID, "Você não tem permissão.")

        inst = Admin_Commands()
        inst.redirect_command(inst, self.command)