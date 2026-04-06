import os
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


# ⚠️ مهم: تشغيل البوت داخل event loop
import asyncio
asyncio.get_event_loop().run_until_complete(application.initialize())


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"


@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"


# ❌ حذف before_first_request
# ✅ بدله بهذا endpoint لتفعيل webhook يدوياً
@app.route("/setwebhook", methods=["GET"])
async def set_webhook():
    await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    return "Webhook set!"


# ❗ مهم لـ Vercel
handler = app
