"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
import asyncio
import time
from inspect import getfullargspec
from os import path

from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
#from Amang.core.userbot import Userbot
from pyrogram import Client, filters
from pyrogram.types import Message
from Amang import core  # type: ignore
from Python_ARQ import ARQ
from telegraph import Telegraph
from config import *
from .logging import LOGGER


USERBOT_PREFIX = USERBOT_PREFIX
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID

SUDOERS = filters.user()
bot_start_time = time.time()
mongo = MongoClient(MONGO_URL)
db = mongo.AmangRobot

MOD_LOAD = []
MOD_NOLOAD = []

async def load_sudoers():
    global SUDOERS
    LOGGER(__name__).info("Loading sudoers")
    sudoersdb = db.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    for user_id in SUDO_USERS_ID:
        SUDOERS.add(user_id)
        if user_id not in sudoers:
            sudoers.append(user_id)
            await sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)


app2 = Client(
    name="userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
)

aiohttpsession = ClientSession()

arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

app = Client("Amang", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

telegraph = Telegraph()


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
