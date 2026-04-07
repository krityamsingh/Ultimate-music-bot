# ============================================================
#  bot.py  —  Entry point
#
#  Runs TWO Pyrogram clients simultaneously:
#    • bot      → responds to users (/play, /vplay)
#    • userbot  → interacts with MegaSaverBot in the private GC
# ============================================================

import asyncio
from pyrogram import Client, idle

from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION
from handlers.play  import register_play
from handlers.vplay import register_vplay


async def main():
    # ── Bot client (uses bot token) ──
    bot = Client(
        name="music_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )

    # ── Userbot client (uses string session) ──
    userbot = Client(
        name="userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION,
    )

    # ── Register command handlers ──
    register_play(bot, userbot)
    register_vplay(bot, userbot)

    # ── Start both clients ──
    await bot.start()
    await userbot.start()

    bot_info = await bot.get_me()
    user_info = await userbot.get_me()

    print("=" * 50)
    print(f"✅ Bot started     : @{bot_info.username}")
    print(f"✅ Userbot started : @{user_info.username}")
    print("🎵 Commands ready  : /play  /vplay")
    print("=" * 50)

    await idle()

    await bot.stop()
    await userbot.stop()


if __name__ == "__main__":
    asyncio.run(main())
