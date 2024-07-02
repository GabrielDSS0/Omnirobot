from src.vars import Varlist
from src.sending import call_command

def joinRoom():
    websocket = Varlist.websocket
    invite = Varlist.content.split(" ")
    
    room = invite[1].strip()

    call_command(websocket.send(f"|/join {room}"))