"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""

from pyrogram import filters

from Amang import *


@app2.on_message(filters.command("alive", prefixes=USERBOT_PREFIX) & SUDOERS)
async def alive_command_func(_, message):
    await message.delete()
    results = await app2.get_inline_bot_results(app.me.username, "alive")
    await app2.send_inline_bot_result(
        message.chat.id, results.query_id, results.results[0].id
    )
