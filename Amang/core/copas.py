

import importlib
from Amang.modules import ALL_MODULES
from ..logging import LOGGER
from config import LOG_GROUP_ID
from platform import python_version
from pyrogram import __version__
from Amang import app, app2
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


HELPABLE = {}

async def bajingan():
    global HELPABLE
    for module in ALL_MODULES:
        imported_module = importlib.import_module(f"Amang.modules.{module}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    LOGGER("Startup").info("Load For All Modules")
    LOGGER("Info").info(bot_modules)
    LOGGER("Info").info("Succesfully Load For All Modules")
    await app.send_message(LOG_GROUP_ID,
      f"""
<b>🔥 {app.me.mention} Berhasil Diaktifkan</b>
<b>📘 Python: {python_version()}</b>
<b>📙 Pyrogram: {__version__}</b>
<b>👮‍♂ Userbot: {app2.me.mention}</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Tutup", callback_data="jmbd")]],
        ),
    )
