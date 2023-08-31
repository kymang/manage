
from os import getenv
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = getenv("BOT_TOKEN")
SUPPORT = getenv("SUPPORT", "")
API_ID = int(getenv("API_ID") or 0)
OWNER_ID = int(getenv("OWNER_ID") or 0)
SESSION = getenv("SESSION", "")
OPENAI_API = getenv("OPENAI_API", "")
API_HASH = getenv("API_HASH")
USERBOT_PREFIX = getenv("USERBOT_PREFIX", "!")
SUDO_USERS_ID = list(map(int, getenv("SUDO_USERS_ID", "").split()))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID") or 0)
WELCOME_DELAY_KICK_SEC = int(getenv("WELCOME_DELAY_KICK_SEC", "600"))
MONGO_URL = getenv("MONGO_URL")
ARQ_API_KEY = getenv("ARQ_API_KEY")
ARQ_API_URL = getenv("ARQ_API_URL", "https://arq.hamker.in")
LOG_MENTIONS = getenv("LOG_MENTIONS", "False").lower() in ["true", "1"]
RSS_DELAY = int(getenv("RSS_DELAY", "300"))
PM_PERMIT = getenv("PM_PERMIT", "False").lower() in ["true", "1"]
