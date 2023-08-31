"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""


import glob
import os
import random

from PIL import Image, ImageDraw, ImageFont
from pyrogram import enums, filters
from Amang import app2 as client
from Amang import *
from Amang.core.decorators.errors import capture_err

__MODULE__ = "Logo"
__HELP__ = """
/logo [Reply Text or Give Text] - Untuk membuat sebuah logo dengan background random .
"""


@app.on_message(filters.command(["logo"]))
@capture_err
async def logo_gen(_, message):
    if message.reply_to_message:
        name = message.reply_to_message.text
    else:
        name = message.text.split(" ", 1)[1]
    xx = await eor(
                message, text="<code>Processing...</code>")
    if not name:
        await xx.edit("<b>Contoh :</b><code>/logo</code> [text]")
        return
    bg_, font_ = "", ""
    if message.reply_to_message:
        temp = message.reply_to_message
        if temp.media:
            if temp.document:
                if "font" in temp.document.mime_type:
                    font_ = await temp.download()
                elif (".ttf" in temp.document.file_name) or (
                    ".otf" in temp.document.file_name
                ):
                    font_ = await temp.download()
            elif temp.photo:
                bg_ = await temp.download()
    else:
        pics = []
        async for i in client.search_messages(
            "AllLogoHyper", filter=enums.MessagesFilter.PHOTO
        ):
            if i.photo:
                pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download()
        fpath_ = glob.glob("Amang/resources/fonts/*")
        font_ = random.choice(fpath_)
    if not bg_:
        pics = []
        async for i in client.search_messages(
            "AllLogoHyper", filter=enums.MessagesFilter.PHOTO
        ):
            if i.photo:
                pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download()
    if not font_:
        fpath_ = glob.glob("Amang/resources/fonts/*")
        font_ = random.choice(fpath_)
    if len(name) <= 8:
        fnt_size = 120
        strke = 10
    elif len(name) >= 9:
        fnt_size = 50
        strke = 5
    else:
        fnt_size = 100
        strke = 20
    img = Image.open(bg_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_, fnt_size)
    w, h = draw.textsize(name, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        name,
        font=font,
        fill=(255, 255, 255),
    )
    x = (image_width - w) / 2
    y = (image_height - h) / 2
    draw.text(
        (x, y), name, font=font, fill="white", stroke_width=strke, stroke_fill="black"
    )
    flnme = "logo.png"
    img.save(flnme, "png")
    await xx.edit("<code>Uploading</code>")
    if os.path.exists(flnme):
        await message.reply_photo(
            photo=flnme,
            caption=f"<b>Logo by :{app.me.mention}</b>",
        )
        os.remove(flnme)
        await xx.delete()
    if os.path.exists(bg_):
        os.remove(bg_)
    if os.path.exists(font_):
        if not font_.startswith("Amang/resources/fonts"):
            os.remove(font_)
