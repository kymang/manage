import asyncio
import os
import re
import shutil
import tempfile

from PIL import Image
from pyrogram import emoji, filters, enums, Client
from pyrogram.errors import BadRequest, PeerIdInvalid, StickersetInvalid
from pyrogram.file_id import FileId
from pyrogram.raw.functions.messages import GetStickerSet, SendMedia
from pyrogram.raw.functions.stickers import AddStickerToSet, CreateStickerSet, RemoveStickerFromSet
from pyrogram.raw.types import DocumentAttributeFilename, InputDocument, InputMediaUploadedDocument, InputStickerSetItem, InputStickerSetShortName
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Amang import *
from Amang.utils.http import http
from config import *

__MODULE__ = "Stickers"
__HELP__ = """
/kang [Reply to sticker] - Add sticker to your pack.
/unkang [Reply to sticker] - Remove sticker from your pack (Only can remove sticker that added by this bot.).
/getsticker - Convert sticker to png.
/stickerid - View sticker ID.
/mmf [balas sticker] - Kata atas;Kata Bawah.
/tiny [balas stiker] - Membuat gambar menjadi kecil.
"""


def get_emoji_regex():
    e_list = [getattr(emoji, e).encode("unicode-escape").decode("ASCII") for e in dir(emoji) if not e.startswith("_")]
    # to avoid re.error excluding char that start with '*'
    e_sort = sorted([x for x in e_list if not x.startswith("*")], reverse=True)
    # Sort emojis by length to make sure multi-character emojis are
    # matched first
    pattern_ = f"({'|'.join(e_sort)})"
    return re.compile(pattern_)


EMOJI_PATTERN = get_emoji_regex()
SUPPORTED_TYPES = ["jpeg", "png", "webp"]


@app.on_message(filters.command(["getsticker"]))
async def getsticker_(self: Client, message: Message):
    if not message.reply_to_message or message.reply_to_message.sticker:
        await eor(message, text="`Ini bukan stiker!`")
    else:
        sticker = message.reply_to_message.sticker
        if sticker.is_animated:
            await eor(message, text="`Harap balas ke non animasi.`")
        else:
            with tempfile.TemporaryDirectory() as tempdir:
                path = os.path.join(tempdir, "getsticker")
            sticker_file = await self.download_media(
                message=message.reply_to_message,
                file_name=f"{path}/{sticker.set_name}.png",
            )
            await message.reply_to_message.reply_document(
                document=sticker_file,
                caption=f"<b>Emoji:</b> {sticker.emoji}\n" f"<b>Sticker ID:</b> <code>{sticker.file_id}</code>\n\n" f"<b>Send by:</b> @{BOT_USERNAME}",
            )
            shutil.rmtree(tempdir, ignore_errors=True)


@app.on_message(filters.command("stickerid"))
async def getstickerid(self: Client, message: Message):
    if message.reply_to_message.sticker:
        await message.reply_msg(f"The ID of this sticker is: <code>{message.reply_to_message.sticker.file_id}</code>")


@app.on_message(filters.command("unkang"))
async def getstickerid(self: Client, message: Message):
    if message.reply_to_message.sticker:
        pp = await eor(message, text="Mencoba menghapus dari paket..")
        try:
            decoded = FileId.decode(message.reply_to_message.sticker.file_id)
            sticker = InputDocument(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference,
            )
            await app.invoke(RemoveStickerFromSet(sticker=sticker))
            await pp.edit_text("Stiker berhasil dihapus dari paket anda.")
        except Exception as e:
            await pp.edit_text(f"Gagal menghapus stiker dari paket Anda.\n\nERR: {e}")
    else:
        await eor(message, text=f"Tolong balas stiker yang dibuat oleh {self.me.username} untuk menghapus stiker dari paket Anda.")


@app.on_message(filters.command(["curi", "kang"]))
async def kang_sticker(self: Client, message: Message):
    if not message.from_user:
        return await eor(message, text="Anda adalah admin anon, stiker kang ada di pm saya.")
    prog_msg = await eor(message, text="Mencoba mencuri stiker Anda...")
    sticker_emoji = "🤔"
    packnum = 0
    packname_found = False
    resize = False
    animated = False
    videos = False
    convert = False
    reply = message.reply_to_message
    user = await self.resolve_peer(message.from_user.username or message.from_user.id)

    if reply and reply.media:
        if reply.photo:
            resize = True
        elif reply.animation:
            videos = True
            convert = True
        elif reply.video:
            convert = True
            videos = True
        elif reply.document:
            if "image" in reply.document.mime_type:
                # mime_type: image/webp
                resize = True
            elif reply.document.mime_type in (
                enums.MessageMediaType.VIDEO,
                enums.MessageMediaType.ANIMATION,
            ):
                # mime_type: application/video
                videos = True
                convert = True
            elif "tgsticker" in reply.document.mime_type:
                # mime_type: application/x-tgsticker
                animated = True
        elif reply.sticker:
            if not reply.sticker.file_name:
                return await prog_msg.edit_text("Stiker tidak memiliki nama.")
            if reply.sticker.emoji:
                sticker_emoji = reply.sticker.emoji
            animated = reply.sticker.is_animated
            videos = reply.sticker.is_video
            if videos:
                convert = False
            elif not reply.sticker.file_name.endswith(".tgs"):
                resize = True
        else:
            return await prog_msg.edit_text()

        pack_prefix = "anim" if animated else "vid" if videos else "a"
        packname = f"{pack_prefix}_{message.from_user.id}_by_{self.me.username}"

        if len(message.command) > 1 and message.command[1].isdigit() and int(message.command[1]) > 0:
            # provide pack number to kang in desired pack
            packnum = message.command.pop(1)
            packname = f"{pack_prefix}{packnum}_{message.from_user.id}_by_{self.me.username}"
        if len(message.command) > 1:
            # matches all valid emojis in input
            sticker_emoji = "".join(set(EMOJI_PATTERN.findall("".join(message.command[1:])))) or sticker_emoji
        filename = await self.download_media(message.reply_to_message)
        if not filename:
            # Failed to download
            await prog_msg.delete()
            return
    elif message.entities and len(message.entities) > 1:
        pack_prefix = "a"
        filename = "sticker.png"
        packname = f"c{message.from_user.id}_by_{self.me.username}"
        img_url = next(
            (message.text[y.offset : (y.offset + y.length)] for y in message.entities if y.type == "url"),
            None,
        )

        if not img_url:
            await prog_msg.delete()
            return
        try:
            r = await http.get(img_url)
            if r.status_code == 200:
                with open(filename, mode="wb") as f:
                    f.write(r.read())
        except Exception as r_e:
            return await prog_msg.edit_text(f"{r_e.__class__.__name__} : {r_e}")
        if len(message.command) > 2:
            # m.command[1] is image_url
            if message.command[2].isdigit() and int(message.command[2]) > 0:
                packnum = message.command.pop(2)
                packname = f"a{packnum}_{message.from_user.id}_by_{self.me.username}"
            if len(message.command) > 2:
                sticker_emoji = "".join(set(EMOJI_PATTERN.findall("".join(message.command[2:])))) or sticker_emoji
            resize = True
    else:
        return await prog_msg.edit_text("Ingin saya menebak stikernya? Harap tandai stiker.")
    try:
        if resize:
            filename = resize_image(filename)
        elif convert:
            filename = await convert_video(filename)
            if filename is False:
                return await prog_msg.edit_text("Error")
        max_stickers = 50 if animated else 120
        while not packname_found:
            try:
                stickerset = await self.invoke(
                    GetStickerSet(
                        stickerset=InputStickerSetShortName(short_name=packname),
                        hash=0,
                    )
                )
                if stickerset.set.count >= max_stickers:
                    packnum += 1
                    packname = f"{pack_prefix}_{packnum}_{message.from_user.id}_by_{self.me.username}"
                else:
                    packname_found = True
            except StickersetInvalid:
                break
        file = await self.save_file(filename)
        media = await self.invoke(
            SendMedia(
                peer=(await self.resolve_peer(LOG_GROUP_ID)),
                media=InputMediaUploadedDocument(
                    file=file,
                    mime_type=self.guess_mime_type(filename),
                    attributes=[DocumentAttributeFilename(file_name=filename)],
                ),
                message=f"#Sticker kang by UserID -> {message.from_user.id}",
                random_id=self.rnd_id(),
            ),
        )
        msg_ = media.updates[-1].message
        stkr_file = msg_.media.document
        if packname_found:
            await prog_msg.edit_text("<code>Menggunakan paket stiker yang ada...</code>")
            await self.invoke(
                AddStickerToSet(
                    stickerset=InputStickerSetShortName(short_name=packname),
                    sticker=InputStickerSetItem(
                        document=InputDocument(
                            id=stkr_file.id,
                            access_hash=stkr_file.access_hash,
                            file_reference=stkr_file.file_reference,
                        ),
                        emoji=sticker_emoji,
                    ),
                )
            )
        else:
            await prog_msg.edit_text("<b>Membuat paket stiker baru...</b>")
            stkr_title = f"{message.from_user.first_name}'s"
            if animated:
                stkr_title += "AnimPack"
            elif videos:
                stkr_title += "VidPack"
            if packnum != 0:
                stkr_title += f" v{packnum}"
            try:
                await self.invoke(
                    CreateStickerSet(
                        user_id=user,
                        title=stkr_title,
                        short_name=packname,
                        stickers=[
                            InputStickerSetItem(
                                document=InputDocument(
                                    id=stkr_file.id,
                                    access_hash=stkr_file.access_hash,
                                    file_reference=stkr_file.file_reference,
                                ),
                                emoji=sticker_emoji,
                            )
                        ],
                        animated=animated,
                        videos=videos,
                    )
                )
            except PeerIdInvalid:
                return await prog_msg.edit_text("Tampaknya Anda belum pernah berinteraksi dengan saya dalam obrolan pribadi, Anda harus melakukannya dulu.."),
    except BadRequest:
        return await prog_msg.edit_text("Paket Stiker Anda penuh jika paket Anda tidak dalam Tipe v1 /kang 1, jika tidak dalam Tipe v2 /kang 2 dan seterusnya.")
    except Exception as all_e:
        await prog_msg.edit_text(f"{all_e.__class__.__name__} : {all_e}")
    else:
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="👀 Lihat Paket",
                        url=f"https://t.me/addstickers/{packname}"),
                ],
            ]
        )
        await prog_msg.edit_text("<b>Stiker berhasil dicuri!</b>\n<b>Emoji:</b> {sticker_emoji}",
        reply_markup=markup,
        )
        # Cleanup
        await self.delete_messages(chat_id=LOG_GROUP_ID, message_ids=msg_.id, revoke=True)
        try:
            os.remove(filename)
        except OSError:
            pass


def resize_image(filename: str) -> str:
    im = Image.open(filename)
    maxsize = 512
    scale = maxsize / max(im.width, im.height)
    sizenew = (int(im.width * scale), int(im.height * scale))
    im = im.resize(sizenew, Image.NEAREST)
    downpath, f_name = os.path.split(filename)
    # not hardcoding png_image as "sticker.png"
    # not hardcoding png_image as "sticker.png"
    png_image = os.path.join(downpath, f"{f_name.split('.', 1)[0]}.png")
    im.save(png_image, "PNG")
    if png_image != filename:
        os.remove(filename)
    return png_image


async def convert_video(filename: str) -> str:
    downpath, f_name = os.path.split(filename)
    webm_video = os.path.join(downpath, f"{f_name.split('.', 1)[0]}.webm")
    cmd = [
        "downloads",
        "-loglevel",
        "quiet",
        "-i",
        filename,
        "-t",
        "00:00:03",
        "-vf",
        "fps=30",
        "-c:v",
        "vp9",
        "-b:v:",
        "500k",
        "-preset",
        "ultrafast",
        "-s",
        "512x512",
        "-y",
        "-an",
        webm_video,
    ]

    proc = await asyncio.create_subprocess_exec(*cmd)
    # Wait for the subprocess to finish
    await proc.communicate()

    if webm_video != filename:
        os.remove(filename)
    return webm_video
