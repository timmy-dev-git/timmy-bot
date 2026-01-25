import os
import asyncio
import discord
from typing import Callable, Coroutine, Any

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        intents.presences = False
        super().__init__(intents=intents, application_id=int(os.environ["ID"]))
        self.tree = discord.app_commands.CommandTree(self)

    def Start(self, background_loop: Callable[[], Coroutine[Any, Any, None]]):
        async def main_loop():
            asyncio.create_task(background_loop())
            try:
                await self.start(os.environ["TOKEN"])
            except asyncio.CancelledError:
                pass
            finally:
                await self.close()

        try:
            asyncio.run(main_loop())
        except KeyboardInterrupt:
            pass