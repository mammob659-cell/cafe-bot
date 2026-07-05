import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # المنيو الكبيرة هنا
    await update.message.reply_text("المنيو...")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start() # ده البخلي رندر يسكت
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("menu", menu))
    app.run_polling()