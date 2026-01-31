import os
import asyncio
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

print("=== BOT FILE LOADED ===")

BOT_TOKEN = os.getenv("BOT_TOKEN")
print("BOT_TOKEN:", "FOUND" if BOT_TOKEN else "MISSING")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running!")

async def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN IS MISSING")
        sys.exit(1)

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    await app.initialize()
    await app.start()

    print("🚀 BOT STARTED AND RUNNING")

    # KEEP PROCESS ALIVE
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
