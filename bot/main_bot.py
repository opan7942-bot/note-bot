import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from backend.bot_database import init_db
from bot.handler import command_handler


def main():
    load_dotenv()
    init_db()

    token = os.environ["TELEGRAM_TOKEN"]
    app = ApplicationBuilder().token(token).build()
    command_handler(app)

    print("bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
