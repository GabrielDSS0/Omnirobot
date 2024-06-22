from src.vars import Varlist
from src.sending import call_command

def joinRoom():
    websocket = Varlist.websocket
    dpGames = Varlist.dpGames
    invite = Varlist.content.split(" ")
    
    room = invite[1].strip()
    roomHost = room.split("-")[1]

    call_command(websocket.send(f"|/join {room}"))

    if not (roomHost in dpGames):
        Varlist.subroomGames[roomHost] =  {
            room: None
        }
    else:
        Varlist.subroomGames[roomHost].update({
            room: None
        })