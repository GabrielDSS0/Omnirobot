from config import prefix

from src.sending import *
from src.vars import Varlist

class OtherCommands():
    def __init__(self):
        self.msgSplited = Varlist.msgSplited
        self.websocket = Varlist.websocket
        self.db = Varlist.db
        self.cursor = Varlist.cursor
        self.msgType = Varlist.msgType
        self.room = Varlist.room

        self.sql_commands = Varlist.sql_commands

    def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.command = Varlist.command
        self.commandParams = Varlist.commandParams
        func = getattr(inst, name_func)
        func()

    def definetimer(self):
        timer = self.commandParams[-1]
        self.sql_commands.update_timer(timer, self.room)
        respond(self.msgType, f"O tempo foi alterado para {timer} segundos!", self.senderID, self.room)
    
    def addpoints(self, newPoints=1, fromRespond=False):
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
                self.sql_commands.update_userpoints_leaderboard(points, user, room)
            else:
                self.sql_commands.insert_leaderboard(user, room, newPoints)
        else:
            self.sql_commands.insert_user(points_receiver)
            user = self.sql_commands.select_iduser_by_nameid(username_id)[0][0]

            self.sql_commands.insert_leaderboard(user, room, newPoints)

        if not fromRespond:
            respond(self.msgType, "Pontos adicionados!", self.senderID, self.room)

    def removepoints(self, remPoints=1):
        username_id = self.senderID
        remPoints = self.commandParams[1]
        try:
            remPoints = float(remPoints)
        except:
            return respond(self.msgType, f"Uso do comando: {prefix}rpoints [usuario], [pontos], [sala]", self.senderID, self.room)

        self.cursor.execute(f"""SELECT idUser FROM tbl_leaderboard WHERE idUser IN (SELECT idUser FROM tbl_user WHERE name_id = '{username_id}')
        """)

        userID = self.cursor.fetchall()
        user = userID[0][0]
        self.cursor.execute(f"""SELECT points FROM tbl_leaderboard WHERE idUser = '{user}'
        """)

        points = self.cursor.fetchall()[0][0] - remPoints

        self.cursor.execute(f"""UPDATE roomLB SET points = {points} WHERE user = '{user}' and roomNAME = '{self.room}'
        """)
        if points <= 0:
                self.cursor.execute(f"""
                DELETE FROM roomLB WHERE idUser = '{user}' and roomNA = '{self.room}'
                """)

        if self.command == "rpoints":
            respond(self.msgType, "Pontos removidos!", self.senderID, self.room)

        self.db.commit()

    def clearpoints(self):
        self.cursor.execute(f"""DELETE FROM roomLB WHERE roomNAME = '{self.room}'
        """)
        self.db.commit()
        respond(self.msgType, "Pontos da sala limpos!", self.senderID, self.room)
    
    def leaderboard(self, inQuestion=False):
        idRoom = self.sql_commands.select_idroom_by_nameid(self.room)[0][0]
        lb_fetch = self.sql_commands.select_all_leaderboard(idRoom)
        lb = {}
        htmlLB = """<div class="infobox"> <h3> Leaderboard </h3> <hr>
        """
        for data in lb_fetch:
            userID = data[1]
            user = self.sql_commands.select_usernameid_by_iduser(userID)[0][0]
            points = data[2]
            if int(points) == points:
                points = int(points)
            lb[user] = points

        lbSequenceSorted = dict(sorted(lb.items(), key=lambda item: item[1], reverse=True))

        for user in lbSequenceSorted:
            points = lbSequenceSorted[user]
            htmlLB += f"<b> {user}: </b> {points}"
            if not user == list(lbSequenceSorted)[-1]:
                htmlLB += ','

        htmlLB += "</hr></div>"

        if inQuestion:
            self.msgType = "room"

        respond(self.msgType, f"/addhtmlbox {htmlLB}", self.senderID, self.room)