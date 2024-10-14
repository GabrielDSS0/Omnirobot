import threading
import html
import inspect
import json

from bs4 import BeautifulSoup
from psclient import toID

from config import username, commands_file
from src.sending import *
from src.vars import Varlist

class Misc_Commands():
    def __init__(self):
        self.websocket = Varlist.websocket
        self.msgType = Varlist.msgType
        self.room = Varlist.room
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID

        self.sql_commands = Varlist.sql_commands

    async def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.command = Varlist.command
        self.commandParams = Varlist.commandParams
        func = getattr(inst, name_func)
        isAsync = inspect.iscoroutinefunction(func)
        if not isAsync:
            func()
        else:
            await func()

    async def query(self, type, params):
        call_command(self.websocket.send(f"|/query {type} {params}"))
        response = str(await self.websocket.recv()).split("|")
        if len(response) > 2:
            while response[1] != "queryresponse" and response[2] != type:
                response = str(await self.websocket.recv()).split("|")

            return response
    
    async def commands(self):
        response_user_rooms = await self.query("userdetails", f"{self.senderID}")

        user_rooms = set((json.loads(response_user_rooms[3])['rooms'].keys()))
        
        response_bot_rooms = await self.query("userdetails", f"{username}")

        bot_rooms = set((json.loads(response_bot_rooms[3])['rooms'].keys()))

        for room in bot_rooms:
            bot_room = toID(room)
            for user_room in user_rooms:
                user_room = toID(user_room)
                if user_room == bot_room:
                    with open(commands_file, "r", encoding="utf-8") as html_file:
                        html_content = html_file.read()
                        converted = BeautifulSoup(html_content, "html.parser")
                        html_done = html.unescape(str(converted).replace("\n", ""))

                        call_command(self.websocket.send(f"{bot_room}|/pmuhtml {self.senderID},htmlcommands,{html_done}"))
                        return
        
        respondPM(self.sender, "Você não está em uma sala em comum com o bot.")

    def addpoints(self, newPoints=1, fromRespond=False):
        if self.msgType:
            points_receiver = self.commandParams[0] if self.msgType == "room" else self.commandParams[1]
            username_id = toID(points_receiver)
            newPoints = self.commandParams[-1].strip()
            try:
                newPoints = float(newPoints)
            except:
                return respond(self.msgType, "A pontuação digitada não é um número.", self.senderID, self.room)
        else:
            points_receiver = self.sender
            username_id = self.senderID

        idRoom_fetch = self.sql_commands.select_idroom_by_nameid(self.room)
        idUser_fetch = self.sql_commands.select_iduser_by_nameid(username_id)

        room = idRoom_fetch[0][0]

        if idUser_fetch:
            user = idUser_fetch[0][0]

            user_room_lb = self.sql_commands.select_userpoints_leaderboard(user, room)
            
            if user_room_lb:
                points = user_room_lb[0][0] + newPoints
                if points <= 0:
                    self.sql_commands.delete_user_from_leaderboard(user, room)
                else:
                    self.sql_commands.update_userpoints_leaderboard(points, user, room)
            else:
                if newPoints <= 0:
                    return respond(self.msgType, "Só se pode adicionar valores de pontos maiores que 0.", self.senderID, self.room)

                self.sql_commands.insert_leaderboard(user, room, newPoints)
        else:
            self.sql_commands.insert_user(points_receiver)
            user = self.sql_commands.select_iduser_by_nameid(username_id)[0][0]

            if newPoints <= 0:
                return respond(self.msgType, "Só se pode adicionar valores de pontos maiores que 0.", self.senderID, self.room)

            self.sql_commands.insert_leaderboard(user, room, newPoints)

        if not fromRespond:
            respond(self.msgType, "Pontos adicionados! 111", self.senderID, self.room)

    def removepoints(self, remPoints=1):
        if self.msgType:
            points_receiver = self.commandParams[0] if self.msgType == "room" else self.commandParams[1]
            username_id = toID(points_receiver)
            remPoints = self.commandParams[-1].strip()
            try:
                remPoints = float(remPoints)
            except:
                return respond(self.msgType, "A pontuação digitada não é um número.", self.senderID, self.room)
        else:
            username_id = self.senderID

        idRoom_fetch = self.sql_commands.select_idroom_by_nameid(self.room)
        idUser_fetch = self.sql_commands.select_iduser_by_nameid(username_id)

        room = idRoom_fetch[0][0]

        if idUser_fetch:
            user = idUser_fetch[0][0]

            user_room_lb = self.sql_commands.select_userpoints_leaderboard(user, room)

            if user_room_lb:
                points = user_room_lb[0][0] - remPoints
                if points <= 0:
                    self.sql_commands.delete_user_from_leaderboard(user, room)
                else:
                    self.sql_commands.update_userpoints_leaderboard(points, user, room)
            else:
                return respond(self.msgType, "O usuário citado não tem pontos nesta sala.", self.senderID, self.room)
        else:
            return respond(self.msgType, "O usuário citado não tem pontos nesta sala.", self.senderID, self.room)

        respond(self.msgType, "Pontos removidos!", self.senderID, self.room)

    def clearpoints(self):
        idRoom_fetch = self.sql_commands.select_idroom_by_nameid(self.room)
        room = idRoom_fetch[0][0]
        self.sql_commands.clear_leaderboard(room)
        respond(self.msgType, "Pontos da sala limpos!", self.senderID, self.room)
    
    def leaderboard(self, inQuestion=False):
        idRoom = self.sql_commands.select_idroom_by_nameid(self.room)[0][0]
        lb_fetch = self.sql_commands.select_all_leaderboard(idRoom)
        lb = {}

        if inQuestion:
            self.msgType = "room"

        code = ""

        for data in lb_fetch:
            userID = data[1]
            user = self.sql_commands.select_username_by_iduser(userID)[0][0]
            points = data[2]
            if int(points) == points:
                points = int(points)
            lb[user] = points

        lbSequenceSorted = dict(sorted(lb.items(), key=lambda item: item[1], reverse=True))

        if self.msgType == "pm":
            code = "!code Leaderboard:\n"
            for user in lbSequenceSorted:
                points = lbSequenceSorted[user]
                code += f"{user} - {points} pontos"
                if not user == list(lbSequenceSorted)[-1]:
                    code += "\n"
        
        elif self.msgType == "room":
            code = """/addhtmlbox <div class="infobox"> <h3> Leaderboard </h3> <hr>
            """
            for user in lbSequenceSorted:
                points = lbSequenceSorted[user]
                code += f"<b> {user}: </b> {points}"
                if not user == list(lbSequenceSorted)[-1]:
                    code += ','
            code += "</hr></div>"

        respond(self.msgType, code, self.senderID, self.room)
    
    def timer(self):
        time = self.commandParams[0]
        try:
            time = float(time)
        except:
            return respond(self.msgType, "O tempo inserido não é um número.", self.senderID, self.room)

        unit = toID(self.commandParams[-1])

        if not (unit == "min" or unit == "sec"):
            return respond(self.msgType, "A unidade de medida deve ser ou min ou sec.", self.senderID, self.room)
        
        if unit == "min":
            time *= 60

        respond(self.msgType, "Timer iniciado!", self.senderID, self.room)

        timer_thread = threading.Timer(time, respond, args=[self.msgType, "Tempo batido!", self.senderID, self.room])

        timer_thread.start()
