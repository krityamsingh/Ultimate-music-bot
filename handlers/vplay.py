# ============================================================
#  handlers/vplay.py  —  /vplay <song name>  →  sends VIDEO (480p)
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message

from services.youtube import get_youtube_link
from services.downloader import fetch_media


def register_vplay(bot: Client, userbot: Client):
    """Register the /vplay command on the bot client."""

    @bot.on_message(filters.command("vplay") & (filters.private | filters.group))
    async def vplay_handler(client: Client, message: Message):
        # ── Validate input ──
        if len(message.command) < 2:
            await message.reply(
                "🎬 Usage: `/vplay <song name>`\n"
                "Example: `/vplay Shape of You Ed Sheeran`"
            )
            return

        query = " ".join(message.command[1:])
        status = await message.reply(f"🔍 **Searching for:** `{query}` …")

        # ── Find YouTube URL via Gemini ──
        url = await get_youtube_link(query)
        if not url:
            await status.edit("❌ Could not find a YouTube link for that song.")
            return

        await status.edit(f"🎯 **Found:** `{url}`\n⚙️ Processing video (480p)…")

        # ── Fetch & deliver ──
        success = await fetch_media(
            userbot=userbot,
            bot=bot,
            youtube_url=url,
            mode="video",
            target_chat_id=message.chat.id,
            status_msg=status,
        )

        if not success:
            pass
