
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8298369135:AAFPLXLAGt5WyReC3xb-7CjUWTIK08iOGCk"
CHANNEL_USERNAME = "@YOUR_PRIVATE_CHANNEL_USERNAME"
CHANNEL_LINK = "https://t.me/+nC_p3xBtCFgxODc9"
WEBSITE_LINK = "https://ustrade.fun/register"
SUPPORT_LINK = "https://t.me/mrnoch21"

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    language TEXT
)
""")
conn.commit()

def save_user(user, language):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username, language) VALUES (?, ?, ?)",
        (user.id, user.username, language),
    )
    conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇮🇳 हिन्दी", callback_data="lang_hi")],
    ]
    await update.message.reply_text(
        "Please choose your language / कृपया भाषा चुनें",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    language = "en" if query.data == "lang_en" else "hi"
    save_user(query.from_user, language)

    text = (
        "👋 Welcome to our Official Blockchain Project\n\n"
        "To continue, please join our official community channel."
        if language == "en"
        else
        "👋 हमारे आधिकारिक ब्लॉकचेन प्रोजेक्ट में आपका स्वागत है\n\n"
        "आगे बढ़ने के लिए कृपया हमारा आधिकारिक चैनल जॉइन करें।"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("🔄 Verify Join", callback_data="verify")],
    ]

    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def verify_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["member", "administrator", "creator"]:
            keyboard = [
                [InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK)],
                [InlineKeyboardButton("📞 Contact Support", url=SUPPORT_LINK)],
            ]
            await query.message.reply_text(
                "🎉 Welcome! You are verified.",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            raise Exception()
    except:
        await query.message.reply_text("❌ Please join the channel first, then verify.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_handler, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(verify_join, pattern="^verify$"))
    app.run_polling()

if __name__ == "__main__":
    main()
