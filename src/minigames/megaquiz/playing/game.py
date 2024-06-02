import asyncio
import threading
import random

from showdown.utils import name_to_id

from config import username, prefix
from src.vars import Varlist as vl
from src.sending import *
from src.minigames.megaquiz.playing.other import *

class GameCommands():
    def __init__(self, host):
        self.msgSplited = Varlist.msgSplited
        self.websocket = Varlist.websocket
        self.db = Varlist.db
        self.cursor = Varlist.cursor
        self.host = host
        self.currentQuestion = False
        self.questionFinished = False
        self.alternativesNumber = 0
        self.timer = 15
        self.alternatives = []
        self.fontColors = ["#008000", "#0000e6", "#cc0000", "#e0ae1b"]
        self.rooms = []
        self.usersAnswered = []
        self.usersPointers = {}
        self.room = Varlist.room
        self.answer = ""
        self.html = ""
        self.question = ""

        self.otherCommands = OtherCommands()
        self.otherCommands.room = self.room

    async def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.commandParams = Varlist.commandParams
        func = getattr(inst, name_func)
        await func()

    async def makequestion(self):
        self.question = self.commandParams[-1]

        self.html += f'<div class="infobox"><center><font size="4">{self.question}</font><br><br><table width="100%" frame="box" rules="all" cellpadding="10"><tbody>'

        vl.sql_commands.select_timer_from_room

        timer = self.cursor.fetchall()

        if timer:
            self.timer = timer[0][0]

        respondPM(self.senderID, f"Questão feita! Agora, para adicionar alternativas, digite {prefix}add (alternativa).")

        self.timeToFinish = threading.Timer(10 * 60, self.finishQuestion)
        self.timeToFinish.start()

    async def cancelquestion(self):
        self.questionFinished = True
        return respondPM(self.senderID, "Questão cancelada.")

    async def addalternative(self):
        alternative = self.commandParams[-1]
        color = random.choice(self.fontColors)
        if self.alternativesNumber % 2 == 0:
            self.html += f'<tr><td style="width: 50.00%"><center><button name="send" value="/w {username},{prefix}respond {self.room}, {self.host}, {alternative}" style=background-color:transparent;border:none;><font color="{color}" size="3"><b>{alternative}</b></font></button></center>'
        else:
            self.html += f'<td style="width: 50.00%"><center><button name="send" value="/w {username},{prefix}respond {self.room}, {self.host}, {alternative}" style=background-color:transparent;border:none;><font color="{color}" size="3"><b>{alternative}</b></font></button></center></tr>'
        self.fontColors.remove(color)
        self.alternativesNumber += 1
        self.alternatives.append(alternative)

        respondPM(self.senderID, f"Alternativa feita! Se quiser colocar alguma alternativa como a correta, digite {prefix}danswer (alternativa).")

    async def defineanswer(self):
        alternative = self.commandParams[-1]
        if alternative in self.alternatives:
            self.answer = alternative
            respondPM(self.senderID, f"A alternativa {alternative} foi configurada como a correta.")

    async def showquestion(self):
        code = f"A questão está assim:\nQuestão: {self.question}\nAlternativas: {', '.join(self.alternatives)}\nAlternativa correta: {self.answer}"

        respondPM(self.senderID, f"!code {code}")

    async def sendquestion(self):
        self.html += "</tbody></table></center></div>"
        respondRoom(f"/addhtmlbox {self.html}", self.room)
        self.currentQuestion = True
        timer = threading.Timer(self.timer, lambda: asyncio.run(self.timeLimit()))
        timer.start()

    async def respondquestion(self):
        points = 0

        if self.currentQuestion:
                self.usersAnswered.append(self.senderID)
                answer = name_to_id(self.commandParams[-1])
                print(answer)
                print(self.answer)
                if answer == name_to_id(self.answer):
                    points += 1
                    self.otherCommands.sender = self.sender
                    self.otherCommands.senderID = self.senderID
                    self.otherCommands.command = ""
                    self.otherCommands.commandParams = [self.sender, points, self.room]
                    await self.otherCommands.addpoints()
                    if self.sender not in self.usersPointers:
                        self.usersPointers[self.sender] = points
                    else:
                        self.usersPointers[self.sender] += points

    async def timeLimit(self):
        self.currentQuestion = False
        self.questionFinished = True
        self.timeToFinish.cancel()
        respondRoom(f"/wall ACABOU O TEMPO!", self.room)
        await self.postQuestion()

    async def postQuestion(self):
        self.msgType = 'room'
        threads = []
        threads.append(threading.Timer(5, respondRoom, args=["E a resposta era...", self.room]))
        threads.append(threading.Timer(10, respondRoom, args=[f"/wall {self.answer}!", self.room]))
        threads.append(threading.Timer(20, respondRoom, args=[f"Pontuadores: {', '.join(self.usersPointers)}", self.room]))

        #threads.append(threading.Timer(30, self.otherCommands.redirect_command, args=[self.otherCommands, "leaderboard"]))
        for thread in threads:
            thread.start()

    def finishQuestion(self):
        self.questionFinished = True
        respondPM(self.host, "Acabou o prazo para formalizar a questão.")