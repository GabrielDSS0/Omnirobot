from psclient import toID

from src.sending import *
from src.vars import Varlist

class Leaderboard_Commands():
    def __init__(self):
        self.msgType = Varlist.msgType
        self.room = Varlist.room
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID

        self.sql_commands = Varlist.sql_commands

    def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.command = Varlist.command
        self.commandParams = Varlist.commandParams
        func = getattr(inst, name_func)
        func()
    
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
            respond(self.msgType, "Pontos adicionados!", self.senderID, self.room)

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