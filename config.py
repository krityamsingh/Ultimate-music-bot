"""All credentials and constants for the bot."""

import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MEGASAVER_BOT_USERNAME = os.getenv("MEGASAVER_BOT_USERNAME", "MegaSaverBot")
DEFAULT_AUDIO_QUALITY = "128k"
DEFAULT_VIDEO_QUALITY = "720p"
