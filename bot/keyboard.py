from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def base_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("DEC", callback_data="DEC"),
            InlineKeyboardButton("BIN", callback_data="BIN"),
            InlineKeyboardButton("HEX", callback_data="HEX"),
            InlineKeyboardButton("OCT", callback_data="OCT"),
        ]
    ])

def explain_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 شرح الطريقة", callback_data="EXPLAIN")]
    ])