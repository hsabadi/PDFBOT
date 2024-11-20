import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
from PyPDF2 import PdfReader

# إعداد OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"

# دالة لتحليل النص وتلخيصه باستخدام OpenAI
def summarize_and_generate_quiz(text):
    try:
        # تلخيص النص
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes and generates quiz questions."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
            ]
        )
        summary = response["choices"][0]["message"]["content"]
        
        # إنشاء أسئلة Quiz بناءً على النص الملخص
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that creates quiz questions."},
                {"role": "user", "content": f"Based on this summary, create 5 quiz questions:\n\n{summary}"}
            ]
        )
        quiz = response["choices"][0]["message"]["content"]
        
        return summary, quiz
    except Exception as e:
        return f"Error: {str(e)}", ""

# دالة لاستلام الملفات
def handle_document(update: Update, context: CallbackContext):
    file = update.message.document
    file_path = f"./{file.file_name}"
    file.get_file().download(file_path)

    try:
        # قراءة الملف إذا كان PDF
        if file.file_name.endswith('.pdf'):
            reader = PdfReader(file_path)
            text = "".join(page.extract_text() for page in reader.pages)
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        # تلخيص النص وإنشاء الأسئلة
        summary, quiz = summarize_and_generate_quiz(text)

        # إرسال النتيجة إلى المستخدم
        update.message.reply_text(f"**Summary:**\n{summary}\n\n**Quiz Questions:**\n{quiz}", parse_mode="Markdown")
    except Exception as e:
        update.message.reply_text(f"Error processing the file: {str(e)}")
    finally:
        os.remove(file_path)

# دالة البدء
def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحبًا! أرسل لي ملف محاضرة (PDF أو نصي) وسأقوم بتلخيصه وإنشاء أسئلة Quiz.")

# إعداد البوت
def main():
    TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # أوامر البوت
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

    # تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
