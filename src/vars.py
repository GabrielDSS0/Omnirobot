from psycopg2.extensions import connection, cursor as cs
from websockets import WebSocketClientProtocol

class Varlist:
   websocket: WebSocketClientProtocol = None
   db: connection = None
   cursor: cs = None
   sql_commands = None
   msgSplited: list =  []
   commandParams: list = []
   questions: dict = {}
   dpGames: dict = {}
   writing: dict = {}
   command: str = ""
   sender: str = ""
   senderID: str = ""
   content: str = ""
   msgType: str = ""
   room: str = ""
