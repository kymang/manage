"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""

from pyrogram import filters

from Amang import SUDOERS, USERBOT_PREFIX, app2
from Amang.modules.userbot import eor


@app2.on_message(
    SUDOERS
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.command("create", prefixes=USERBOT_PREFIX)
)
async def create(_, message):
    if len(message.command) < 3:
        return await eor(message, text="__**.create (b|s|c) Name**__")
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    desc = "Welcome To My " + ("Supergroup" if group_type == "s" else "Channel")
    if group_type == "b":  # for basicgroup
        chat = await app2.create_group(group_name, app.me.username)
        link = await app2.get_chat(chat.id)
        await eor(
            message,
            text=f"**Basicgroup Created: [{group_name}]({link.invite_link})**",
            disable_web_page_preview=True,
        )
    elif group_type == "s":  # for supergroup
        chat = await app2.create_supergroup(group_name, desc)
        link = await app2.get_chat(chat.id)
        await eor(
            message,
            text=f"**Supergroup Created: [{group_name}]({link.invite_link})**",
            disable_web_page_preview=True,
        )
    elif group_type == "c":  # for channel
        chat = await app2.create_channel(group_name, desc)
        link = await app2.get_chat(chat.id)
        await eor(
            message,
            text=f"**Channel Created: [{group_name}]({link.invite_link})**",
            disable_web_page_preview=True,
        )
