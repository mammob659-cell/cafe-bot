import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'مرحباً بيك في *كافيه مزاج* ☕\n\n'
        '/menu  - تشوف المنيو كامل\n'
        '/order - تطلب طلبك\n'
        '/location - موقعنا ومواعيدنا',
        parse_mode='Markdown'
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = """
☕ *منيو كافيه مزاج - امدرمان* ☕

*1. القهوة والمشروبات الساخنة*
قهوة سادة ................. 2,000 ج
قهوة تركية ................ 2,500 ج
قهوة بالحليب .............. 2,500 ج
اسبريسو ................... 3,000 ج
كابتشينو .................. 3,500 ج
لاتيه ..................... 3,500 ج
نسكافيه ................... 3,000 ج
شاي سادة .................. 1,000 ج
شاي لبن ................... 1,500 ج
شاي بالنعناع .............. 1,500 ج
زنجبيل بالليمون ........... 2,000 ج

*2. العصائر الفريش*
عصير مانجا ................ 2,500 ج
عصير جوافة ................ 2,500 ج
عصير برتقال ............... 2,500 ج
عصير ليمون بالنعناع ....... 2,500 ج
عصير قنقليز ................ 2,000 ج
سموثي فراولة .............. 3,500 ج

*3. المشروبات الباردة*
موهيتو .................... 3,500 ج
ايس كوفي .................. 4,000 ج
ايس لاتيه ................. 4,000 ج
ميلك شيك شوكولاتة ......... 4,500 ج
ميلك شيك فراولة ........... 4,500 ج
بيبسي / ميرندا ............ 1,500 ج
موية صحة .................. 1,000 ج

*4. الوجبات الخفيفة*
سندوتش شاورما ............. 4,000 ج
سندوتش كبدة ............... 3,500 ج
سندوتش جبنة ................ 2,500 ج
برجر لحم .................. 5,000 ج
برجر دجاج ................. 5,000 ج
بيتزا صغيرة ................ 6,000 ج
بطاطس مقلية ................ 2,500 ج

*5. الحلويات*
كيكة شوكولاتة ............. 2,500 ج
تشيز كيك .................. 3,500 ج
وافل بالنوتيلا ............ 4,000 ج
بان كيك ................... 3,000 ج

*للطلب اكتب /order*
    """
    await update.message.reply_text(menu_text, parse_mode='Markdown')

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('رسل لينا:\nالاسم\nرقم التلفون\nالطلب\n\nمثال:\nاحمد\n0912xxxxxx\n2 قهوة + 1 برجر')

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('📍 امدرمان - شارع الوادي جنب استاد الهلال\n⏰ من 8 صباح ل 12 مساء')

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("order", order))
    app.add_handler(CommandHandler("location", location))
    print("Bot is running...")
    app.run_polling()