from telegram import Update
from telegram.ext import Application, Defaults
from telegram.constants import ParseMode
import os
from bot import edit_channel_handler, show_channels_handler, start_command

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

from dotenv import load_dotenv

load_dotenv()


def main():
    app = (
        Application.builder()
        .token(os.getenv("BOT_TOKEN"))
        .defaults(Defaults(parse_mode=ParseMode.HTML))
        .concurrent_updates(True)
        .build()
    )

    # CHANNELS SETTINGS
    app.add_handler(start_command)
    app.add_handler(show_channels_handler)
    app.add_handler(edit_channel_handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
