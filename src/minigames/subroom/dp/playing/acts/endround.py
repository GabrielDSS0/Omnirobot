from src.vars import Varlist

class PostRound():
    def __init__(self) -> None:
        self.room = Varlist.room
        self.writing = Varlist.writing
    def writingActions(self):
        self.writing.pop(self.room)