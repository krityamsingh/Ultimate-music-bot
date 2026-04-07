"""/vplay command handler (video)."""

from telegram import Update
from telegram.ext import ContextTypes

from services.downloader import fetch_video_file
from services.youtube import find_youtube_link


async def vplay_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /vplay <query> and return a video file."""
    if not context.args:
        await update.message.reply_text("Usage: /vplay <song name>")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"🎬 Searching video for: {query}")

    youtube_url = await find_youtube_link(query)
    if not youtube_url:
        await update.message.reply_text("No matching YouTube result found.")
        return

    video_path = await fetch_video_file(youtube_url)
    if not video_path:
        await update.message.reply_text("Failed to download video.")
        return

    with open(video_path, "rb") as video:
        await update.message.reply_video(video=video, caption=query)
