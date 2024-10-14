import json
import requests
import logging

import src.vars as vars
import src.commands_list as cmd_list
import src.control_pm_and_room as pm_room
import src.server_messages as server_msg
import src.sending as sending
import src.database_sql_commands as db_commands
import config

import src.admin_commands.redirecting as admin_redirect
import src.minigames.room.megaquiz.redirecting as mq_redirect
import src.minigames.subroom.redirecting as subroom_redirect
import src.minigames.subroom.dp.redirecting as dp_redirect
import src.misc_commands.redirecting as misc_redirect

logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.DEBUG,
)

class User():
    def __init__(self) -> None:
        self.websocket = vars.Varlist.websocket
        self.splitMsg = ""
        self.loginDone = False
        self.control_pm_room = None

    async def login(self):
        while True:
            msg = await self.websocket.recv()
            splitMsg = str(msg).split("|")
            self.splitMsg = splitMsg
            vars.Varlist.msgSplited = splitMsg
            if len(splitMsg) > 1:
                if splitMsg[1] == "challstr":
                    challstrStart = str(msg).find("4")
                    challstr = msg[challstrStart:]
                    postlogin = requests.post("https://play.pokemonshowdown.com/~~showdown/action.php", data={'act':'login','name':config.username,'pass':config.password,'challstr':challstr})
                    assertion = json.loads(postlogin.text[1:])["assertion"]
                    sending.call_command(self.websocket.send(f"|/trn {config.username},0,{assertion}"))
                    sending.call_command(self.websocket.send(f"|/avatar {config.avatar}"))

                    for room in config.rooms:
                        sending.call_command(self.websocket.send(f"|/join {room}"))
                        db_commands.Commands_SQL().insert_room(room)

                    self.loginDone = True

                    sending.call_command(self.websocket.send(f"|/status Para saber os comandos, digite @commands em minha PM."))

                    self.reconnecting()

            if self.loginDone:
                await self.afterLogin()

    async def afterLogin(self):
        self.control_pm_room = pm_room.Control()
        cmd_or_invite = self.control_pm_room.determinate_pm_or_room()

        if cmd_or_invite == "COMMAND":
            command = vars.Varlist.command
            if command in cmd_list.commands_misc:
                await misc_redirect.RedirectingFunction().redirect_to_function()
            elif command in cmd_list.commands_mq:
                await mq_redirect.RedirectingFunction().redirect_to_function()
            elif command in cmd_list.commands_dp:
                await dp_redirect.RedirectingFunction().redirect_to_function()
            elif command in cmd_list.commands_adm:
                await admin_redirect.RedirectingFunction().redirect_to_function()

        elif cmd_or_invite == "INVITE":
            subroom_redirect.joinRoom()
        
        else:
            server_msg.Server_Messages().check()
    
    def reconnecting(self):
        if vars.Varlist.dpGames:
            for player in vars.Varlist.dpGames:
                for room in vars.Varlist.dpGames[player]:
                    sending.call_command(self.websocket.send(f"|/j {room}"))