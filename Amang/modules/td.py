"""
Project [DarkWeb](https://github.com/TeamKillerX/DarkWeb) is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT
"""

import asyncio
import random

import Amang.modules.truth_and_dare_string as tod

from Amang import *


# LU GABISA CODING LU KONTOL
# BELAJAR CODING DARI NOL
@app.on_message(filters.command(["apakah"]))
async def apakah(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.AP)}")



@app.on_message(filters.command(["kenapa"]))
async def kenapa(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.KN)}")


@app.on_message(filters.command(["bagaimana"]))
async def bagaimana(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.BG)}")


@app.on_message(filters.command(["dare"]))
async def dare(client, message):
    try:        
        await message.reply_text(f"{random.choice(tod.DARE)}")
    except BaseException:
        pass


@app.on_message(filters.command(["truth"]))
async def truth(client, message):
    try:
        await message.reply_text(f"{random.choice(tod.TRUTH)}")
    except Exception:
        pass



__MODULE__ = "For Fun"
__HELP__ = """
/apakah - Coba sendiri.
/kenapa - Coba sendiri.
/bagaimana - Coba sendiri.
/truth - Coba sendiri.
/dare - Coba sendiri.
"""
