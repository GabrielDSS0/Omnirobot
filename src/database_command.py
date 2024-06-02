from src.vars import Varlist

def execute_sql_command(command: str, params = ()):
    db = Varlist.db
    cursor = Varlist.cursor
    cursor.execute(command, params)
    db.commit()

def execute_sql_query(command: str, params = ()):
    cursor = Varlist.cursor
    cursor.execute(command, params)
    query_result = cursor.fetchall()
    return query_result