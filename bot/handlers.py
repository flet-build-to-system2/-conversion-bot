from telegram import Update
from telegram.ext import ContextTypes
from utils.converters import convert_any
from utils.validators import is_valid
from utils.explanations import decimal_to_binary_steps
from bot.keyboard import base_keyboard, explain_button

user_data = {}

BASES = {
    "DEC": 10,
    "BIN": 2,
    "HEX": 16,
    "OCT": 8
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📩 أرسل رقم:", reply_markup=base_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = update.message.text
    await update.message.reply_text("اختر نوع الرقم:", reply_markup=base_keyboard())

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data in BASES:
        value = user_data.get(user_id)

        if not is_valid(value, BASES[data]):
            await query.edit_message_text("❌ رقم غير صالح لهذا النظام")
            return

        result = convert_any(value, BASES[data])

        text = "\n".join([f"{k}: {v}" for k, v in result.items()])

        context.user_data["last"] = (value, data)

        await query.edit_message_text(text, reply_markup=explain_button())

    elif data == "EXPLAIN":
        value, base = context.user_data.get("last", (None, None))

        if base == "DEC":
            steps, result = decimal_to_binary_steps(int(value))
            await query.edit_message_text(
                f"📖 خطوات التحويل:\n\n{steps}\n\nالنتيجة: {result}"
            )
        else:
            await query.edit_message_text("⚠️ الشرح متوفر حالياً فقط من DEC إلى BIN")