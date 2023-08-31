import sys
from pyrogram import Client
from config import *
from ..logging import LOGGER
from pytgcalls import *



class Userbot(Client):
    assistants = []
    def __init__(self, **kwargs):
        name = self.__class__.__name__.lower()
        super().__init__(
            name="userbot",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION,
        )

    async def start(self):
        await super().start()
        LOGGER(__name__).info("Starting Assistant Clients")
        if self not in self.assistants:
            self.assistants.append(self)
