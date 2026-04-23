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
    return "I'm alive!"

def run():
    # Render يطلب استخدام منفذ متغير، هذا السطر يحل المشكلة
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
    await update.message.reply_text("🎂 أهلاً بك! أرسل تاريخ ميلادك (سنة/شهر/يوم).")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.replace('-', '/').replace('.', '/')
        birth_date = datetime.strptime(text, "%Y/%m/%d").date()
        day_ar = DAYS_AR.get(birth_date.strftime("%A"))
        await update.message.reply_text(f"🌟 لقد ولدت يوم: {day_ar}")
    except:
        await update.message.reply_text("❌ أرسل التاريخ بشكل صحيح: 1992/05/28")

if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    application.run_polling()
