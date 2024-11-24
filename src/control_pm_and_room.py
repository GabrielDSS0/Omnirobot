import re

import src.vars as vars
import src.commands_list as cmd_list
import config

from psclient import toID

class Control():
    def __init__(self) -> None:
        self.msgSplited = vars.Varlist.msgSplited
        self.content = ""
        self.msgType = ""
        self.commandParams = []
        self.room = ""

    def determinate_pm_or_room(self):
        if len(self.msgSplited) == 2:
            if self.msgSplited[1] == "deinit":
                room = self.msgSplited[0][1:].strip()
                hosts_groupchats = vars.Varlist.hosts_groupchats.copy()
                for user in hosts_groupchats:
                    rooms = vars.Varlist.hosts_groupchats[user]
                    if room in rooms:
                        vars.Varlist.hosts_groupchats[user].remove(room)
                        if not (vars.Varlist.hosts_groupchats[user]):
                            del vars.Varlist.hosts_groupchats[user]

                        if user in vars.Varlist.dpGames:
                            if room in vars.Varlist.dpGames[user]:
                                vars.Varlist.dpGames[user].pop(room)
                            if not (vars.Varlist.dpGames[user]):
                                del vars.Varlist.dpGames[user]
            return
                        
        elif len(self.msgSplited) > 4:
            if self.msgSplited[1] == "pm":
                sender = self.msgSplited[2][1:]
                senderID = toID(sender)
                self.content = self.msgSplited[4]
                self.msgType = "pm"
            elif self.msgSplited[1] == "c:":
                sender = self.msgSplited[3][1:]
                senderID = toID(sender)
                self.content = self.msgSplited[4]
                self.msgType = "room"
            else:
                return
        else:
            return
        
        if not self.content:
            return

        vars.Varlist.sender = sender
        vars.Varlist.senderID = senderID
        vars.Varlist.content = self.content
        vars.Varlist.msgType = self.msgType

        is_command = self.determinate_is_a_command()
        if not is_command:
            is_invite = self.determinate_is_a_invite()
            if not is_invite:
                return
            else:
                return is_invite
        else:
            return is_command

    def determinate_is_a_command(self):
        if self.content[0] == config.prefix:
            command = toID(self.content.split(" ")[0].strip()[1:])
            self.commandParams = self.content.replace(f"{config.prefix}{command}", "").strip().split(",")
            self.commandParams = [param.strip() for param in self.commandParams]
        else:
            return

        if command in cmd_list.aliases:
            command = cmd_list.aliases[command]

        if command in cmd_list.allCommands_keys:
            vars.Varlist.command = command
            vars.Varlist.commandParams = self.commandParams
        else:
            return

        self.identify_room()

        return "COMMAND"
    
    def identify_room(self):
        if self.msgType == "room":
            self.room = self.msgSplited[0].strip()
            if not self.room:
                self.room = "lobby"
            else:
                self.room = self.room[1:]
                if self.room[:9] == "groupchat":
                    vars.Varlist.groupchat_name_complete = self.room


        elif self.msgType == "pm":
            self.room = self.commandParams[0].strip()
            vars.Varlist.groupchat_name_complete = f"groupchat-{self.room}"
            if self.room[:9] == "groupchat":
                self.room = re.sub('[^0-9a-zA-Z-]+', '', self.room).lower()
            else:
                self.room = toID(self.room)

        vars.Varlist.room = self.room
    
    def determinate_is_a_invite(self):
        invite = self.content.split(" ")

        if invite[0] == "/invite":
            return "INVITE"
        else:
            return