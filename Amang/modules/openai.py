"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""



import openai
from pyrogram import filters
from config import OPENAI_API
from Amang import *
from Amang.core.decorators.errors import capture_err

__MODULE__ = "OpenAi"
__HELP__ = """
/ai or ask - Untuk mengajukan pertanyaan ke AI.

/img - Untuk mencari gambar ke AI.
"""


class OpenAi:
    def text(self):
        openai.api_key = OPENAI_API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Q: {self}\nA:",
            temperature=0,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text

    def photo(self):
        openai.api_key = OPENAI_API
        response = openai.Image.create(prompt=self, n=1, size="1024x1024")
        return response["data"][0]["url"]


@app.on_message(filters.command(["ai", "ask"]))
@capture_err
async def ask(_, message):
    tt = await message.reply_text("<code>Processing...</code>")
    if len(message.command) < 2:
        return await eor(
            message, text="<b>Gunakan format :<code>ai</code> [pertanyaan]</b>"
        )
    try:
        response = OpenAi.text(message.text.split(None, 1)[1])
        await tt.delete()
        await message.reply_text(response)

    except Exception as error:
        await message.reply_text(error)
        await tt.delete()


@app.on_message(filters.command(["img"]))
@capture_err
async def img(_, message):
    tt = await message.reply_text("<code>Processing...</code>")
    if len(message.command) < 2:
        return await eor(
            message, text="<b>Gunakan format :<code>ai</code> [pertanyaan]</b>"
        )
    try:
        response = OpenAi.photo(message.text.split(None, 1)[1])
        msg = message.reply_to_message or message
        await message.reply_photo(response, reply_to_message_id=msg.id)
        return await tt.delete()
    except Exception as error:
        await message.reply_text(error)
        return await tt.delete()
