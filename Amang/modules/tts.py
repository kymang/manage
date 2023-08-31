"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
import traceback
from asyncio import get_running_loop
from io import BytesIO
import asyncio
import speech_recognition as sr
import ffmpeg
from gtts import gTTS
from googletrans import Translator
from pyrogram import *
from pyrogram.types import *
import os
from py_trans import Async_PyTranslator
from Amang.utils.tools import *
from Amang import *

__MODULE__ = "Voice"
__HELP__ = """
/tr [kode bahasa] - Terjemahkan bahasa.
/tts [balas teks] - Convert text ke pesan suara.
/stt [balas pesan suara] - Convert pesan suara ke text.
"""

def convert(text):
    audio = BytesIO()
    i = Translator().translate(text, dest="en")
    lang = i.src
    tts = gTTS(text, lang=lang)
    audio.name = f"{lang}.mp3"
    tts.write_to_fp(audio)
    return audio


@app.on_message(filters.command("tts"))
async def text_to_speech(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to some text ffs.")
    if not message.reply_to_message.text:
        return await message.reply_text("Reply to some text ffs.")
    m = await message.reply_text("Processing")
    text = message.reply_to_message.text
    try:
        loop = get_running_loop()
        audio = await loop.run_in_executor(None, convert, text)
        await message.reply_audio(audio)
        await m.delete()
        audio.close()
    except Exception as e:
        await m.edit(e)
        e = traceback.format_exc()
        print(e)



@app.on_message(filters.command(["tr"]))
async def pytrans_tr(_, message: Message):
  tr_msg = await eor(message, text="`Processing...`")
  r_msg = message.reply_to_message
  args = get_arg(message)
  if r_msg:
    if r_msg.text:
      to_tr = r_msg.text
    else:
      return await eor(message, text="`Mohon Balas Ke Pesan..`")
    # Checks if dest lang is defined by the user
    if not args:
      return await eor(message, text=f"`Gunakan tr <kode_bahasa> <kata> atau tr id <balas ke pesan>`")
    # Setting translation if provided
    else:
      sp_args = args.split(" ")
      if len(sp_args) == 2:
        dest_lang = sp_args[0]
        tr_engine = sp_args[1]
      else:
        dest_lang = sp_args[0]
        tr_engine = "google"
  elif args:
    # Splitting provided arguments in to a list
    a_conts = args.split(None, 2)
    # Checks if translation engine is defined by the user
    if len(a_conts) == 3:
      dest_lang = a_conts[0]
      tr_engine = a_conts[1]
      to_tr = a_conts[2]
    else:
      dest_lang = a_conts[0]
      to_tr = a_conts[1]
      tr_engine = "google"
  # Translate the text
  py_trans = Async_PyTranslator(provider=tr_engine)
  translation = await py_trans.translate(to_tr, dest_lang)
  # Parse the translation message
  if translation["status"] == "success":
    tred_txt = f"""
**Translation**: `{translation["engine"]}`
**Translated to:** `{translation["dest_lang"]}`
**Translation:**
`{translation["translation"]}`
"""
    if len(tred_txt) > 4096:
      await eor(message, text="`Teks yang anda berikan terlalu panjang, ini bisa memakakan waktu`\n`Tunggu sebentar..`")
      tr_txt_file = open("translated.txt", "w+")
      tr_txt_file.write(tred_txt)
      tr_txt_file.close()
      await tr_msg.reply_document("translate.txt")
      os.remove("ptranslated.txt")
      await tr_msg.delete()
    else:
      await eor(message, text=tred_txt)
      
@app.on_message(filters.command(["stt"]))
async def speech_to_text(client, message):
    reply = message.reply_to_message
    if not (reply and reply.voice):
        return await message.reply("Mohon Balas Ke Pesan Suara")
    ajg = await message.reply("`Processing...`")
    monyet = await client.download_media(message=reply, file_name='Amang/downloads/voice.ogg')

    @run_in_exc
    def convert_to_raw(audio_original, raw_file_name):
        stream = ffmpeg.input(audio_original)
        stream = ffmpeg.output(stream, raw_file_name, format="wav", acodec="pcm_s16le", ac=2, ar="48k", loglevel="error").overwrite_output().run()
        return raw_file_name


    recognizer = sr.Recognizer()
    babi = await convert_to_raw(monyet, 'Amang/downloads/voice.wav')
    with sr.AudioFile(babi) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="id-ID")
    except sr.UnknownValueError:
        return await ajg.edit("Mohon Periksa Apakah Itu Pesan Suara..")
    except sr.RequestError as e:
        return await ajg.edit("Error {0}".format(e))
    await ajg.edit(
        text=text
    )
    os.remove(babi)
    os.remove(monyet)