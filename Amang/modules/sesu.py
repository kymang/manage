from pyrogram.types import Message
from pyrogram import Client, filters
from config import *
from Amang.utils.dbfunctions import *
import os
import sys
import asyncio
from Amang import *


@app.on_message(
    SUDOERS
    & filters.command("stats"))
async def _stats(_, msg: Message):
    users = len(await get_served_users())
    await msg.reply_text(f"**✓ Kumpulan babi babi liar :\n\nTotal ada `{users}` babi **")


@app.on_message(
    SUDOERS
    & filters.command("bacot"))
async def _bacot(bot: Client, message: Message):
    user = message.from_user.id
    if user not in SUDOERS:
        return await message.reply_text(
            "<b>LU SIAPA MONYED, BABI, BANGSAT, KONTOL, MMK, PELER KUDA, SEMPAK KADAL, KANCUT FIR'AUN,DAKI GORILA, UPIL JERAPA, JEMBUD SINGA, TOPENG MONYET, SOFTEX KUNTILANAK, KOLOR POCONG, POPOK TUYUL, JIGONG GENDERUWO.</b>"
        )
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message is not None:
        text = message.reply_to_message.text
    else:
        return await message.reply(
            "<code>Silakan sertakan pesan atau balas pesan yang ingin disiarkan.</code>"
        )
      
    kntl = 0
    mmk = []
    jmbt = len(await get_served_users())
    babi = await get_served_users()
    for x in babi:
            mmk.append(int(x["user_id"]))
    for i in mmk:
        try:
            await bot.send_message(i, text)
            kntl += 1
        except:
            pass
    return await message.reply(f"**Berhasil memotong {kntl} babi, dari `{jmbt}` babi.**")
