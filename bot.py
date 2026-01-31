import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# --------- LOGGING ---------
logging.basicConfig(level=logging.INFO)

# --------- CONFIG ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing in Railway Variables")

CHANNEL_ID = -1003208376960  # <-- PUT YOUR REAL CHANNEL ID
CHANNEL_LINK = "https://t.me/+nC_p3xBtCFgxODc9"
WEBSITE_LINK = "https://ustrade.fun/register"
SUPPORT_LINK = "https://t.me/mrnoch21"
# ---------------------------


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

    text = (
        "👋 Welcome to our Official Blockchain Project\n\n"
        "Please join our official channel to continue."
        if query.data == "lang_en"
        else
        "👋 हमारे आधिकारिक ब्लॉकचेन प्रोजेक्ट में आपका स्वागत है\n\n"
        "आगे बढ़ने के लिए कृपया चैनल जॉइन करें।"
    )

    keyboard = [
        [InlineKeyboardButton("🔒 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Verify Join", callback_data="verify")],
    ]

    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def verify_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, query.from_user.id)
        if member.status in ("member", "administrator", "creator"):
            await query.message.reply_text(
                "🎉 Verified successfully!\n\n"
                "You can now explore our platform.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK)],
                    [InlineKeyboardButton("📞 Contact Support", url=SUPPORT_LINK)],
                ])
            )
        else:
            raise Exception
    except Exception as e:
        logging.error(e)
        await query.message.reply_text(
            "❌ You have not joined the channel yet.\n"
            "Please join and click Verify again."
        )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_handler, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(verify_join, pattern="^verify$"))

    print("🤖 Bot running safely...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
