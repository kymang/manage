"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
import re
from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.types import ChatPermissions

from Amang import *
from Amang.core.decorators.errors import capture_err
from Amang.core.decorators.permissions import adminsOnly
from Amang.modules.admin import list_admins
from Amang.utils.dbfunctions import (
    delete_blacklist_filter,
    get_blacklisted_words,
    save_blacklist_filter,
)
from Amang.utils.tools import get_arg, get_text
from Amang.utils.filter_groups import blacklist_filters_group

__MODULE__ = "Blacklist"
__HELP__ = """
/blacklisted or /listbl- Get All The Blacklisted Words In The Chat.
/blacklist or /bl [balas pesan|berikan kata] - Blacklist A Word Or A Sentence.
/whitelist or /wl [kata kunci] - Whitelist A Word Or A Sentence.
"""


@app.on_message(filters.command(["blacklist", "bl"]) & ~filters.private)
@adminsOnly("can_restrict_members")
async def save_filters(_, message):
    if message.reply_to_message:
        kata = message.reply_to_message.text
    else:
        kata = message.text.split(None, 1)[1]
    if not kata:
        return await message.reply_text("**Usage**\n__/blacklist [balas pesan/berikan kata]__")
    await message.reply_to_message.delete()
    await message.delete()
    chat_id = message.chat.id
    await save_blacklist_filter(chat_id, kata)
    await message.reply_text(f"__**Blacklisted {kata}.**__")


@app.on_message(filters.command(["blacklisted", "listbl"]) & ~filters.private)
@capture_err
async def get_filterss(_, message):
    data = await get_blacklisted_words(message.chat.id)
    if not data:
        await message.reply_text("**No blacklisted words in this chat.**")
    else:
        msg = f"List of blacklisted words in {message.chat.title} :\n"
        for word in data:
            msg += f"**-** `{word}`\n"
        await message.reply_text(msg)


@app.on_message(filters.command(["whitelist", "wl"]) & ~filters.private)
@adminsOnly("can_restrict_members")
async def del_filter(_, message):
    if message.reply_to_message:
        kata = message.reply_to_message.text
    else:
        kata = message.text.split(None, 1)[1].strip()
    if not kata:
        return await message.reply_text("**Usage**\n__/whitelist [berikan kata]__")
    chat_id = message.chat.id
    deleted = await delete_blacklist_filter(chat_id, kata)
    if deleted:
        return await message.reply_text(f"**Whitelisted {kata}.**")
    await message.reply_text("**No such blacklist filter.**")


@app.on_message(filters.text & filters.group, group=1)
@capture_err
async def blacklist_filters_re(_, message):
    text = message.text.lower().strip()
    if not text:
        return
    chat_id = message.chat.id
    user = message.from_user
    if not user:
        return
    if user.id in SUDOERS:
        return
    list_of_filters = await get_blacklisted_words(chat_id)
    for word in list_of_filters:
        pattern = r"( |^|[^\w])" + re.escape(word) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            if user.id in await list_admins(chat_id):
                return
            if user.id:
                try:
                    until_date = datetime.now() + timedelta(hours=24)
                    await message.delete()
#                    await message.chat.restrict_member(
#                        user.id,
#                        ChatPermissions(),
#                        until_date=until_date,
#                    )
                except Exception as e:
                    print(e)
#                return await app.send_message(
#                    chat_id,
#                    f"Saya menghapus pesan dia {user.mention} [`{user.id}`] "
#                    + f"Karna menggunakan kata terlarang {word}.",
#                )

