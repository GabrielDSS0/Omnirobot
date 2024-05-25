from config import prefix

from src.sending import *
from src.vars import Varlist

class OtherCommands():
    def __init__(self):
        self.msgSplited = Varlist.msgSplited
        self.websocket = Varlist.websocket
        self.db = Varlist.db
        self.cursor = Varlist.cursor
        self.command = Varlist.command
        self.commandParams = Varlist.commandParams
        self.msgType = Varlist.msgType
        self.room = Varlist.room
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID

    def redirect_command(self, inst, name_func: str):
        func = getattr(inst, name_func)
        func()

    def defTimer(self):
        time = self.commandParams[0]
        self.cursor.execute(f"""UPDATE tbl_room SET timer = "{self.timer}" WHERE name_id = '{self.room}'
        """)
        self.db.commit()
        respond(self.msgType, f"O tempo foi alterado para {time} segundos!", self.websocket, self.senderID, self.room)
    
    def addpoints(self, newPoints=1):
        username_id = self.senderID

        self.cursor.execute(f"""SELECT idUser FROM tbl_leaderboard WHERE idUser IN (SELECT idUser FROM tbl_user WHERE name_id = '{username_id}')
        """)

        userID = self.cursor.fetchall()
        user = userID[0][0]
        self.cursor.execute(f"""SELECT points FROM tbl_leaderboard WHERE idUser = '{user}'
        """)

        points = self.cursor.fetchall()[0][0] + newPoints

        if userID:
            self.cursor.execute(f"""UPDATE tbl_leaderboard SET points = {points} WHERE idUser = '{user}' and roomNAME = '{self.room}'
            """)
        else:
            self.cursor.execute(f"""SELECT idRoom FROM tbl_leaderboard WHERE idRoom IN (SELECT idRoom FROM tbl_room WHERE name_id = '{self.room}'
            """)
            
            self.cursor.execute(f"""INSERT INTO tbl_leaderboard (idUser, idRoom, points) VALUES (?,?,?)
            """, (self.room, user, points))

        if self.command == "addpoints":
            respond(self.msgType, "Pontos adicionados!", self.websocket, self.senderID, self.room)

        self.db.commit()

    def rempoints(self, remPoints=1):
        username_id = self.senderID
        remPoints = self.commandParams[1]
        try:
            remPoints = float(remPoints)
        except:
            return respond(self.msgType, f"Uso do comando: {prefix}rpoints [usuario], [pontos], [sala]", self.websocket, self.senderID, self.room)

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
            respond(self.msgType, "Pontos removidos!", self.websocket, self.senderID, self.room)

        self.db.commit()

    def clearpoints(self):
        self.cursor.execute(f"""DELETE FROM roomLB WHERE roomNAME = '{self.room}'
        """)
        self.db.commit()
        respond(self.msgType, "Pontos da sala limpos!", self.websocket, self.senderID, self.room)
    
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

        respond(self.msgType, f"/addhtmlbox {htmlLB}", self.websocket, self.senderID, self.room)