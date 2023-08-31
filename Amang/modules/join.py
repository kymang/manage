from config import *
from pyrogram import *
from pyrogram.types import *
from pyrogram.errors import *
from Amang import *

NAN = "amwangsupport"

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not NAN:
        return
    try:
        try:
            await bot.get_chat_member(NAN, msg.from_user.id)
        except UserNotParticipant:
            if NAN.isalpha():
                link = f"https://t.me/{NAN}"
            else:
                chat_info = await bot.get_chat(NAN)
                link = chat_info.invite_link
            try:
                await msg.reply(
                    "Si Anjeng, Masuk Sini Dulu Lu Bangsat !",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Sini Nyet Masuk, Jangan Lupa Salam",
                                    url=link,
                                )
                            ]
                        ]
                    ),
                )
                await msg.stop_propagation()
            except UserBannedInChannel:
                await bot.send_message(
                msg.chat.id,
                "**Maaf, Anda tidak dapat menggunakan bot ini karena anda di banned dari Amang Support**\n**Silakan contact @amwng agar dibuka blokir anda.**"
            )
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat : {SUPPORT} !")
