from src.vars import Varlist

def execute_sql_command(command: str, params = ()):
    db = Varlist.db
    cursor = Varlist.cursor
    cursor.execute(command, params)
    db.commit()