# 🤖 Telegram Business AI Assistant Bot

Professional Telegram Business AI Assistant built with **aiogram 3.x**, **FastAPI**, **SQLAlchemy**, **Redis** and **Groq AI**.

## ✨ Features

- 🏢 **Telegram Business** integration (processes business messages)
- 🧠 **AI** powered by Groq (Llama 3.3 70B, configurable model)
- 🌍 **Multilingual** — auto-detects Uzbek, Russian, English
- 💬 **Per-user chat history** with context window
- 🎛️ **Admin dashboard** (35+ commands, inline keyboard, pagination)
- 🔒 **Security** — rate limit, flood control, black/white list, spam filter
- 💾 **Backups** — export / import / restore database
- 🐳 **Docker** — production ready
- 📦 **Modular** architecture, PEP 8, type hints, async

## 📂 Structure

```
app/
 ├── handlers/        # aiogram routers
 ├── middlewares/     # auth, throttle, logging
 ├── filters/         # custom filters (admin, blocked, …)
 ├── database/        # engine & session
 ├── models/          # SQLAlchemy ORM
 ├── services/        # business logic
 ├── ai/              # Groq client & prompt builder
 ├── keyboards/       # inline / reply keyboards
 ├── utils/           # helpers, logger, exporters
 ├── config.py        # settings
 ├── main.py          # entry point
 └── requirements.txt
```

## 🚀 Quick start

```bash
# 1. Clone
git clone https://github.com/KRYZENSYS/tg-business-ai-bot.git
cd tg-business-ai-bot

# 2. Copy env
cp .env.example .env
# edit .env (BOT_TOKEN, ADMIN_ID, GROQ_API_KEY)

# 3. Docker
docker compose up -d

# OR local
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## 📜 License

MIT © 2026 KRYZENSYS
