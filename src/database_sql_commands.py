from src.database_command import execute_sql_command, execute_sql_query

from showdown.utils import name_to_id

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
subroom_name varchar(60) NOT NULL,
host_name varchar(20) NOT NULL,
host_name_id varchar(20) NOT NULL
)
"""

CREATE_TABLE_DP_TEAM = """
CREATE TABLE IF NOT EXISTS tbl_dp_team (
idTeam serial PRIMARY KEY NOT NULL,
name VARCHAR(15) NOT NULL
)
"""

CREATE_TABLE_DP_PLAYER = """
CREATE TABLE IF NOT EXISTS tbl_dp_player (
idPlayer serial PRIMARY KEY NOT NULL,
idGame serial NOT NULL,
idTeam serial NOT NULL,
name varchar(20) NOT NULL,
name_id varchar(20) NOT NULL,
CONSTRAINT fk_ID_Game FOREIGN KEY (idGame)
REFERENCES tbl_dp_game(idGame),
CONSTRAINT fk_ID_Team FOREIGN KEY (idTeam)
REFERENCES tbl_dp_team(idTeam)
)
"""

CREATE_TABLE_DP_CLASS = """
CREATE TABLE IF NOT EXISTS tbl_dp_class (
idClass serial PRIMARY KEY NOT NULL,
idPlayer serial NOT NULL,
class_name varchar(20) NOT NULL,
class_name_id varchar(20) NOT NULL,
stat_hp real NOT NULL,
stat_shield real NOT NULL,
stat_atk real NOT NULL,
stat_tc real NOT NULL,
stat_td real NOT NULL,
levelup_atk real NOT NULL,
levelup_td real NOT NULL,
levelup_tc real NOT NULL,
keywords text,
effects text,
CONSTRAINT fk_ID_Player FOREIGN KEY (idPlayer)
REFERENCES tbl_dp_player (idPlayer)
)
"""

CREATE_TABLE_DP_MOVE = """
CREATE TABLE IF NOT EXISTS tbl_dp_move (
idMove serial PRIMARY KEY NOT NULL,
idClass serial NOT NULL,
name varchar(25) NOT NULL,
name_id varchar(25) NOT NULL,
target boolean NOT NULL,
priority real NOT NULL,
cooldown integer,
danos text,
efeitos text,
CONSTRAINT fk_ID_Class FOREIGN KEY (idClass)
REFERENCES tbl_dp_class (idClass)
)
"""

class Commands_SQL():
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
    
    def create_table_dp_team(self):
        self.params = ()
        self.command = CREATE_TABLE_DP_TEAM
        self.call_execute_sql_command()
    
    def create_table_dp_player(self):
        self.params = ()
        self.command = CREATE_TABLE_DP_PLAYER
        self.call_execute_sql_command()
    
    def create_table_dp_class(self):
        self.params = ()
        self.command = CREATE_TABLE_DP_CLASS
        self.call_execute_sql_command()
    
    def create_table_dp_move(self):
        self.params = ()
        self.command = CREATE_TABLE_DP_MOVE
        self.call_execute_sql_command()
    
    def create_all_tables(self):
        self.params = ()
        commands = [CREATE_TABLE_ROOM,
                         CREATE_TABLE_USER,
                         CREATE_TABLE_LEADERBOARD,
                         CREATE_TABLE_DP_GAME,
                         CREATE_TABLE_DP_TEAM,
                         CREATE_TABLE_DP_PLAYER,
                         CREATE_TABLE_DP_CLASS,
                         CREATE_TABLE_DP_MOVE]
    
        for command in commands:
            self.command = command
            self.call_execute_sql_command()

    def insert_room(self, roomname_id: str):
        if (self.verify_room_exists(roomname_id)):
            return
        timer_mq_default = 12
        self.params = (roomname_id, timer_mq_default)
        self.command = """
        INSERT INTO tbl_room (name_id, timer_mq) 
        VALUES (%s,%s,%s);
        """
        self.call_execute_sql_command()
    
    def verify_room_exists(self, roomname_id: str):
        self.params = ()
        self.command = f"""
        SELECT idRoom FROM tbl_room WHERE name_id = '{roomname_id}'
        """
        return self.call_execute_sql_query()

    def delete_room(self, roomname_id: str):
        self.params = ()
        self.command = f"""
        DELETE FROM tbl_room WHERE name_id = {roomname_id}
        """
        self.call_execute_sql_command()
    
    def select_timer_from_room(self, roomname_id):
        self.params = ()
        self.command = f"""SELECT timer_mq FROM tbl_room WHERE name_id = '{roomname_id}'
        """
        return self.call_execute_sql_query()

    def update_timer(self, timer: float, room_id: str):
        self.params = ()
        self.command = f"""UPDATE tbl_room SET timer_mq = '{timer}' WHERE name_id = '{room_id}'
        """
        self.call_execute_sql_command()

    def insert_user(self, username: str):
        username_id = name_to_id(username)
        self.params = (username, username_id)
        self.command = """
        INSERT INTO tbl_user (name, name_id) 
        VALUES (%s,%s);
        """
        self.call_execute_sql_command()
    
    def select_user_by_nameid(self, username_id: str):
        self.params = ()
        self.command = f"""
        SELECT idUser FROM tbl_user WHERE name_id = '{username_id}'
        """
        return self.call_execute_sql_query()
    
    def delete_user(self, username_id: str):
        self.params = ()
        self.command = f"""
        DELETE FROM tbl_user WHERE name_id = {username_id}
        """
        self.call_execute_sql_command()
    
    def insert_leaderboard(self, idUser: int, idRoom: int, points: float):
        params = (idUser, idRoom, points)
        self.command = """INSERT INTO tbl_leaderboard (idUser, idRoom, points) VALUES (%s,%s,%s)
        """
    
    def select_userpoints_leaderboard(self, idUser: int, idRoom: int):
        self.params = ()
        self.command = f"""SELECT points FROM tbl_leaderboard WHERE idUser = {idUser} AND WHERE idRoom = {idRoom}
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

    def update_userpoints_leaderboard(self, points: float, idUser: int, idRoom: int):
        self.cursor.execute(f"""UPDATE tbl_leaderboard SET points = {points} WHERE idUser = {idUser} and idRoom = {idRoom}
        """)

    def call_execute_sql_command(self):
        execute_sql_command(self.command, self.params)
    
    def call_execute_sql_query(self):
        return execute_sql_query(self.command, self.params)