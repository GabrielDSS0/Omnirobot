import asyncio
import traceback
from datetime import datetime

import psycopg2
import websockets

import config
import objectsdill
import src.database_sql_commands as db_commands
import src.login as login
import src.vars as vars


def init_db():
	db = psycopg2.connect(
		database=config.database,
		host=config.host_db,
		user=config.user_db,
		password=config.password_db,
		port=config.port_db,
		options=f"-c search_path=dbo,{config.schema}",
	)

	cursor = db.cursor()

	commands_sql_var = db_commands.Commands_SQL()

	vars.Varlist.db = db
	vars.Varlist.cursor = cursor
	vars.Varlist.sql_commands = commands_sql_var

	vars.Varlist.sql_commands.create_all_tables()


async def run():
	init_db()

	async for websocket in websockets.connect(config.uri):
		try:
			objectsdill.load()
			vars.Varlist.websocket = websocket
			login_client: login.User = login.User()
			await login_client.login()

		except websockets.exceptions.ConnectionClosed:
			continue
		except Exception:
			e = traceback.format_exc()
			now = datetime.now()
			now_format = now.strftime("%d/%m/%Y %H:%M:%S")
			msg = "|".join(vars.Varlist.msgSplited)
			vars.Varlist.sql_commands.insert_exception(e, now_format, msg)
		finally:
			objectsdill.save()


if __name__ == "__main__":
	asyncio.run(run())
