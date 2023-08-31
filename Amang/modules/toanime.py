# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT
# Credits : TomiX

import random
from random import choice
import asyncio
import os
import shutil
import time
from py_extract import Video_tools
from pyrogram import Client, filters, enums
from pyrogram.types import *
from pyrogram.raw.functions.messages import DeleteHistory
from Amang import *
from Amang.utils.tools import *
from Amang import app2 as client

__MODULE__ = "To Anime"
__HELP__ = """
/toanime [balas foto] - Ubah foto menjadi anime, wajah harus terlihat.
/toaudio [balas ke video] - Extract suara dari video.
/efek [nama efek] [balas audio] - Ubah audio suara dengan menambahkan efek.
"""


async def dl_pic(client, download):
    path = await client.download_media(download)
    with open(path, "rb") as f:
        content = f.read()
    os.remove(path)
    return BytesIO(content)

@app.on_message(filters.command(["toaudio"]))
async def convert_audio(_, message):
    replied_msg = message.reply_to_message
    ajg = await eor(message, text="`Downloading Video . . .`")
    ext_out_path = f"{os.getcwd()}/Amang/resources/"
    if not replied_msg:
        await eor(message, text="`Mohon Balas Ke Video`")
        return
    if not replied_msg.video:
        await eor(message, text="`Mohon Balas Ke Video`")
        return
    if os.path.exists(ext_out_path):
        await eor(message, text="`Processing...`")
        return
    replied_video = replied_msg.video
    try:
        await eor(message, text="`Downloading...`")
        ext_video = await app2.download_media(replied_video)
        await eor(message, text="`Converting...`")
        exted_aud = Video_tools.extract_all_audio(
            input_file=ext_video, output_path=ext_out_path
        )
        await eor(message, text="`Uploading...`")
        for nexa_aud in exted_aud:
            await message.reply_audio(
                audio=nexa_aud, caption=f"`Extracted by` {app.me.mention}"
            )
        await eor(message, text="`Extracting Finished!`")
        shutil.rmtree(ext_out_path)
    except Exception as e:
        await eor(message, text=f"**Error:** `{e}`")


@app.on_message(filters.command(["toanime"]))
async def convert_anime(_, message):
    Tm = await message.reply("<code>Processing...</code>")
    if message.reply_to_message:
        if len(message.command) < 2:
            if message.reply_to_message.photo:
                file = "foto"
                get_photo = message.reply_to_message.photo.file_id
            elif message.reply_to_message.sticker:
                file = "sticker"
                get_photo = await dl_pic(app2, message.reply_to_message)
            elif message.reply_to_message.animation:
                file = "gift"
                get_photo = await dl_pic(app2, message.reply_to_message)
            else:
                return await eor(message, text=
                    "<code>Mohon balas ke foto</code>"
                )
        elif message.command[1] in ["foto", "profil", "photo"]:
            file = "foto profil"
            chat = (
                message.reply_to_message.from_user
                or message.reply_to_message.sender_chat
            )
            get = await app.get_chat(chat.id)
            photo = get.photo.big_file_id
            get_photo = await dl_pic(app2, photo)
    else:
        if len(message.command) < 2:
            return await eor(message, text=
                "`Mohon balas ke foto...`"
            )
        try:
            file = "foto"
            get = await app.get_chat(message.command[1])
            photo = get.photo.big_file_id
            get_photo = await dl_pic(app2, photo)
        except Exception as error:
            return await eor(message, text=error)
    await eor(message, text="<code>Processing...</code>")
    await app2.unblock_user("@qq_neural_anime_bot")
    send_photo = await app2.send_photo("@qq_neural_anime_bot", get_photo)
    await asyncio.sleep(30)
    await send_photo.delete()
    await Tm.delete()
    info = await app2.resolve_peer("@qq_neural_anime_bot")
    anime_photo = []
    async for anime in app2.search_messages(
        "@qq_neural_anime_bot", filter=MessagesFilter.PHOTO
    ):
        anime_photo.append(
            InputMediaPhoto(
                anime.photo.file_id, caption=f"<b>Created by : {app.me.mention}</b>"
            )
        )
    if anime_photo:
        await app.send_media_group(
            message.chat.id,
            anime_photo,
            reply_to_message_id=message.id,
        )
    else:
        await app.send_message(
            message.chat.id,
            f"<code>Gagal merubah {file}</code>",
            reply_to_message_id=message.id,
        )

    return await app2.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))


@app.on_message(filters.command("efek"))
async def convert_efek(_, message):
    helo = get_arg(message)
    rep = message.reply_to_message
    if rep and helo:
        tau = ["bengek", "robot", "jedug", "fast", "echo"]
        if helo in tau:
            Tm = await message.reply(f"`Processing, mengubah suara ke {helo}`")
            indir = await client.download_media(rep)
            KOMUT = {
                "bengek": '-filter_complex "rubberband=pitch=1.5"',
                "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
                "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
                "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
                "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
            }
            ses = await asyncio.create_subprocess_shell(
                f"ffmpeg -i '{indir}' {KOMUT[helo]} audio.mp3"
            )
            await ses.communicate()
            await Tm.delete()
            await rep.reply_voice("audio.mp3", caption=f"Efek {helo}")
            os.remove("audio.mp3")
        else:
            await message.reply(f"`Silakan format yang anda inginkan : {tau}`")
    else:
        await eor(
            message,
            text="`Silakan masukkan : <code>/efek bengek</code> balas ke ke audio atau mp3.`",
        )