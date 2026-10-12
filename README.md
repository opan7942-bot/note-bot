# note-bot

Telegram bot and Mini App for managing notes, todos, and saved secrets.

## Setup

1. Create and activate a Python virtual environment.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Keep `.env` in the project root. It must contain `TELEGRAM_TOKEN` and a private `API_SECRET_KEY`. Generate a key with `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
4. Set `MINI_APP_URL` to the public HTTPS URL for the Mini App. The app is served at `/mini-app/` by the API. `.env.example` shows the required variable names.

## Run

Open two terminals in the project root. Start the API in one terminal:

```powershell
uvicorn backend.main:app --reload
```

Start the Telegram bot in the other terminal:

```powershell
python -m bot.main_bot
```

The API initializes the SQLite tables at startup. The database file is stored at `data/note_bot.db`.
