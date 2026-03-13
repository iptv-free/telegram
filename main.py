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

# Flask ilovasini yaratish
app = Flask(__name__)

# Bot tokenini muhit o'zgaruvchisidan olish
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Iltimos, Render'da Environment Variables ni tekshiring.")

# --- Bot funksiyalari ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Salom! Men Render cloud\'da ishlayapman 🚀')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Siz yozdingiz: {update.message.text}')

def run_bot():
    logging.info("Bot ishga tushmoqda...")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# --- Flask serveri ---
@app.route("/")
def home():
    return "Telegram Bot ishlamoqda ✅"

@app.route("/health")
def health():
    return "Alive", 200

# --- Asosiy dastur ---
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True  # Asosiy dastur tugagach botni ham o'chirish uchun
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
