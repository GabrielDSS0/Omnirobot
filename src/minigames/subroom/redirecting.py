from src.vars import Varlist
from src.sending import call_command

def joinRoom():
    websocket = Varlist.websocket
    invite = Varlist.content.split(" ")

    room = invite[1].strip()
    host = room.split("-")[1]
    if host in Varlist.hosts_groupchats:
        groupchats: list  = Varlist.hosts_groupchats[host] 
        Varlist.hosts_groupchats[host] = groupchats.append(host)
    else:
        Varlist.hosts_groupchats[host] = [room]

    call_command(websocket.send(f"|/join {room}"))