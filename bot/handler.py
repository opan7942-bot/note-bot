import os

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, filters
import httpx


API_URL = "http://127.0.0.1:8000"
MENU_OPTIONS = {
    "📝 Notes": "notes",
    "✅ To-do": "todos",
    "🔐 Secrets": "secrets",
    "📱 Mini App": "mini_app",
}


def _api_headers(owner_id):
    return {
        "X-API-Key": os.environ["API_SECRET_KEY"],
        "X-Owner-ID": str(owner_id),
    }


def _menu_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton(label)] for label in MENU_OPTIONS],
        resize_keyboard=True,
        is_persistent=True,
    )


async def start(update, context):
    await update.message.reply_text(
        "Choose an option:", reply_markup=_menu_keyboard()
    )


async def note(update, context):
    user_id = update.effective_user.id
    async with httpx.AsyncClient(headers=_api_headers(user_id)) as client:
        response = await client.get(
            f"{API_URL}/get_notes", params={"owner_id": user_id}
        )
        response.raise_for_status()
        notes_data = response.json()

    if notes_data:
        for row in notes_data:
            await update.effective_message.reply_text(f"{row[0]}: {row[2]}")
    else:
        await update.effective_message.reply_text("Your notes are empty.")


async def todo(update, context):
    user_id = update.effective_user.id
    async with httpx.AsyncClient(headers=_api_headers(user_id)) as client:
        response = await client.get(
            f"{API_URL}/get_todos", params={"owner_id": user_id}
        )
        response.raise_for_status()
        todos_data = response.json()

    if not todos_data:
        await update.effective_message.reply_text("You don't have any todos.")
        return

    for row in todos_data:
        todo_id, _, task, status = row
        checkbox = "☑" if status else "☐"
        keyboard = None
        if not status:
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    f"☐ {task}", callback_data=f"complete_todo:{todo_id}"
                )
            ]])
        else:
            await update.effective_message.reply_text(f"☑ {task}")
            continue
        await update.effective_message.reply_text(
            f"{checkbox} {task}", reply_markup=keyboard
        )


async def secret(update, context):
    user_id = update.effective_user.id
    async with httpx.AsyncClient(headers=_api_headers(user_id)) as client:
        response = await client.get(
            f"{API_URL}/get_secrets", params={"owner_id": user_id}
        )
        response.raise_for_status()
        secrets_data = response.json()

    if secrets_data:
        for row in secrets_data:
            await update.effective_message.reply_text(f"{row[2]}: {row[3]}")
    else:
        await update.effective_message.reply_text("You don't have any secrets.")


async def mini_app(update, context):
    mini_app_url = os.getenv("MINI_APP_URL")
    if not mini_app_url or not mini_app_url.startswith("https://"):
        await update.effective_message.reply_text(
            "Mini App needs a public HTTPS URL. Set MINI_APP_URL in the project .env file."
        )
        return

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Open Mini App", web_app=WebAppInfo(url=mini_app_url))
    ]])
    await update.effective_message.reply_text(
        "Open your notes, tasks, and secrets:", reply_markup=keyboard
    )


async def complete_todo(update, context):
    query = update.callback_query
    await query.answer()
    todo_id = int(query.data.split(":", 1)[1])
    async with httpx.AsyncClient(headers=_api_headers(query.from_user.id)) as client:
        response = await client.post(
            f"{API_URL}/complete_todo",
            params={"owner_id": query.from_user.id, "todo_id": todo_id},
        )
        response.raise_for_status()
    task_text = query.message.reply_markup.inline_keyboard[0][0].text[2:]
    await query.edit_message_text(f"☑ {task_text}")


async def menu_selection(update, context):
    option = MENU_OPTIONS.get(update.effective_message.text)
    if option == "notes":
        await note(update, context)
    elif option == "todos":
        await todo(update, context)
    elif option == "secrets":
        await secret(update, context)
    elif option == "mini_app":
        await mini_app(update, context)


def command_handler(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("note", note))
    app.add_handler(CommandHandler("todo", todo))
    app.add_handler(CommandHandler("secret", secret))
    app.add_handler(CommandHandler("mini_app", mini_app))
    app.add_handler(CallbackQueryHandler(complete_todo, pattern=r"^complete_todo:\d+$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_selection))
