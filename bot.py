import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
...
def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start() # السطر ده مهم
    app.run_polling()import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

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

# بنخزن سلة كل زول براهو
carts = {}

# المنيو مقسمة
MENU = {
    "مشروبات ساخنة": {
        "قهوة سادة": 2000, "قهوة تركية": 2500, "كابتشينو": 3500, "لاتيه": 3500
    },
    "عصائر": {
        "مانجا": 2500, "جوافة": 2500, "موهيتو": 3500, "ايس كوفي": 4000
    },
    "وجبات": {
        "شاورما": 4000, "برجر لحم": 5000, "برجر دجاج": 5000, "بيتزا": 6000, "بطاطس": 2500
    },
    "حلويات": {
        "كيكة شوكولاتة": 2500, "تشيز كيك": 3500, "وافل": 4000
    }
}

def get_main_menu():
    keyboard = []
    for category in MENU.keys():
        keyboard.append([InlineKeyboardButton(f"🍽️ {category}", callback_data=f"cat_{category}")])
    keyboard.append([InlineKeyboardButton("🛒 السلة", callback_data="cart")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    carts[update.effective_user.id] = {}
    await update.message.reply_text(
        'مرحباً بيك في *كافيه مزاج* ☕\nاختار القسم العايزو:',
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data.startswith("cat_"):
        category = query.data.split("_", 1)[1]
        keyboard = []
        for item, price in MENU[category].items():
            keyboard.append([InlineKeyboardButton(f"{item} - {price:,} ج", callback_data=f"add_{category}_{item}")])
        keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="back")])
        await query.edit_message_text(f"*{category}*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data.startswith("add_"):
        _, category, item = query.data.split("_", 2)
        if user_id not in carts: carts[user_id] = {}
        carts[user_id][item] = carts[user_id].get(item, 0) + 1
        await query.answer(f"تم اضافة {item} للسلة ✅")

    elif query.data == "cart":
        if not carts.get(user_id):
            await query.edit_message_text("السلة فاضية 😅", reply_markup=get_main_menu())
            return
        text = "*سلة الطلبات:*\n"
        total = 0
        for item, qty in carts[user_id].items():
            price = next((p for cat in MENU.values() for i,p in cat.items() if i==item), 0)
            text += f"- {item} x{qty} = {price*qty:,} ج\n"
            total += price*qty
        text += f"\n*الاجمالي: {total:,} ج*"
        keyboard = [[InlineKeyboardButton("✅ تأكيد الطلب", callback_data="checkout")], [InlineKeyboardButton("⬅️ رجوع", callback_data="back")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == "checkout":
        await query.edit_message_text("تمام 👌 رسل لينا:\nالاسم\nرقم التلفون\nالعنوان\nوح نتصل عليك نأكد الطلب")
        carts[user_id] = {}

    elif query.data == "back":
        await query.edit_message_text('اختار القسم العايزو:', reply_markup=get_main_menu())

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()