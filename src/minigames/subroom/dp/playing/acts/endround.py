import asyncio

from src.vars import Varlist
from src.sending import respondRoom

class PostRound():
    def __init__(self, idGame, room) -> None:
        self.idGame = idGame
        self.room = room
        self.sql_commands = Varlist.sql_commands
        self.dpGames = Varlist.dpGames

    async def writingActions(self):
        actions = self.sql_commands.select_dp_actions(self.idGame)
        for act in actions:
            await asyncio.sleep(5)
            act = act[0]
            respondRoom(f"**{act}**", self.room)

        self.sql_commands.delete_dp_actions(self.idGame)