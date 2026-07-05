import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TOKEN")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()

# ده عشان نخزن طلب الزبون
user_orders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 شوف المنيو", callback_data='menu')],
        [InlineKeyboardButton("🛒 اطلب الان", callback_data='order')],
        [InlineKeyboardButton("📍 موقعنا", callback_data='location')]
    ]
    await update.message.reply_text(
        'مرحباً بيك في *كافيه مزاج* ☕\nاختار من تحت:',
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'menu':
        menu_text = """
☕ *منيو كافيه مزاج* ☕
*مشروبات ساخنة*
قهوة سادة - 2,000 ج
كابتشينو - 3,500 ج
*عصائر*
مانجا - 2,500 ج
موهيتو - 3,500 ج
*وجبات*
شاورما - 4,000 ج
برجر - 5,000 ج

اضغط "اطلب الان" عشان تطلب
        """
        await query.edit_message_text(menu_text, parse_mode='Markdown')

    elif query.data == 'order':
        keyboard = [
            [InlineKeyboardButton("قهوة سادة", callback_data='add_قهوة سادة')],
            [InlineKeyboardButton("كابتشينو", callback_data='add_كابتشينو')],
            [InlineKeyboardButton("شاورما", callback_data='add_شاورما')],
            [InlineKeyboardButton("برجر", callback_data='add_برجر')],
            [InlineKeyboardButton("✅ تم الطلب", callback_data='done')]
        ]
        user_orders[query.from_user.id] = []
        await query.edit_message_text('اختار من المنيو:', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith('add_'):
        item = query.data.split('_')[1]
        user_orders[query.from_user.id].append(item)
        await query.answer(f"تم اضافة {item} ✅")

    elif query.data == 'done':
        order_list = "\n".join(user_orders.get(query.from_user.id, []))
        await query.edit_message_text(f'طلبك:\n{order_list}\n\nرسل لينا رقمك عشان نتواصل معاك')
        user_orders[query.from_user.id] = []

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('📍 امدرمان - شارع الوادي جنب استاد الهلال\n⏰ من 8 صباح ل 12 مساء')

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("location", location))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()