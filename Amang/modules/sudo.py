"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
from pyrogram import filters
from pyrogram.types import Message

from Amang import *
from Amang.core.decorators.errors import capture_err
from Amang.utils.dbfunctions import add_sudo, get_sudoers, remove_sudo

__MODULE__ = "Sudo"
__HELP__ = """
**THIS MODULE IS ONLY FOR DEVS**

.addsudo - To Add A User In Sudoers.
.delsudo - To Remove A User From Sudoers.
.listsudo - To List Sudo Users.

**NOTE:**

Never add anyone to sudoers unless you trust them,
sudo users can do anything with your account, they
can even delete your account.
"""


@app2.on_message(filters.command("addsudo", prefixes=USERBOT_PREFIX) & SUDOERS)
@capture_err
async def useradd(_, message: Message):
    if not message.reply_to_message:
        return await eor(
            message,
            text="Reply to someone's message to add him to sudoers.",
        )
    user_id = message.reply_to_message.from_user.id
    umention = (await app2.get_users(user_id)).mention
    sudoers = await get_sudoers()

    if user_id in sudoers:
        return await eor(message, text=f"{umention} is already in sudoers.")
    if user_id == app.me.id:
        return await eor(message, text="You can't add assistant bot in sudoers.")

    await add_sudo(user_id)

    if user_id not in SUDOERS:
        SUDOERS.add(user_id)

    await eor(
        message,
        text=f"Successfully added {umention} in sudoers.",
    )


@app2.on_message(filters.command("delsudo", prefixes=USERBOT_PREFIX) & SUDOERS)
@capture_err
async def userdel(_, message: Message):
    if not message.reply_to_message:
        return await eor(
            message,
            text="Reply to someone's message to remove him to sudoers.",
        )
    user_id = message.reply_to_message.from_user.id
    umention = (await app2.get_users(user_id)).mention

    if user_id not in await get_sudoers():
        return await eor(message, text=f"{umention} is not in sudoers.")

    await remove_sudo(user_id)

    if user_id in SUDOERS:
        SUDOERS.remove(user_id)

    await eor(
        message,
        text=f"Successfully removed {umention} from sudoers.",
    )


@app2.on_message(filters.command("listsudo", prefixes=USERBOT_PREFIX) & SUDOERS)
@capture_err
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = ""
    j = 0
    for user_id in sudoers:
        try:
            user = await app2.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
            j += 1
        except Exception:
            continue
        text += f"{j}. {user}\n"
    if text == "":
        return await eor(message, text="No sudoers found.")
    await eor(message, text=text)
