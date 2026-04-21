import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, date

# التوكن الخاص بك
TOKEN = "8761916372:AAF3_UuwNZBO88IyyELEKkLO5IERL-g-_us"

# إعداد السجلات لمراقبة أداء البوت على السيرفر
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

DAYS_AR = {
    "Monday": "الإثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
    "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"أهلاً بك يا {user_name} في بوت ميلادك! 🎂\n\n"
        "أرسل تاريخ ميلادك (سنة/شهر/يوم) لأعطيك تقريراً كاملاً.\n"
        "مثال: 1992/05/28"
    )

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        # معالجة التاريخ
        birth_date = datetime.strptime(text.replace('-', '/').replace('.', '/'), "%Y/%m/%d").date()
        today = date.today()
        
        # 1. معرفة اليوم
        day_en = birth_date.strftime("%A")
        day_ar = DAYS_AR.get(day_en, day_en)
        
        # 2. حساب العمر
        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # 3. حساب الأيام التي عاشها
        days_lived = (today - birth_date).days
        
        # 4. الأيام المتبقية لعيد الميلاد القادم
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
    except Exception:
        await update.message.reply_text("❌ يرجى إرسال التاريخ بشكل صحيح: سنة/شهر/يوم\nمثال: 1998/12/30")

if __name__ == '__main__':
    # بناء وتشغيل البوت
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    
    application.run_polling()
