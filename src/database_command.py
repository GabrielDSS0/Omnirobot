import src.vars as vars

def execute_sql_command(command: str, params = ()):
    db = vars.Varlist.db
    cursor = vars.Varlist.cursor
    cursor.execute(command, params)
    db.commit()

def execute_sql_query(command: str, params = ()):
    cursor = vars.Varlist.cursor
    cursor.execute(command, params)
    query_result = cursor.fetchall()
    return query_result