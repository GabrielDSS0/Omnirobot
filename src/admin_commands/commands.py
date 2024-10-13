from websockets.exceptions import ConnectionClosed

from src.vars import Varlist

class Admin_Commands():
    def __init__(self):
        self.senderID = Varlist.senderID
    
    def redirect_command(self, inst, name_func):
        func = getattr(inst, name_func)
        func()

    def kill(self):
        raise ConnectionClosed(None, None)