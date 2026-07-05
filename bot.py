import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'مرحباً بيك في كافيه مزاج ☕\n'
        'اكتب /menu عشان تشوف المنيو\n'
        'اكتب /order عشان تطلب\n'
        'اكتب /location عشان تعرف مكانا'
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = """
    *☕ منيو كافيه مزاج ☕*
    
    *المشروبات الساخنة:*
    قهوة سادة ........ 2000 ج
    قهوة بالحليب ....... 2500 ج
    شاي لبن ........... 1500 ج
    كابتشينو .......... 3000 ج
    نسكافيه ........... 3000 ج
    
    *المشروبات الباردة:*
    عصير مانجا ........ 2500 ج
    عصير جوافة ........ 2500 ج
    موهيتو ............ 3500 ج
    ايس كوفي .......... 4000 ج
    
    *الوجبات الخفيفة:*
    سندوتش شاورما ...... 4000 ج
    بيتزا صغيرة ........ 6000 ج
    كيكة شوكولاتة ...... 2500 ج
    
    اطلب هسي بـ /order
    """
    await update.message.reply_text(menu_text, parse_mode='Markdown')

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'عشان تطلب رسل لينا:\n'
        '1. اسمك\n'
        '2. رقم تلفونك\n'
        '3. الطلب بتاعك\n'
        'مثال:\nاحمد\n0912345678\n2 قهوة + 1 شاورما'
    )

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '📍 *موقعنا:*\n'
        'امدرمان - شارع الوادي\n'
        'جنب استاد الهلال\n'
        'مواعيد العمل: 8 صباحاً - 12 مساءً'
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("order", order))
    app.add_handler 