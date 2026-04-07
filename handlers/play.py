"""/play command handler (audio)."""

from telegram import Update
from telegram.ext import ContextTypes

from services.downloader import fetch_audio_file
from services.youtube import find_youtube_link


async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /play <query> and return an audio file."""
    if not context.args:
        await update.message.reply_text("Usage: /play <song name>")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"🔎 Searching audio for: {query}")

    youtube_url = await find_youtube_link(query)
    if not youtube_url:
        await update.message.reply_text("No matching YouTube result found.")
        return

    audio_path = await fetch_audio_file(youtube_url)
    if not audio_path:
        await update.message.reply_text("Failed to download audio.")
        return

    with open(audio_path, "rb") as audio:
        await update.message.reply_audio(audio=audio, caption=query)
