import asyncio

import src.vars as vars


def call_command(command):
	try:
		asyncio.get_event_loop().is_running()
	except RuntimeError:
		return asyncio.run(command)
	return asyncio.gather(command)


def respondRoom(message, room):
	websocket = vars.Varlist.websocket
	try:
		asyncio.get_event_loop().is_running()
	except RuntimeError:
		return asyncio.run(websocket.send(f"{room}|{message}"))
	return asyncio.gather(websocket.send(f"{room}|{message}"))


def respondPM(user, message):
	websocket = vars.Varlist.websocket
	try:
		asyncio.get_event_loop().is_running()
	except RuntimeError:
		return asyncio.run(websocket.send(f"|/pm {user}, {message}"))
	return asyncio.gather(websocket.send(f"|/pm {user}, {message}"))


def respond(msgType, message, user=None, room=None):
	if msgType == "pm":
		respondPM(user, message)
	elif msgType == "room":
		respondRoom(message, room)


async def query(type, params):
	websocket = vars.Varlist.websocket

	await websocket.send(f"|/query {type} {params}")
	response = str(await websocket.recv()).split("|")
	if len(response) > 2:
		while response[1] != "queryresponse" and response[2] != type:
			response = str(await websocket.recv()).split("|")

		return response
