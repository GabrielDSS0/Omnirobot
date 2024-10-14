from psycopg2.extensions import connection, cursor as cs
from websockets import WebSocketClientProtocol

class Varlist:
   websocket: WebSocketClientProtocol = None
   db: connection = None
   cursor: cs = None
   sql_commands = None
   
   msgSplited: list =  []
   commandParams: list = []
   command: str = ""
   sender: str = ""
   senderID: str = ""
   content: str = ""
   msgType: str = ""
   
   room: str = ""
   groupchat_name_complete: str = ""

   questions: dict = {}
   hosts_groupchats: dict = {}
   dpGames: dict = {}

   modules_to_reload = []