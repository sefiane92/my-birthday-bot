import os
from flask import Flask
from threading import Thread
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, date

# --- سيرفر لإبقاء البوت حياً ---
app = Flask('')

@app.route('/')
def home():
    return "I'm alive and kicking!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# -----------------------------

TOKEN = "8761916372:AAF3_UuwNZBO88IyyELEKkLO5IERL-g-_us"

DAYS_AR = {
    "Monday": "الإثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
    "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎂 أهلاً بك! أرسل تاريخ ميلادك (سنة/شهر/يوم) لأعطيك تقريراً كاملاً.")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.replace('-', '/').replace('.', '/')
        birth_date = datetime.strptime(text, "%Y/%m/%d").date()
        today = date.today()
        
        # 1. اليوم
        day_en = birth_date.strftime("%A")
        day_ar = DAYS_AR.get(day_en, day_en)
        
        # 2. العمر
        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # 3. الأيام التي عاشها
        days_lived = (today - birth_date).days
        
        # 4. المتبقي لعيد الميلاد القادم
        next_birthday = date(today.year, birth_date.month, birth_date.day)
        if next_birthday < today:
            next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
        days_to_go = (next_birthday - today).days

        response = (
            f"📊 **تقرير ميلادك الشخصي:**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🌟 ولدت في يوم: **{day_ar}**\n"
            f"🎂 عمرك الآن: **{age_years} سنة**\n"
            f"🌍 عشت حتى الآن: **{days_lived:,} يوماً**\n"
            f"🎁 متبقي لميلادك القادم: **{days_to_go} يوماً**\n"
            f"━━━━━━━━━━━━━━━"
        )
        await update.message.reply_text(response, parse_mode="Markdown")
    except:
        await update.message.reply_text("❌ يرجى إرسال التاريخ بشكل صحيح: سنة/شهر/يوم\nمثال: 1995/10/20")

if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    application.run_polling()
