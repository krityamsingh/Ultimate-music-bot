# ============================================================
#  handlers/play.py  —  /play <song>
#
#  Flow:
#  1. "🔍 Finding music..."
#  2. yt-dlp searches YouTube (no API key)
#  3. Log to private GC  (silent, user never sees it)
#  4. "⏳ Loading track..."
#  5. pytgcalls joins VC and streams
#  6. "▶️ Now Playing" card with thumbnail
# ============================================================

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

from services.youtube import search_youtube
from services.player  import play_audio
from config import LOG_GC_ID


# ── Helpers ───────────────────────────────────────────────────

def _fmt_dur(sec: int) -> str:
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def _fmt_views(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


# ── Status card frames ────────────────────────────────────────

def _card_searching(query: str) -> str:
    return (
        "🎵  **Music Bot**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🔍  **Searching:** `{query}`\n"
        "⬜⬜⬜⬜⬜⬜⬜⬜  *Finding music...*"
    )


def _card_loading(title: str) -> str:
    return (
        "🎵  **Music Bot**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯  **Found:** {title}\n"
        "🟩🟩🟩⬜⬜⬜⬜⬜  *Loading track...*"
    )


def _card_joining() -> str:
    return (
        "🎵  **Music Bot**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🟩🟩🟩🟩🟩🟩⬜⬜  *Joining voice chat...*"
    )


def _card_now_playing(info: dict) -> str:
    dur   = _fmt_dur(info["duration"])  if info["duration"] else "Live"
    views = _fmt_views(info["views"])   if info["views"]    else "—"
    return (
        f"▶️  **Now Playing**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎼  **{info['title']}**\n"
        f"👤  {info['uploader']}\n"
        f"⏱️  `{dur}`   👁  `{views} views`\n\n"
        f"[📺 Open on YouTube]({info['webpage_url']})"
    )


# ── Handler ───────────────────────────────────────────────────

def register(bot: Client, userbot: Client):

    @bot.on_message(filters.command("play") & (filters.private | filters.group))
    async def play_handler(client: Client, message: Message):

        # Validate input
        if len(message.command) < 2:
            await message.reply(
                "🎵 **Usage:** `/play <song name or YouTube link>`\n"
                "**Example:** `/play Blinding Lights The Weeknd`"
            )
            return

        query = " ".join(message.command[1:])

        # ── Stage 1: Finding music ──────────────────────────────
        status = await message.reply(_card_searching(query), disable_web_page_preview=True)

        # ── Search YouTube (no API) ─────────────────────────────
        info = await search_youtube(query)

        if not info or not info.get("stream_url"):
            await status.edit(
                "🎵  **Music Bot**\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "❌  No results found for that song.\n"
                "Try a different name or add the artist."
            )
            return

        # ── Stage 2: Loading track ──────────────────────────────
        await status.edit(_card_loading(info["title"]))
        await asyncio.sleep(0.6)

        # ── Silent log to private GC ────────────────────────────
        try:
            requester = (
                f"@{message.from_user.username}"
                if message.from_user.username
                else message.from_user.first_name
            )
            await userbot.send_message(
                LOG_GC_ID,
                f"🎵 **Queued**\n"
                f"**Track:** {info['title']}\n"
                f"**By:** {info['uploader']}\n"
                f"**Duration:** {_fmt_dur(info['duration'])}\n"
                f"**Requested by:** {requester}\n"
                f"**Chat:** `{message.chat.id}`\n"
                f"**Link:** {info['webpage_url']}",
            )
        except Exception:
            pass  # Log GC failure must never break the user experience

        # ── Stage 3: Joining VC ─────────────────────────────────
        await status.edit(_card_joining())

        try:
            await play_audio(message.chat.id, info["stream_url"], info)
        except Exception as e:
            err = str(e).lower()
            if "no active" in err or "not found" in err or "chat_id" in err:
                tip = "Make sure there's an **active Voice Chat** in this group."
            else:
                tip = f"`{e}`"
            await status.edit(
                "🎵  **Music Bot**\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"❌  Could not join voice chat.\n{tip}"
            )
            return

        # ── Stage 4: Now Playing card ───────────────────────────
        await status.delete()

        caption = _card_now_playing(info)

        if info.get("thumbnail"):
            try:
                await bot.send_photo(
                    message.chat.id,
                    photo=info["thumbnail"],
                    caption=caption,
                )
            except Exception:
                await bot.send_message(message.chat.id, caption, disable_web_page_preview=False)
        else:
            await bot.send_message(message.chat.id, caption, disable_web_page_preview=False)
