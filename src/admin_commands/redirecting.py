

import config
import src.vars as vars
import src.sending as sending
import src.admin_commands.commands as adm_commands

from psclient import toID

class RedirectingFunction():
    def __init__(self) -> None:
        self.websocket = vars.Varlist.websocket

        self.senderID = vars.Varlist.senderID
        self.command = vars.Varlist.command


    async def redirect_to_function(self):
        if self.senderID != toID(config.owner):
            return sending.respondPM(self.senderID, "Você não tem permissão.")

        inst = adm_commands.Admin_Commands()
        inst.redirect_command(inst, self.command)