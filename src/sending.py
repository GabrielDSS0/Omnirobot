import asyncio

from src.vars import Varlist

def call_command(command):
    websocket = Varlist.websocket
    try:
        asyncio.get_event_loop().is_running()
    except RuntimeError:
        return asyncio.run(command)
    return asyncio.gather(command)

def respondRoom(message, room):
    websocket = Varlist.websocket
    try:
        asyncio.get_event_loop().is_running()
    except RuntimeError:
        return asyncio.run(websocket.send(f"{room}|{message}"))
    return asyncio.gather(websocket.send(f"{room}|{message}"))

def respondPM(user, message):
    websocket = Varlist.websocket
    try:
        asyncio.get_event_loop().is_running()
    except RuntimeError:
        return asyncio.run(websocket.send(f"|/pm {user}, {message}"))
    return asyncio.gather(websocket.send(f"|/pm {user}, {message}"))

def respond(msgType, message, user=None, room=None):
    websocket = Varlist.websocket
    if msgType == "pm":
        respondPM(user, message, websocket)
    elif msgType == "room":
        respondRoom(message, websocket, room)