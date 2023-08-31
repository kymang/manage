import random
from random import choice

from pyrogram import *
from pyrogram.types import *
from Amang import *



@app.on_message(filters.command("asupan"))
async def _(client, message):
    y = await eor(message, text="<b>🔍 Mencari Video Asupan...</b>")
    try:
        asupan = []
        async for asu in app2.search_messages(
            "AsupanNyaSaiki", filter=enums.MessagesFilter.VIDEO, limit=1):
                asupan.append(asu)
                video = random.choice(asupan)
                ajg = await app2.download_media(video)
                await message.reply_video(
                    video=ajg,
                    caption=f"<b>Asupan By {app.me.mention}</b>",
                )
                await y.delete()
    except Exception as e:
        await y.edit(f"**Error `{e}`**")



@app.on_message(filters.command("cewe"))
async def _(client, message):
    y = await eor(message, text="<b>🔍 Mencari Cewe...</b>")
    try:
        cewe = []
        async for ce in app2.search_messages(
            "AyangSaiki", filter=enums.MessagesFilter.PHOTO, limit=1):
                cewe.append(ce)
                poto = random.choice(cewe)
                ajg = await app2.download_media(poto)
                await message.reply_photo(
                    photo=ajg,
                    caption=f"<b>Cewe By {app.me.mention}</b>",
                )
                await y.delete()
    except Exception as e:
        await y.edit(f"**Error `{e}`**")



@app.on_message(filters.command("cowo"))
async def _(_, message):
    y = await eor(message, text="<b>🔍 Mencari Cowo...</b>")
    try:
        cowo = []
        async for co in app2.search_messages(
            "Ayang2Saiki", filter=enums.MessagesFilter.PHOTO, limit=1):
                cowo.append(co)
                poto = random.choice(cowo)
                ajg = await app2.download_media(poto)
                await message.reply_photo(
                    photo=ajg,
                    caption=f"**Cowo By {app.me.mention}</b>",
                )
                await y.delete()
    except Exception:
        await y.edit(f"**Error `{e}`**")



@app.on_message(filters.command("anime"))
async def _(_, message):
    y = await eor(message, text="<b>🔍 Mencari Anime...</b>")
    try:
        anime = []
        async for an in app2.search_messages(
            "animehikarixa", filter=enums.MessagesFilter.PHOTO, limit=1):
                anime.append(an)
                poto = random.choice(anime)
                ajg = await app2.download_media(poto)
                await message.reply_photo(
                    photo=ajg,
                    caption=f"<b>Anime By {app.me.mention}</b>",
                )
                await y.delete()
    except Exception:
        await y.edit(f"**Error `{e}`**")
  

@app.on_message(filters.command("anime2"))
async def _(_, message):
    y = await eor(message, text="<b>🔍 Mencari Anime...</b>")
    try:
        animek = []
        async for ani in app2.search_messages(
            "Anime_WallpapersHD", filter=enums.MessagesFilter.PHOTO, limit=1):
                animek.append(ani)
                poto = random.choice(animek)
                ajg = await app2.download_media(poto)
                await message.reply_photo(
                    photo=ajg,
                    caption=f"<b>Anime By {app.me.mention}</b>",
                )
                await y.delete()
    except Exception:
        await y.edit(f"**Error `{e}`**")


@app.on_message(filters.command("ppcp"))
async def _(_, message):
    y = await eor(message, text="<b>🔍 Mencari Anime...</b>")
    try:
        ppcp = []
        async for pp in app2.search_messages(
            "mentahanppcp", filter=enums.MessagesFilter.PHOTO, limit=1):
                ppcp.append(pp)
                poto = random.choice(ppcp)
                ajg = await app2.download_media(poto)
                await message.reply_photo(
                    photo=ajg,
                    caption=f"<b>PP Couple By {app.me.mention}</b>",
                )
                await y.delete()
    except Exception:
        await y.edit(f"**Error `{e}`**")


@app.on_message(filters.command("ppcp2"))
async def _(_, message):
    y = await eor(message, text="<b>🔍 Mencari Anime...</b>")
    try:
        ppcp2 = []
        async for pe in app2.search_messages(
            "ppcpcilik", filter=enums.MessagesFilter.PHOTO, limit=1):
                ppcp2.append(pe)
                poto = random.choice(ppcp2)
                ajg = await app2.download_media(poto)
                await message.reply_photo(
                    photo=ajg,
                    caption=f"<b>PP Couple By {app.me.mention}</b>",
                )
                await y.delete()
    except Exception:
        await y.edit(f"**Error `{e}`**")


@app.on_message(filters.command("pap"))
async def _(_, message):
    y = await eor(message, text="<b>🔍 Mencari Pap...</b>")
    try:
        pap = []
        async for pa in app2.search_messages(
            "mm_kyran", filter=enums.MessagesFilter.PHOTO, limit=1):
                pap.append(pa)
                poto = random.choice(pap)
                ajg = await app2.download_media(poto)
                await message.reply_photo(
                    photo=ajg,
                    caption=f"<b>Untuk Kamu Dari {app.me.mention}</b>",
                )
                await y.delete()
    except Exception:
        await y.edit(f"**Error `{e}`**")


__MODULE__ = "Asupan"
__HELP__ = f"""
/asupan - Untuk mengirim video asupan random. 

/cewe - Untuk mengirim photo cewek random.
           
/cowo - Untuk mengirim photo cowok random.

/anime - Untuk mengirim photo anime random.
           
/anime2 - Untuk mengirim photo anime random.

/ppcp - Untuk mengirim photo ppcp random.
           
/ppcp2 - Untuk mengirim photo ppcp random.

/pap - Untuk mengirim photo pap random.
"""
