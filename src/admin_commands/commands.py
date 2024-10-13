import subprocess

from websockets.exceptions import ConnectionClosed

from src.vars import Varlist
from src.sending import respondPM

class Admin_Commands():
    def __init__(self):
        self.senderID = Varlist.senderID
    
    def redirect_command(self, inst, name_func):
        func = getattr(inst, name_func)
        func()

    def kill(self):
        raise ConnectionClosed(None, None)
    
    def gitpull(self):
        command = ["git", "pull"]
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        results = (output.stdout + output.stderr).decode('utf-8')
        respondPM(self.senderID, f"!code {results}")