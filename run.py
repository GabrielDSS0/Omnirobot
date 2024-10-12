import asyncio
import websockets
import psycopg2
import traceback
import os
import dill

from datetime import datetime

from src.database_sql_commands import Commands_SQL
import src.vars
from src.vars import Varlist
from src.login import User
from config import uri
from config import database, host_db, user_db, password_db, port_db, schema

def init_db():
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
    init_db()
    async for websocket in websockets.connect(uri):
        try:
            if os.path.isfile("saveobjects.pkl"):
                with open('saveobjects.pkl', 'rb') as f:
                    if f.readlines():
                        src.vars.Varlist = dill.load(f)
                open("saveobjects.pkl", "w")

            Varlist.websocket = websocket
            login: User = User()
            await login.login()

        except websockets.exceptions.ConnectionClosed:
            continue
        except Exception:
            e = traceback.format_exc()
            now = datetime.now()
            now_format = now.strftime("%d/%m/%Y %H:%M:%S")
            Varlist.sql_commands.insert_exception(e, now_format)

        finally:
            with open('saveobjects.pkl', 'wb') as f:
                dill.dump(Varlist, f)

if __name__ == "__main__":
    asyncio.run(run())