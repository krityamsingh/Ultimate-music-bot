# ============================================================
#  start.py  —  The one file you always run
#
#  python start.py
# ============================================================

import asyncio
from pyrogram import Client, idle
from pyrogram.errors import FloodWait

from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION
import handlers
from services.player import init_player, start_player


async def safe_start(client: Client, label: str) -> None:
    """Start a Pyrogram client, respecting FloodWait instead of crashing."""
    while True:
        try:
            await client.start()
            return
        except FloodWait as e:
            print(f"[start] ⏳  Telegram flood-wait on {label}: sleeping {e.value}s …")
            await asyncio.sleep(e.value + 5)   # +5s safety margin


async def main():
    # ── Clients ──────────────────────────────────────────────
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

    # ── PyTgCalls (voice chat engine) ─────────────────────────
    init_player(userbot)

    # ── Auto-load handlers ────────────────────────────────────
    handlers.load_all(bot, userbot)

    # ── Start everything (flood-safe) ─────────────────────────
    await safe_start(bot,     "bot")
    await safe_start(userbot, "userbot")
    await start_player()          # must start AFTER userbot.start()

    bot_info  = await bot.get_me()
    user_info = await userbot.get_me()

    print()
    print("=" * 52)
    print(f"  🤖  Bot     : @{bot_info.username}")
    print(f"  👤  Userbot : @{user_info.username}")
    print("  🎵  Ready   : /play  |  /stop  |  /pause  |  /resume")
    print("=" * 52)
    print()

    await idle()

    print("\n[start] Shutting down…")
    await bot.stop()
    await userbot.stop()
    print("[start] Bye! 👋")


if __name__ == "__main__":
    asyncio.run(main())
