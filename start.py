# ============================================================
#  start.py  —  The one file you always run
#
#  python start.py
#
#  What it does:
#    1. Creates the bot + userbot Pyrogram clients
#    2. Calls handlers.load_all()  → auto-registers EVERY handler
#    3. Starts both clients and idles until Ctrl-C
# ============================================================

import asyncio
from pyrogram import Client, idle

from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION
import handlers  # triggers handlers/__init__.py  (the auto-loader)

async def main():
    # ── Create clients ──────────────────────────────────────
    bot = Client(
        name="music_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )

    userbot = Client(
        name="userbot_session",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION,
    )

    # ── Auto-load every handler in handlers/ ────────────────
    handlers.load_all(bot, userbot)
    
    # ── Start both clients ───────────────────────────────────
    await bot.start()
    await userbot.start()

    bot_info  = await bot.get_me()
    user_info = await userbot.get_me()

    print()
    print("=" * 52)
    print(f"  🤖  Bot     : @{bot_info.username}")
    print(f"  👤  Userbot : @{user_info.username}")
    print("  🎵  Ready   : /play  |  /vplay")
    print("=" * 52)
    print()

    # ── Keep running until Ctrl-C ────────────────────────────
    await idle()

    # ── Graceful shutdown ────────────────────────────────────
    print("\n[start] Shutting down…")
    await bot.stop()
    await userbot.stop()
    print("[start] Bye! 👋")


if __name__ == "__main__":
    asyncio.run(main())
