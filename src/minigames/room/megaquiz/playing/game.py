import threading
import random

from showdown.utils import name_to_id

from config import username, prefix
from src.vars import Varlist
from src.sending import *
from src.leaderboard.commands import *

class GameCommands():
    def __init__(self, host):
        self.host = host
        self.room = Varlist.room
        self.timer = 0
        self.alternatives = []
        self.fontColors = ["#008000", "#0000e6", "#cc0000", "#e0ae1b"]
        self.usersAnswered = []
        self.usersPointers = {}
        self.answer = ""
        self.html = ""
        self.question = ""

        self.currentQuestion = False

        self.sql_commands = Varlist.sql_commands
        self.questions = Varlist.questions

        self.leaderboardCommands = Leaderboard_Commands()
        self.leaderboardCommands.room = self.room

    def redirect_command(self, inst, name_func: str):
        self.sender = Varlist.sender
        self.senderID = Varlist.senderID
        self.commandParams = Varlist.commandParams
        func = getattr(inst, name_func)
        func()

    def makequestion(self):
        self.question = self.commandParams[-1]

        self.html += f'<div class="infobox"><center><font size="4">{self.question}</font><br><br><table width="100%" frame="box" rules="all" cellpadding="10"><tbody>'

        self.timer = self.sql_commands.select_timer_from_room(self.room)[0][0]

        respondPM(self.senderID, f"Questão feita! Agora, para adicionar alternativas, digite {prefix}add (alternativa).")

        self.timeToFinish = threading.Timer(10 * 60, self.finishQuestion)
        self.timeToFinish.start()

    def cancelquestion(self):
        if not self.question:
            return respondPM(self.senderID, "Não há uma questão ativa.")
        self.killQuestion()
        return respondPM(self.senderID, "Questão cancelada.")

    def addalternative(self):
        if not self.question:
            return respondPM(self.senderID, "Não há uma questão ativa.")
        alternative = self.commandParams[-1]
        color = random.choice(self.fontColors)
        if len(self.alternatives) % 2 == 0:
            self.html += f'<tr><td style="width: 50.00%"><center><button name="send" value="/w {username},{prefix}respond {self.room}, {self.host}, {alternative}" style=background-color:transparent;border:none;><font color="{color}" size="3"><b>{alternative}</b></font></button></center>'
        else:
            self.html += f'<td style="width: 50.00%"><center><button name="send" value="/w {username},{prefix}respond {self.room}, {self.host}, {alternative}" style=background-color:transparent;border:none;><font color="{color}" size="3"><b>{alternative}</b></font></button></center></tr>'
        self.fontColors.remove(color)
        self.alternatives.append(alternative)
        respondPM(self.senderID, f"Alternativa feita! Se quiser colocar alguma alternativa como a correta, digite {prefix}danswer (alternativa).")

    def defineanswer(self):
        if not self.question:
            return respondPM(self.senderID, "Não há uma questão ativa.")
        alternative = self.commandParams[-1]
        if alternative in self.alternatives:
            self.answer = alternative
            respondPM(self.senderID, f"A alternativa {alternative} foi configurada como a correta.")
        else:
            respondPM(self.senderID, f"A alternativa inserida não é uma das alternativas da questão.")

    def showquestion(self):
        if not self.question:
            return respondPM(self.senderID, "Não há uma questão ativa.")
        code = f"A questão está assim:\nQuestão: {self.question}\nAlternativas: {', '.join(self.alternatives)}\nAlternativa correta: {self.answer}"

        respondPM(self.senderID, f"!code {code}")

    def sendquestion(self):
        if not self.question:
            return respondPM(self.senderID, "Não há uma questão ativa.")
        self.html += "</tbody></table></center></div>"
        respondRoom(f"/addhtmlbox {self.html}", self.room)
        self.currentQuestion = True
        timer = threading.Timer(self.timer, self.timeLimit)
        timer.start()

    def respondquestion(self):
        points = 0

        if self.currentQuestion:
            if self.senderID in self.usersAnswered:
                return respondPM(self.senderID, "Você já enviou uma resposta nesta questão.")
            else:                
                self.usersAnswered.append(self.senderID)
                answer = name_to_id(self.commandParams[-1])
                if answer == name_to_id(self.answer):
                    points += 1
                    self.leaderboardCommands.sender = self.sender
                    self.leaderboardCommands.senderID = self.senderID
                    self.leaderboardCommands.command = ""
                    self.leaderboardCommands.msgType = ""
                    self.leaderboardCommands.addpoints(fromRespond=True)

                    self.usersPointers[self.sender] = points

    def timeLimit(self):
        self.currentQuestion = False
        self.timeToFinish.cancel()
        respondRoom(f"/wall ACABOU O TEMPO!", self.room)
        self.postQuestion()

    def postQuestion(self):
        self.killQuestion()

        self.msgType = 'room'
        threads = []

        pre_answer_revelation = 5
        answer_revelation = pre_answer_revelation + 5
        score = answer_revelation + 10
        lb_revelation = score + 10
        threads.append(threading.Timer(pre_answer_revelation, respondRoom, args=["E a resposta era...", self.room]))
        threads.append(threading.Timer(answer_revelation, respondRoom, args=[f"/wall {self.answer}!", self.room]))
        threads.append(threading.Timer(score, respondRoom, args=[f"Pontuadores: {', '.join(self.usersPointers)}", self.room]))
        threads.append(threading.Timer(lb_revelation, self.leaderboardCommands.leaderboard, args=[True]))
        for thread in threads:
            thread.start()

    def finishQuestion(self):
        self.killQuestion()
        respondPM(self.host, "Acabou o prazo para formalizar a questão.")
    
    def killQuestion(self):
        del self.questions[self.host][self.room]
        if not self.questions[self.host]:
            del self.questions[self.host]