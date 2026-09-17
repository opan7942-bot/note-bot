from telegram.ext import ApplicationBuilder
import os
from dotenv import load_dotenv
from handler import command_handler
from backend.bot_database import init_db
load_dotenv()

init_db()

TOKEN = os.environ["TELEGRAM_TOKEN"]

app = ApplicationBuilder().token(TOKEN).build()




command_handler(app)


print("bot started")
app.run_polling()