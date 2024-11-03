import src.vars as vars
import src.sending as sending
import config

def joinRoom():
    websocket = vars.Varlist.websocket
    invite = vars.Varlist.content.split(" ")

    room = invite[1].strip()
    host = room.split("-")[1]
    if host in vars.Varlist.hosts_groupchats:
        groupchats: list = vars.Varlist.hosts_groupchats[host]
        groupchats.append(room)
        vars.Varlist.hosts_groupchats[host] = groupchats
        vars.Varlist.hosts_groupchats[config.owner] = groupchats
    else:
        vars.Varlist.hosts_groupchats[host] = [room]
        vars.Varlist.hosts_groupchats[config.owner] = groupchats

    sending.call_command(websocket.send(f"|/join {room}"))