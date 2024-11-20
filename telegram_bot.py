import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from googletrans import Translator

# إعداد سجل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# مترجم النصوص
translator = Translator()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """رسالة الترحيب عند بدء البوت"""
    await update.message.reply_text("مرحبًا! أرسل لي أي نص بالإنجليزية وسأترجمه لك للعربية.")

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ترجمة الرسائل من الإنجليزية إلى العربية"""
    input_text = update.message.text
    try:
        translated_text = translator.translate(input_text, src="en", dest="ar").text
        await update.message.reply_text(translated_text)
    except Exception as e:
        await update.message.reply_text("عذرًا، حدث خطأ أثناء الترجمة.")

def main():
    """تشغيل البوت"""
    TOKEN = "1589049533:AAHqq493CO4cBA38HLTr4liojIW1LcKJr5E"
    app = ApplicationBuilder().token(TOKEN).build()

    # إعداد الأوامر والمستمعين
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))

    # بدء التشغيل
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
