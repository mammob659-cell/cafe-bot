import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = os.getenv("TOKEN")

# ===== ده السيرفر الوهمي عشان رندر يسكت =====
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running')

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()
# =============================================

# بنخزن سلة كل زول براهو
carts = {}

# المنيو مقسمة
MENU = {
    "مشروبات ساخنة": {
        "قهوة سادة": 2000, "قهوة تركية": 2500, "قهوة بالحليب": 2500,
        "اسبريسو": 3000, "كابتشينو": 3500, "لاتيه": 3500, "نسكافيه": 3000
    },
    "عصائر": {
        "مانجا": 2500, "جوافة": 2500, "برتقال": 2500,
        "ليمون نعناع": 2500, "موهيتو": 3500, "ايس كوفي": 4000
    },
    "وجبات": {
        "شاورما": 4000, "برجر لحم": 5000, "برجر دجاج": 5000,
        "بيتزا صغيرة": 6000, "بطاطس": 2500, "سندوتش كبدة": 3500
    },
    "حلويات": {
        "كيكة شوكولاتة": 2500, "تشيز كيك": 3500, "وافل نوتيلا": 4000, "بان كيك": 3000
    }
}

def get_main_menu():
    keyboard = []
    for category in MENU.keys():
        keyboard.append([InlineKeyboardButton(f"🍽️ {category}", callback_data=f"cat_{category}")])
    keyboard.append([InlineKeyboardButton("🛒 السلة", callback_data="cart")])
    keyboard.append([InlineKeyboardButton("📍 موقعنا", callback_data="location")])
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
            keyboard.append([InlineKeyboardButton(f"{item} - {price:,} ج", callback_data=f"add_{category}_{item}")