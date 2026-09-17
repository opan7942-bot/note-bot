from telegram.ext import CommandHandler
import httpx

async def start(update, context):
    await update.message.reply_text("welcome, I'm  note bot")

async def note(update, context):
    user_id = update.message.from_user.id
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/get_notes",
            params={"owner_id": user_id})
        notes_data = response.json()

        if notes_data:
            for row in notes_data:
                await update.message.reply_text(f"{row[0]}: {row[2]}")
        else:
            await update.message.reply_text("your notes are empty [:(]")


async def todo(update, context):
    user_id = update.message.from_user.id
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/get_todos",
            params={"owner_id": user_id})
        todos_data = response.json()

        if todos_data:
            for row in todos_data:
                await update.message.reply_text(f"{row[0]}: {row[2]})")
        else:
            await update.message.reply_text("you don't have any todos :( ")

async def secret(update, context):
    pass
async def mini_app(update, context):
    pass


def command_handler(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("note", note))
    app.add_handler(CommandHandler("todo",todo))
    app.add_handler(CommandHandler("secret",secret))
    app.add_handler(CommandHandler("mini_app",mini_app))
