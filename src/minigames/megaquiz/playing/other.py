from config import prefix

from src.sending import *
from src.vars import Varlist as vl

class OtherCommands():
    def __init__(self):
        self.msgSplited = Varlist.msgSplited
        self.websocket = Varlist.websocket
        self.db = Varlist.db
        self.cursor = Varlist.cursor
        self.msgType = Varlist.msgType
        self.room = Varlist.room

    def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.command = Varlist.command
        self.commandParams = Varlist.commandParams
        func = getattr(inst, name_func)
        func()

    def definetimer(self):
        timer = self.commandParams[-1]
        vl.sql_commands.update_timer(timer, self.room)
        respond(self.msgType, f"O tempo foi alterado para {timer} segundos!", self.senderID, self.room)
    
    def addpoints(self, newPoints=1):
        points_receiver = self.sender
        username_id = self.senderID

        idRoom = vl.sql_commands.select_idroom_from_leaderboard(self.room)[0][0]
        idUser = vl.sql_commands.select_iduser_from_leaderboard(username_id)[0][0]

        userID = self.cursor.fetchall()

        if userID:
            user = userID[0][0]
            vl.sql_commands.select_userpoints_leaderboard(idUser, idRoom)

            points = self.cursor.fetchall()[0][0] + newPoints

            vl.sql_commands.update_userpoints_leaderboard(points, idUser, idRoom)
        else:
            vl.sql_commands.insert_user(points_receiver)
            idUser = vl.sql_commands.select_user_by_nameid(username_id)[0][0]

            vl.insert_leaderboard(idUser, idRoom, newPoints)

        if self.command == "addpoints":
            respond(self.msgType, "Pontos adicionados!", self.senderID, self.room)

        self.db.commit()

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
    
    def leaderboard(self):
        self.cursor.execute(f"""SELECT * FROM roomLB WHERE roomNAME = '{self.room}'
        """)
        lb = {}
        htmlLB = """<div class="infobox"> <h3> Leaderboard </h3> <hr>
        """
        for data in self.cursor.fetchall():
            user = data[1]
            points = data[3]
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

        respond(self.msgType, f"/addhtmlbox {htmlLB}", self.senderID, self.room)