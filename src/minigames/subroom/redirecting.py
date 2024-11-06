import src.vars as vars
import src.sending as sending

def joinRoom():
    websocket = vars.Varlist.websocket
    invite = vars.Varlist.content.split(" ")

    room = invite[1].strip()
    host = vars.Varlist.senderID
    if host in vars.Varlist.hosts_groupchats:
        groupchats: list = vars.Varlist.hosts_groupchats[host]
        groupchats.append(room)
        vars.Varlist.hosts_groupchats[host] = groupchats
    else:
        vars.Varlist.hosts_groupchats[host] = [room]

    sending.call_command(websocket.send(f"|/join {room}"))