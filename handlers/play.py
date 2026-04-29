# ============================================================
#  handlers/play.py  —  /play <song>
#  Flow: yt-dlp search → stream URL → play in VC
# ============================================================

import asyncio, os
from pyrogram import Client, filters
from pyrogram.types import Message
from services.youtube import search_youtube
from services.player import play_audio


def _fmt_dur(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def register(bot: Client, userbot: Client):

    @bot.on_message(filters.command("play") & (filters.private | filters.group))
    async def play_handler(client: Client, message: Message):
        if len(message.command) < 2:
            await message.reply("🎵 **Usage:** `/play <song name>`")
            return

        query = " ".join(message.command[1:])
        status = await message.reply(
            "🎵  **Music Bot**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🔍  **Searching:** `{query}`\n"
            "⬜⬜⬜⬜⬜⬜⬜⬜  *Finding music...*"
        )

        # ── Search YouTube ──────────────────────────────────────
        info = await search_youtube(query)
        if not info:
            await status.edit(
                "🎵  **Music Bot**\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "❌  No results found. Try a different name."
            )
            return

        await status.edit(
            "🎵  **Music Bot**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯  **Found:** {info['title']}\n"
            "🟩🟩🟩🟩🟩🟩🟩⬜  *Joining voice chat...*"
        )

        # ── Play in VC via stream URL ───────────────────────────
        try:
            await play_audio(message.chat.id, info["stream_url"], info)
        except Exception as e:
            await status.edit(
                "🎵  **Music Bot**\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "❌  Could not join voice chat.\n"
                "Make sure there is an **active Voice Chat** in this group.\n"
                f"`{e}`"
            )
            return

        # ── Now Playing card ────────────────────────────────────
        await status.delete()
        caption = (
            f"▶️  **Now Playing**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎼  **{info['title']}**\n"
            f"👤  {info['uploader']}\n"
            f"⏱️  `{_fmt_dur(info['duration'])}`\n\n"
            f"[📺 YouTube]({info['webpage_url']})"
        )

        if info.get("thumbnail"):
            try:
                await bot.send_photo(message.chat.id, photo=info["thumbnail"], caption=caption)
                return
            except Exception:
                pass
        await bot.send_message(message.chat.id, caption, disable_web_page_preview=False)
