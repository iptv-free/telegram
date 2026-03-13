import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Flask ilovasini yaratish (Render uxlab qolmasligi uchun)
app = Flask(__name__)

# Bot tokenini muhit o'zgaruvchisidan olish
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Iltimos, Render'da Environment Variables ni tekshiring.")

# --- Bot funksiyalari ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start buyrug'i bosilganda ishlaydi"""
    await update.message.reply_text('Salom! Men Render cloud\'da ishlayapman 🚀\nNima yozsangiz, shuni qaytaraman.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Oddiy xabarlarga javob"""
    await update.message.reply_text(f'Siz yozdingiz: {update.message.text}')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xatoliklar haqida xabar"""
    logging.error(f"Update {update} caused error {context.error}")

# --- Botni ishga tushirish funksiyasi ---
def run_bot():
    logging.info("Bot ishga tushmoqda...")
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Buyruqlar
    application.add_handler(CommandHandler("start", start))
    # Oddiy xabarlar
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Xatoliklar
    application.add_error_handler(error_handler)
    
    # Polling rejimida ishga tushirish
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# --- Flask serveri (Webhook emas, lekin serverni tirik tutadi) ---
@app.route("/")
def home():
    return "Telegram Bot ishlamoqda ✅ | Status: OK"

@app.route("/health")
def health():
    return "Alive", 200

# --- Asosiy dastur ---
if __name__ == "__main__":
    # Botni alohida oqimda (thread) ishga tushiramiz
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Flask serverini ishga tushiramiz (Render talabi)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
