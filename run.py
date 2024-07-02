import asyncio
import websockets
import psycopg2

from src.database_sql_commands import Commands_SQL
from src.vars import Varlist
from src.login import User
from config import uri
from config import database, host_db, user_db, password_db, port_db, schema

db = psycopg2.connect(database=database,
                      host=host_db,
                      user=user_db,
                      password=password_db,
                      port=port_db,
                      options=f"-c search_path=dbo,{schema}")

cursor = db.cursor()

commands_sql_var = Commands_SQL() 

Varlist.db = db
Varlist.cursor = cursor
Varlist.sql_commands = commands_sql_var

Varlist.sql_commands.create_all_tables()

async def run():
    async with websockets.connect(uri) as websocket:
        Varlist.websocket = websocket
        login: User = User()
        await login.login()

if __name__ == "__main__":
    asyncio.run(run())