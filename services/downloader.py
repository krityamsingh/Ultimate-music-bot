# ============================================================
#  services/downloader.py
#
#  Flow:
#  1. Userbot sends YouTube URL to LOG_GC_ID
#  2. MegaSaverBot replies with inline buttons (Audio / Video)
#  3. Userbot clicks the right button
#  4. MegaSaverBot sends the media file
#  5. Userbot downloads the file to disk and returns the path
# ============================================================

import asyncio
import time
import os
from pyrogram import Client
from pyrogram.types import Message
from config import (
    LOG_GC_ID,
    MEGA_SAVER_BOT,
    WAIT_FOR_BUTTONS,
    WAIT_FOR_FILE,
)


async def fetch_and_download(
    userbot: Client,
    youtube_url: str,
    mode: str,           # "audio" or "video"
    status_msg: Message,
) -> str | None:
    """
    Sends the YouTube URL to the log GC, waits for MegaSaverBot buttons,
    clicks the right one, waits for the file, downloads it to /tmp,
    and returns the local file path. Returns None on failure.
    """

    # ── Step 1: Send URL to log GC ────────────────────────────
    sent: Message = await userbot.send_message(LOG_GC_ID, youtube_url)
    sent_msg_id = sent.id

    # ── Step 2: Wait for MegaSaverBot inline buttons ──────────
    await status_msg.edit(
        "🎵  **Music Bot**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🟩🟩🟩🟩⬜⬜⬜⬜  *Waiting for download options...*"
    )

    button_msg: Message | None = None
    deadline = time.time() + WAIT_FOR_BUTTONS

    while time.time() < deadline:
        await asyncio.sleep(2)
        async for msg in userbot.get_chat_history(LOG_GC_ID, limit=10):
            if (
                msg.from_user
                and msg.from_user.username
                and msg.from_user.username.lower() == MEGA_SAVER_BOT.lower()
                and msg.reply_markup
                and msg.id > sent_msg_id
            ):
                button_msg = msg
                break
        if button_msg:
            break

    if not button_msg:
        await status_msg.edit(
            "🎵  **Music Bot**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "❌  MegaSaverBot did not respond."
        )
        return None

    # ── Step 3: Click the right button ───────────────────────
    target_kw = "audio" if mode == "audio" else "480"
    clicked = False

    markup = button_msg.reply_markup
    if markup and hasattr(markup, "inline_keyboard"):
        for row in markup.inline_keyboard:
            for btn in row:
                if target_kw.lower() in btn.text.lower():
                    await status_msg.edit(
                        "🎵  **Music Bot**\n"
                        "━━━━━━━━━━━━━━━━━━━━\n"
                        f"🟩🟩🟩🟩🟩⬜⬜⬜  *Clicking {btn.text}...*"
                    )
                    await button_msg.click(btn.text)
                    clicked = True
                    break
            if clicked:
                break

    if not clicked:
        await status_msg.edit(
            "🎵  **Music Bot**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "❌  Could not find the download button."
        )
        return None

    # ── Step 4: Wait for the media file ──────────────────────
    await status_msg.edit(
        "🎵  **Music Bot**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🟩🟩🟩🟩🟩🟩⬜⬜  *Downloading file...*"
    )

    media_msg: Message | None = None
    deadline = time.time() + WAIT_FOR_FILE

    while time.time() < deadline:
        await asyncio.sleep(3)
        async for msg in userbot.get_chat_history(LOG_GC_ID, limit=15):
            if (
                msg.from_user
                and msg.from_user.username
                and msg.from_user.username.lower() == MEGA_SAVER_BOT.lower()
                and msg.id > button_msg.id
                and (msg.audio or msg.video or msg.document)
            ):
                media_msg = msg
                break
        if media_msg:
            break

    if not media_msg:
        await status_msg.edit(
            "🎵  **Music Bot**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "❌  Timed out waiting for the file."
        )
        return None

    # ── Step 5: Download to disk ──────────────────────────────
    await status_msg.edit(
        "🎵  **Music Bot**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🟩🟩🟩🟩🟩🟩🟩⬜  *Saving to player...*"
    )

    ext = "mp4" if mode == "video" else "mp3"
    file_path = f"/tmp/music_{media_msg.id}.{ext}"

    await userbot.download_media(media_msg, file_name=file_path)

    if not os.path.exists(file_path):
        await status_msg.edit(
            "🎵  **Music Bot**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "❌  File download failed."
        )
        return None

    return file_path


async def fetch_media(
    userbot: Client,
    bot: Client,
    youtube_url: str,
    mode: str,           # "audio" or "video"
    target_chat_id: int,
    status_msg,
) -> bool:
    """
    Fetches media via MegaSaverBot and forwards the file to target_chat_id.
    Returns True on success, False on failure.
    """
    file_path = await fetch_and_download(
        userbot=userbot,
        youtube_url=youtube_url,
        mode=mode,
        status_msg=status_msg,
    )
    if not file_path:
        return False

    try:
        await status_msg.edit("🟩🟩🟩🟩🟩🟩🟩🟩  *Sending file...*")
        if mode == "video":
            await bot.send_video(target_chat_id, file_path)
        else:
            await bot.send_audio(target_chat_id, file_path)
        await status_msg.delete()
        return True
    except Exception as e:
        await status_msg.edit(f"❌  Failed to send the file.\n`{e}`")
        return False
    finally:
        try:
            os.remove(file_path)
        except Exception:
            pass
