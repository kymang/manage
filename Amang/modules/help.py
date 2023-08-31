"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
import re
from pyrogram.enums import *
from pyrogram.types import *
from pyrogram import *
from Amang.core.copas import *
from Amang.modules.sudoers import bot_sys_stats
from Amang.utils import paginate_modules
from Amang.utils.constants import MARKDOWN
from config import *
from Amang import *

home_keyboard_pm = InlineKeyboardMarkup(
    [
        [ 
            InlineKeyboardButton(text="Buat String Session 📝", callback_data="generate"),
        ],
        [
            InlineKeyboardButton(text="Perintah Lainnya ❓", callback_data="helpernya"),
            InlineKeyboardButton(text="Perintah Multi Fungsi 🤖", callback_data="multi_funsgi"),
        ],
        [
            InlineKeyboardButton(
                text="Jasa Bot 🖥",
                callback_data="jasa_repo",
            ),
            InlineKeyboardButton(text="Support 👥", url=f"https://t.me/amwangsupport"),
        ],
        [
            InlineKeyboardButton(
                text="➕ Tambahkan Saya Ke Grup Anda ➕",
                url=f"http://t.me/{app.me.username}?startgroup=new",
            )
        ],
    ]
)

home_text_pm = (
    "**ʜᴇʟʟᴏ {}, sᴀʏᴀ ᴀᴅᴀʟᴀʜ ʙᴏᴛ ᴅᴇɴɢᴀɴ ʙᴇʀʙᴀɢᴀɪ ꜰᴜɴɢsɪ.**")

keyboard = InlineKeyboardMarkup(
    [
        [ 
            InlineKeyboardButton(text="Buat String Session 📝", callback_data="generate"),
        ],
        [
            InlineKeyboardButton(text="Perintah Lainnya ❓", callback_data="bot_commands"),
            InlineKeyboardButton(text="Perintah Multi Fungsi 🤖", callback_data="multi_funsgi"),
        ],
        [
            InlineKeyboardButton(
                text="Jasa Bot 🖥",
                callback_data="jasa_repo",
            ),
            InlineKeyboardButton(text="Support 👥", url=f"https://t.me/amwangsupport"),
        ],
        [
            InlineKeyboardButton(
                text="➕ Tambahkan Saya Ke Grup Anda ➕",
                url=f"http://t.me/{app.me.username}?startgroup=new",
            )
        ],
    ]
)


@app.on_message(filters.command("start"))
async def start(_, message):
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply("Kirim pesan pribadi untuk melihat bantuan.", reply_markup=keyboard)
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )
        elif "_" in name:
            module = name.split("_", 1)[1]
            text = (
                f"Ini bantuan untuk **{HELPABLE[module].__MODULE__}**:\n"
                + HELPABLE[module].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        elif name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply(
                text,
                reply_markup=keyb,
            )
    else:
        await message.reply(
            home_text_pm.format(
              message.from_user.mention, app.me.mention),
            reply_markup=home_keyboard_pm,
        )
    return


@app.on_message(filters.command("help"))
async def help_command(_, message):
    if message.chat.type != ChatType.PRIVATE:
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Klik disini",
                                url=f"t.me/{app.me.username}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply(
                    f"Klik tombol bantuan dibawah untuk mendapatkan bantuan {name}",
                    reply_markup=key,
                )
            else:
                await message.reply("Kirim pesan pribadi untuk melihat bantuan.", reply_markup=keyboard)
        else:
            await message.reply("Kirim pesan pribadi untuk melihat bantuan.", reply_markup=keyboard)
    elif len(message.command) >= 2:
        name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
        if str(name) in HELPABLE:
            text = (
                f"Ini bantuan untuk **{HELPABLE[name].__MODULE__}**:\n"
                + HELPABLE[name].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        else:
            text, help_keyboard = await help_parser(message.from_user.first_name)
            await message.reply(
                text,
                reply_markup=help_keyboard,
                disable_web_page_preview=True,
            )
    else:
        text, help_keyboard = await help_parser(message.from_user.first_name)
        await message.reply(
            text, reply_markup=help_keyboard, disable_web_page_preview=True
        )
    return


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """**Ini adalah daftar perintah {bot_name}.**
""".format(
            first_name=name,
            bot_name=app.me.mention,
        ),
        keyboard,
    )

@app.on_callback_query(filters.regex("ahh_ajg"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=home_text_pm.format(
                CallbackQuery.from_user.mention,
                app.me.mention),
        reply_markup=keyboard,
    )
    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await app.answer_callback_query(CallbackQuery.id, text, show_alert=True)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""
**Ini adalah daftar perintah.**
 """
    if mod_match:
        module = mod_match[1].replace(" ", "_")
        text = f"Ini adalah bantuan untuk **{HELPABLE[module].__MODULE__}**:\n{HELPABLE[module].__HELP__}"

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Kembali", callback_data="help_back")]]
            ),
            disable_web_page_preview=True,
        )
    elif home_match:
        await app.send_message(
            query.from_user.id,
            text=home_text_pm.format(
                query.from_user.mention,
                app.me.mention),
            reply_markup=home_keyboard_pm,
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match[1])
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match[1])
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)
    
    
@app.on_callback_query(filters.regex("jmbd"))
async def now(_, query):
    await query.message.delete()

