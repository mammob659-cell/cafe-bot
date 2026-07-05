import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN not found! Please set TOKEN in Environment Variables")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('مرحباً بيك في كافيه مزاج ☕\nاكتب /menu')

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = "*☕ منيو كافيه مزاج ☕*\n\nقهوة ........ 2000 ج\nشاي ........ 1500 ج"
    await update.message.reply_text(menu_text, parse_mode='Markdown')

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    print("Bot is running...")
    app.run_polling()