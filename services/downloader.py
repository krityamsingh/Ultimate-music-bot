# ============================================================
#  services/downloader.py
#
#  Flow:
#  1. Userbot sends YouTube URL to PRIVATE_GC_ID
#  2. MegaSaverBot replies with an inline keyboard (Audio / Video buttons)
#  3. Userbot clicks the correct button
#  4. MegaSaverBot sends the media file
#  5. We forward that file to the requesting user via the bot
# ============================================================

import asyncio
import time
from pyrogram import Client
from pyrogram.types import Message
from config import (
    PRIVATE_GC_ID,
    MEGA_SAVER_BOT,
    WAIT_FOR_BUTTONS,
    WAIT_FOR_FILE,
)


async def fetch_media(
    userbot: Client,
    bot: Client,
    youtube_url: str,
    mode: str,           # "audio" or "video"
    target_chat_id: int, # where to forward the result
    status_msg: Message, # the "searching…" message to edit
) -> bool:
    """
    Sends the YouTube URL into the private GC, waits for MegaSaverBot
    to reply with buttons, clicks the right one, then waits for the
    media file and forwards it to target_chat_id.

    Returns True on success, False on failure.
    """

    # ── Step 1: Send the YouTube URL into the private GC via userbot ──
    sent: Message = await userbot.send_message(PRIVATE_GC_ID, youtube_url)
    sent_msg_id = sent.id

    # ── Step 2: Wait for MegaSaverBot to reply with inline buttons ──
    await status_msg.edit("⏳ **Waiting for download options…**")

    button_message: Message | None = None
    deadline = time.time() + WAIT_FOR_BUTTONS

    while time.time() < deadline:
        await asyncio.sleep(2)
        async for msg in userbot.get_chat_history(PRIVATE_GC_ID, limit=10):
            # We want a message FROM MegaSaverBot that has an inline keyboard
            if (
                msg.from_user
                and msg.from_user.username
                and msg.from_user.username.lower() == MEGA_SAVER_BOT.lower()
                and msg.reply_markup              # has inline buttons
                and msg.id > sent_msg_id          # came after our request
            ):
                button_message = msg
                break
        if button_message:
            break

    if not button_message:
        await status_msg.edit("❌ MegaSaverBot did not respond with options.")
        return False

    # ── Step 3: Click the right button ──
    #
    # MegaSaverBot typically sends buttons like:
    #   [ 🎵 Audio ]  [ 🎬 Video 480p ]
    #
    # We match the button label by the mode requested.

    target_keyword = "audio" if mode == "audio" else "480"  # 480p for video
    clicked = False

    markup = button_message.reply_markup
    if markup and hasattr(markup, "inline_keyboard"):
        for row in markup.inline_keyboard:
            for button in row:
                if target_keyword.lower() in button.text.lower():
                    await status_msg.edit(
                        f"🖱 **Clicking:** `{button.text}` …"
                    )
                    await button_message.click(button.text)
                    clicked = True
                    break
            if clicked:
                break

    if not clicked:
        await status_msg.edit("❌ Could not find the right button to click.")
        return False

    # ── Step 4: Wait for the actual media file from MegaSaverBot ──
    await status_msg.edit("📥 **Downloading… please wait.**")

    media_message: Message | None = None
    deadline = time.time() + WAIT_FOR_FILE

    while time.time() < deadline:
        await asyncio.sleep(3)
        async for msg in userbot.get_chat_history(PRIVATE_GC_ID, limit=15):
            if (
                msg.from_user
                and msg.from_user.username
                and msg.from_user.username.lower() == MEGA_SAVER_BOT.lower()
                and msg.id > button_message.id
                and (msg.audio or msg.video or msg.document)
            ):
                media_message = msg
                break
        if media_message:
            break

    if not media_message:
        await status_msg.edit("❌ Timed out waiting for the media file.")
        return False

    # ── Step 5: Forward the media to the user ──
    await status_msg.edit("📤 **Sending you the file…**")
    await userbot.forward_messages(
        chat_id=target_chat_id,
        from_chat_id=PRIVATE_GC_ID,
        message_ids=media_message.id,
    )
    await status_msg.delete()
    return True
