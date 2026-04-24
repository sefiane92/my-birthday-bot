import logging
from datetime import date
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "8675024471:AAH1Za4ze9Fyahs5QFrpfpGYp6_SwFPQEPE"

logging.basicConfig(level=logging.INFO)

WAITING_DATE = 1

def calculate_birthday_info(birth_date: date):
    today = date.today()

    # اليوم بالعربي
    days_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    day_name = days_ar[birth_date.weekday()]

    # العمر بالسنين
    age_years = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age_years -= 1

    # العمر بالأيام
    age_days = (today - birth_date).days

    # كم باقي لعيد الميلاد القادم
    next_birthday = date(today.year, birth_date.month, birth_date.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
    elif next_birthday == today:
        days_left = 0
    days_left = (next_birthday - today).days

    return day_name, age_years, age_days, days_left

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎂 *أهلاً بك في بوت عيد الميلاد!*\n\n"
        "أرسل لي تاريخ ميلادك بهذا الشكل:\n"
        "`YYYY-MM-DD`\n\n"
        "مثال: `1995-06-15`",
        parse_mode="Markdown"
    )
    return WAITING_DATE

async def handle_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        birth_date = date.fromisoformat(text)

        if birth_date >= date.today():
            await update.message.reply_text("❌ التاريخ يجب أن يكون في الماضي! حاول مجدداً.")
            return WAITING_DATE

        day_name, age_years, age_days, days_left = calculate_birthday_info(birth_date)

        if days_left == 0:
            birthday_msg = "🎉 *اليوم هو عيد ميلادك!* كل عام وأنت بخير! 🎂"
        elif days_left == 1:
            birthday_msg = "⏳ *باقي يوم واحد فقط* على عيد ميلادك! 🥳"
        else:
            birthday_msg = f"⏳ *باقي {days_left} يوم* على عيد ميلادك القادم 🎈"

        response = (
            f"📅 *نتائج تاريخ ميلادك:*\n\n"
            f"🗓️ وُلدت يوم: *{day_name}*\n"
            f"🎂 عمرك: *{age_years} سنة*\n"
            f"📆 عمرك بالأيام: *{age_days:,} يوم*\n\n"
            f"{birthday_msg}\n\n"
            f"_أرسل تاريخاً آخر لحسابه_"
        )

        await update.message.reply_text(response, parse_mode="Markdown")
        return WAITING_DATE

    except ValueError:
        await update.message.reply_text(
            "❌ *صيغة خاطئة!*\n\n"
            "أرسل التاريخ بهذا الشكل:\n`YYYY-MM-DD`\n\nمثال: `1995-06-15`",
            parse_mode="Markdown"
        )
        return WAITING_DATE

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={WAITING_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_date)]},
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_date))
    print("✅ البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
