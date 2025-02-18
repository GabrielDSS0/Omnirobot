from psclient import toID

import src.database_command as db_command

CREATE_TABLE_ROOM = """
CREATE TABLE IF NOT EXISTS tbl_room (
idRoom serial PRIMARY KEY NOT NULL,
name_id varchar(40) NOT NULL,
timer_mq real
)
"""

CREATE_TABLE_USER = """
CREATE TABLE IF NOT EXISTS tbl_user (
idUser serial PRIMARY KEY NOT NULL,
name varchar(20) NOT NULL,
name_id varchar(20) NOT NULL
)
"""

CREATE_TABLE_LEADERBOARD = """
CREATE TABLE IF NOT EXISTS tbl_leaderboard (
idRoom serial NOT NULL,
idUser serial NOT NULL,
points real,
CONSTRAINT fk_ID_Room FOREIGN KEY (idRoom)
REFERENCES tbl_room(idRoom),
CONSTRAINT fk_ID_User FOREIGN KEY (idUser)
REFERENCES tbl_user(idUser)
)
"""

CREATE_TABLE_DP_GAME = """
CREATE TABLE IF NOT EXISTS tbl_dp_game (
idGame serial PRIMARY KEY NOT NULL,
subroom_name varchar(60) NOT NULL
)
"""

CREATE_TABLE_DP_ACTION = """
CREATE TABLE IF NOT EXISTS tbl_dp_action (
idAction serial PRIMARY KEY NOT NULL,
idGame serial NOT NULL,
action text,
CONSTRAINT fk_ID_Game FOREIGN KEY (idGame)
REFERENCES tbl_dp_game(idGame)
)
"""

CREATE_TABLE_EXCEPTION = """
CREATE TABLE IF NOT EXISTS tbl_exception (
idException serial PRIMARY KEY NOT NULL,
exception text,
date text,
lastmsg text
)
"""


class Commands_SQL:
	def __init__(self) -> None:
		self.command: str = ""
		self.params: tuple = ()

	def create_table_room(self):
		self.params = ()
		self.command = CREATE_TABLE_ROOM
		self.call_execute_sql_command()

	def create_table_user(self):
		self.params = ()
		self.command = CREATE_TABLE_USER
		self.call_execute_sql_command()

	def create_table_lb(self):
		self.params = ()
		self.command = CREATE_TABLE_LEADERBOARD
		self.call_execute_sql_command()

	def create_table_dp_game(self):
		self.params = ()
		self.command = CREATE_TABLE_DP_GAME
		self.call_execute_sql_command()

	def create_table_dp_action(self):
		self.params = ()
		self.command = CREATE_TABLE_DP_ACTION
		self.call_execute_sql_command()

	def create_table_exception(self):
		self.params = ()
		self.command = CREATE_TABLE_EXCEPTION
		self.call_execute_sql_command()

	def create_all_tables(self):
		self.params = ()
		functions = [
			self.create_table_room,
			self.create_table_user,
			self.create_table_lb,
			self.create_table_dp_game,
			self.create_table_dp_action,
			self.create_table_exception,
		]

		for func in functions:
			func()

	def insert_room(self, roomname_id: str):
		if self.select_idroom_by_nameid(roomname_id):
			return
		timer_mq_default = 12
		self.params = (roomname_id, timer_mq_default)
		self.command = """
        INSERT INTO tbl_room (name_id, timer_mq) 
        VALUES (%s,%s);
        """
		self.call_execute_sql_command()

	def select_idroom_by_nameid(self, roomname_id: str):
		self.params = ()
		self.command = f"""
        SELECT idRoom FROM tbl_room WHERE name_id = '{roomname_id}'
        """
		return self.call_execute_sql_query()

	def select_timer_from_room(self, roomname_id: str):
		self.params = ()
		self.command = f"""SELECT timer_mq FROM tbl_room WHERE name_id = '{roomname_id}'
        """
		return self.call_execute_sql_query()

	def update_timer(self, timer: float, room_id: str):
		self.params = ()
		self.command = f"""UPDATE tbl_room SET timer_mq = '{timer}' WHERE name_id = '{room_id}'
        """
		self.call_execute_sql_command()

	def delete_room(self, roomname_id: str):
		self.params = ()
		self.command = f"""
        DELETE FROM tbl_room WHERE name_id = {roomname_id}
        """
		self.call_execute_sql_command()

	def insert_user(self, username: str):
		username_id = toID(username)
		self.params = (username, username_id)
		self.command = """
        INSERT INTO tbl_user (name, name_id) 
        VALUES (%s,%s);
        """
		self.call_execute_sql_command()

	def select_iduser_by_nameid(self, username_id: str):
		self.params = ()
		self.command = f"""
        SELECT idUser FROM tbl_user WHERE name_id = '{username_id}'
        """
		return self.call_execute_sql_query()

	def select_username_by_iduser(self, idUser: int):
		self.params = ()
		self.command = f"""SELECT name FROM tbl_user WHERE idUser = {idUser}
        """
		return self.call_execute_sql_query()

	def select_usernameid_by_iduser(self, idUser: int):
		self.params = ()
		self.command = f"""SELECT name_id FROM tbl_user WHERE idUser = {idUser}
        """
		return self.call_execute_sql_query()

	def delete_user(self, username_id: str):
		self.params = ()
		self.command = f"""
        DELETE FROM tbl_user WHERE name_id = {username_id}
        """
		self.call_execute_sql_command()

	def insert_leaderboard(self, idUser: int, idRoom: int, points: float):
		self.params = (idUser, idRoom, points)
		self.command = """INSERT INTO tbl_leaderboard (idUser, idRoom, points) VALUES (%s,%s,%s)
        """
		self.call_execute_sql_command()

	def select_all_leaderboard(self, idRoom: int):
		self.params = ()
		self.command = f"""SELECT * FROM tbl_leaderboard WHERE idRoom = {idRoom}
        """
		return self.call_execute_sql_query()

	def select_userpoints_leaderboard(self, idUser: int, idRoom: int):
		self.params = ()
		self.command = f"""SELECT points FROM tbl_leaderboard WHERE idUser = {idUser} AND idRoom = {idRoom}
        """
		return self.call_execute_sql_query()

	def select_iduser_from_leaderboard(self, username_id: str):
		self.params = ()
		self.command = f"""SELECT idUser FROM tbl_leaderboard WHERE idUser IN (SELECT idUser FROM tbl_user WHERE name_id = '{username_id}')
        """
		return self.call_execute_sql_query()

	def select_idroom_from_leaderboard(self, roomname_id: str):
		self.params = ()
		self.command = f"""SELECT idRoom FROM tbl_leaderboard WHERE idRoom IN (SELECT idRoom FROM tbl_room WHERE name_id = '{roomname_id}')
        """
		return self.call_execute_sql_query()

	def update_userpoints_leaderboard(
		self, points: float, idUser: int, idRoom: int
	):
		self.params = ()
		self.command = f"""UPDATE tbl_leaderboard SET points = {points} WHERE idUser = {idUser} and idRoom = {idRoom}
        """
		self.call_execute_sql_command()

	def clear_leaderboard(self, idRoom: int):
		self.params = ()
		self.command = f"""DELETE FROM tbl_leaderboard WHERE idRoom = {idRoom}
        """
		self.call_execute_sql_command()

	def delete_user_from_leaderboard(self, idUser: int, idRoom: int):
		self.params = ()
		self.command = f"""DELETE FROM tbl_leaderboard WHERE idUser = {idUser} and idRoom = {idRoom}
        """
		self.call_execute_sql_command()

	def insert_dp_game(self, subroom_name: str):
		self.params = (subroom_name,)
		self.command = """INSERT INTO tbl_dp_game (subroom_name) VALUES (%s)
        """
		self.call_execute_sql_command()

	def select_dp_games(self):
		self.params = ()
		self.command = """SELECT * FROM tbl_dp_game
        """
		return self.call_execute_sql_query()

	def delete_dp_game(self, idGame):
		self.params = ()
		self.command = f"""DELETE FROM tbl_dp_game where idGame = {idGame}
        """
		self.call_execute_sql_command()

	def insert_dp_action(self, idGame: int, action: str):
		self.params = (idGame, action)
		self.command = """INSERT INTO tbl_dp_action (idGame, action) VALUES (%s,%s)
        """
		self.call_execute_sql_command()

	def select_dp_action(self, idGame: int):
		self.params = ()
		self.command = f"""SELECT action FROM tbl_dp_action WHERE idGame = {idGame}
        """
		return self.call_execute_sql_query()

	def delete_dp_action(self, idGame: int):
		self.params = ()
		self.command = f"""DELETE FROM tbl_dp_action WHERE idGame = {idGame}
        """
		self.call_execute_sql_command()

	def insert_exception(self, exception, date, lastmsg):
		self.params = (exception, date, lastmsg)
		self.command = """INSERT INTO tbl_exception (exception, date, lastmsg) VALUES (%s,%s,%s)
        """
		self.call_execute_sql_command()

	def call_execute_sql_command(self):
		db_command.execute_sql_command(self.command, self.params)

	def call_execute_sql_query(self):
		return db_command.execute_sql_query(self.command, self.params)
