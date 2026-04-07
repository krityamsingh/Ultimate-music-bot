"""Main entry point for the Ultimate Music Bot."""

from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN
from handlers.play import play_command
from handlers.vplay import vplay_command


def main() -> None:
    """Start the bot and register command handlers."""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("play", play_command))
    app.add_handler(CommandHandler("vplay", vplay_command))

    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
