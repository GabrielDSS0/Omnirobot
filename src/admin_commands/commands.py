import importlib
import sys
import subprocess

from src.vars import Varlist
from src.sending import respondPM

class Admin_Commands():
    def __init__(self):
        self.senderID = Varlist.senderID
    
    def redirect_command(self, inst, name_func):
        func = getattr(inst, name_func)
        func()

    def kill(self):
        sys.exit()
    
    def gitpull(self):
        command = ["git", "pull"]
        output_git = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        results_git = (output_git.stdout + output_git.stderr).decode('utf-8').strip()

        respondPM(self.senderID, f"!code {results_git}")

        if results_git == "Already up to date.":
            return

        results_git = results_git.split("\n")
        
        for result in results_git:
            if result.startswith(" "):
                pipes = result.count("|")
                if not pipes:
                    continue
                result = result.split("|", 1)[0].strip()
                result = result.replace("/", ".")
                result = result.replace(".py", "")

                module = __import__(result)
                importlib.reload(module)