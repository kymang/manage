# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT
"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat
"""

import glob
import os
import random

from pyrogram import *
from pyrogram.types import *
from Amang import *
from PIL import *
from Amang.core.decorators.errors import capture_err

__MODULE__ = "Nulis"
__HELP__ = """
/nulis [text/reply to text/media] - Buat kamu yang malas nulis.

"""

def text_set(text):
    lines = []
    if len(text) <= 55:
        lines.append(text)
    else:
        all_lines = text.split("\n")
        for line in all_lines:
            if len(line) <= 55:
                lines.append(line)
            else:
                k = len(line) // 55
                lines.extend(line[((z - 1) * 55) : (z * 55)] for z in range(1, k + 2))
    return lines[:25]
    
    
@app.on_message(filters.command(["nulis"]))
@capture_err
async def ABC(_, message):
    if message.reply_to_message:
        Amang = message.reply_to_message.text
    else:
        Amang = get_text(message)
    nan = await eor(message, text="`Processing...`")
    try:
        img = Image.open("Amang/resources/kertas.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Amang/resources/fonts/assfont.ttf", 30)
        x, y = 150, 140
        lines = text_set(Amang)
        line_height = font.getsize("hg")[1]
        for line in lines:
            draw.text((x, y), line, fill=(1, 22, 55), font=font)
            y = y + line_height - 5
        file = "nulis.jpg"
        img.save(file)
        if os.path.exists(file):
            await message.reply_photo(
                photo=file,
                caption=f"<b>Ditulis Oleh :</b> {app.me.mention}"
            )
            os.remove(file)
            await nan.delete()
    except Exception as e:
        return await message.reply(e)