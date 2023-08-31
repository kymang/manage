"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
import random
from datetime import datetime
import pytz

from pyrogram import enums, filters

from Amang import *
from Amang.core.decorators.errors import capture_err
from Amang.utils.dbfunctions import get_couple, save_couple

__MODULE__ = "Shippering"
__HELP__ = "/cp or couple - To Choose Couple Of The Day"


# Date and time
def dt():
    # Set the timezone to Indian Standard Time
    ist_timezone = pytz.timezone('Asia/Jakarta')

    # Get the current time in IST
    ist_now = datetime.now(ist_timezone)

    dt_string = ist_now.strftime("%d/%m/%Y %H:%M")
    return dt_string.split(" ")


def dt_tom():
    return (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[1]
    )


def today():
    return str(dt()[0])


def tomorrow():
    return str(dt_tom())


@app.on_message(filters.command(["cp", "couple"]))
@capture_err
async def couple(_, message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("This command only works in groups.")

    m = await message.reply("Detecting gay among us...")

    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today())
        if not is_selected:
            list_of_users = []
            async for i in app.get_chat_members(message.chat.id):
                if not i.user.is_bot and not i.user.is_deleted:
                    user = await app.get_users(i.user.id)
                    list_of_users.append(user.id)
            if len(list_of_users) < 2:
                return await m.edit("Not enough users")
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            c1_mention = (await app.get_users(c1_id)).mention
            c2_mention = (await app.get_users(c2_id)).mention

            couple_selection_message = f"""**Couple of the day:**
{c1_mention} + {c2_mention} = ❤️

__Pasangan baru esok dapat dipilih pada pukul 12 {tomorrow()}__"""
            await m.edit(couple_selection_message)
            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(chat_id, today(), couple)

        else:
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await app.get_users(c1_id)).first_name
            c2_name = (await app.get_users(c2_id)).first_name
            couple_selection_message = f"""Couple of the day:
[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = ❤️

__Pasangan baru hari ini dapat dipilih pada pukul 12 {tomorrow()}__"""
            await m.edit(couple_selection_message)
    except Exception as e:
        print(e)
        await message.reply_text(e)
