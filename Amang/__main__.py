"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
import asyncio
import importlib
import re
from contextlib import closing, suppress

from pyrogram import idle

from uvloop import install

from Amang import *
from config import *
from Amang.core.copas import bajingan
from Amang.utils.dbfunctions import clean_restart_stage
from .logging import LOGGER


loop = asyncio.get_event_loop()


async def start_bot():
    with suppress(KeyboardInterrupt):
        await app.start()
        x = await app.get_me()
        BOT_ID = x.id
        BOT_NAME = x.first_name + (x.last_name or "")
        BOT_USERNAME = x.username
        BOT_MENTION = x.mention
        BOT_DC_ID = x.dc_id
        LOGGER("Info").info(f"BOT STARTED AS {BOT_NAME}!")
        await app2.start()
        y = await app2.get_me()
        USERBOT_ID = y.id
        USERBOT_NAME = y.first_name + (y.last_name or "")
        USERBOT_USERNAME = y.username
        USERBOT_MENTION = y.mention
        USERBOT_DC_ID = y.dc_id
        LOGGER("Info").info(f"USERBOT STARTED AS {USERBOT_NAME}!")
        telegraph.create_account(short_name=BOT_USERNAME)
        LOGGER("Info").info("Startup Telegraph...")
        restart_data = await clean_restart_stage()
        if USERBOT_ID not in SUDOERS:
            SUDOERS.add(USERBOT_ID)
        if OWNER_ID not in SUDOERS:
            SUDOERS.add(OWNER_ID)
        await load_sudoers()

        with suppress(Exception):
            LOGGER("Info").info("Sending online status")
            if restart_data:
                await app.edit_message_text(
                    restart_data["chat_id"],
                    restart_data["message_id"],
                    "**Restarted Successfully**",
                )

            else:
                await app.send_message(LOG_GROUP_ID, "Bot started!")
        await bajingan()
        await idle()
#        await aiohttpsession.close()
        LOGGER("Info").info("Stopping clients")
        await app.stop()
        LOGGER("Info").info("Cancelling asyncio tasks")


if __name__ == "__main__":
    try:
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        pass
    except Exception:
        err = traceback.format_exc()
        LOGGER.info(err)
    finally:
        loop.stop()
        LOGGER.info("------------------------ Stopped Services ------------------------")
