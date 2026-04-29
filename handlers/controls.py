# ============================================================
#  handlers/controls.py  —  /stop  /pause  /resume  /np
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message

from services.player import stop_audio, pause_audio, resume_audio, get_now_playing


def register(bot: Client, userbot: Client):

    # ── /stop ─────────────────────────────────────────────────
    @bot.on_message(filters.command("stop") & (filters.private | filters.group))
    async def stop_handler(client: Client, message: Message):
        try:
            await stop_audio(message.chat.id)
            await message.reply(
                "⏹️  **Stopped**\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "Music stopped and left the voice chat."
            )
        except Exception:
            await message.reply("❌ No active voice chat to stop.")

    # ── /pause ────────────────────────────────────────────────
    @bot.on_message(filters.command("pause") & (filters.private | filters.group))
    async def pause_handler(client: Client, message: Message):
        try:
            await pause_audio(message.chat.id)
            await message.reply("⏸️  **Paused** — use `/resume` to continue.")
        except Exception:
            await message.reply("❌ Nothing is playing right now.")

    # ── /resume ───────────────────────────────────────────────
    @bot.on_message(filters.command("resume") & (filters.private | filters.group))
    async def resume_handler(client: Client, message: Message):
        try:
            await resume_audio(message.chat.id)
            await message.reply("▶️  **Resumed!**")
        except Exception:
            await message.reply("❌ Nothing to resume.")

    # ── /np  (now playing) ────────────────────────────────────
    @bot.on_message(filters.command("np") & (filters.private | filters.group))
    async def np_handler(client: Client, message: Message):
        info = get_now_playing(message.chat.id)
        if not info:
            await message.reply("🔇 Nothing is playing right now.")
            return

        m, s = divmod(info.get("duration", 0), 60)
        h, m = divmod(m, 60)
        dur = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

        caption = (
            f"▶️  **Now Playing**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎼  **{info['title']}**\n"
            f"👤  {info['uploader']}\n"
            f"⏱️  `{dur}`\n\n"
            f"[📺 YouTube]({info['webpage_url']})"
        )

        if info.get("thumbnail"):
            try:
                await bot.send_photo(message.chat.id, photo=info["thumbnail"], caption=caption)
                return
            except Exception:
                pass
        await message.reply(caption, disable_web_page_preview=False)
