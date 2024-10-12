import json
import requests
import logging

from src.commands_list import commands_dp, commands_mq, commands_leaderboard
from src.vars import Varlist
from src.control_pm_and_room import Control
from src.sending import call_command
from src.database_sql_commands import Commands_SQL
from config import username, password, rooms, avatar

from src.minigames.room.megaquiz.redirecting import RedirectingFunction as mq_redirect
from src.minigames.subroom.dp.redirecting import RedirectingFunction as dp_redirect
from src.minigames.subroom.redirecting import joinRoom
from src.leaderboard.redirecting import RedirectingFunction as lb_redirect

logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.DEBUG,
)

class User():
    def __init__(self) -> None:
        self.websocket = Varlist.websocket
        self.splitMsg = ""
        self.loginDone = False
        self.control_pm_room = None

    async def login(self):
        while True:
            msg = await self.websocket.recv()
            splitMsg = str(msg).split("|")
            self.splitMsg = splitMsg
            Varlist.msgSplited = splitMsg
            if len(splitMsg) > 1:
                if splitMsg[1] == "challstr":
                    challstrStart = str(msg).find("4")
                    challstr = msg[challstrStart:]
                    postlogin = requests.post("https://play.pokemonshowdown.com/~~showdown/action.php", data={'act':'login','name':username,'pass':password,'challstr':challstr})
                    assertion = json.loads(postlogin.text[1:])["assertion"]
                    call_command(self.websocket.send(f"|/trn {username},0,{assertion}"))
                    call_command(self.websocket.send(f"|/avatar {avatar}"))

                    for room in rooms:
                        call_command(self.websocket.send(f"|/join {room}"))
                        Commands_SQL().insert_room(room)

                    self.loginDone = True

            if self.loginDone:
                await self.afterLogin()


    async def afterLogin(self):
        self.control_pm_room = Control()
        cmd_or_invite = self.control_pm_room.determinate_pm_or_room()
        
        if cmd_or_invite == "COMMAND":
            command = Varlist.command
            if command in commands_leaderboard:
                await lb_redirect().redirect_to_function()
            elif command in commands_mq:
                await mq_redirect().redirect_to_function()
            elif command in commands_dp:
                await dp_redirect().redirect_to_function()

        elif cmd_or_invite == "INVITE":
            joinRoom()