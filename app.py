import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from bot.handlers import start, handle_message, handle_buttons

TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

# تسجيل handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
application.add_handler(CallbackQueryHandler(handle_buttons))

# تشغيل البوت
loop = asyncio.get_event_loop()
loop.run_until_complete(application.initialize())


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"


# ✅ webhook بدون async
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    loop.run_until_complete(application.process_update(update))
    return "ok"


# ✅ endpoint لتفعيل webhook
@app.route("/setwebhook", methods=["GET"])
def set_webhook():
    loop.run_until_complete(
        application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    )
    return "Webhook set!"


# مهم لـ Vercel
handler = app
