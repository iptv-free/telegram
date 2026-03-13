import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

# --- LOGGING (Bot loglarini ko'rish uchun) ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- FLASK SERVERI (Render uchun zarur) ---
app = Flask(__name__)

# --- BOT TOKENINI Olish ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN topilmadi! Render'da Environment Variables ni tekshiring.")
    raise ValueError("Missing required environment variable: BOT_TOKEN")

# --- BOT FUNKSIYALARI ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /start buyrug'i bosilganda ishlaydi """
    await update.message.reply_text('🚀 Bot ishga tushdi!\nMen Render cloud\'da ishlayapman.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Oddiy xabarlarga javob """
    await update.message.reply_text(f'Siz yozdingiz: {update.message.text}')

# --- BOTNI ISHGA TUSHIRISH FUNKSIYASI ---
def run_bot():
    try:
        logger.info("🤖 Bot ishga tushmoqda...")
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Handlerlar qo'shish
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        # Polling rejimida ishga tushirish
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Bot ishga tushmadi: {e}")

# --- WEB ROUTES (Server uyquga ketmasligi uchun) ---
@app.route("/")
def home():
    return "<h1>✅ Telegram Bot ishlamoqda!</h1>"

@app.route("/health")
def health():
    return {"status": "ok"}, 200

# --- ASOSIY DASTUR ---
if __name__ == "__main__":
    # Botni alohida thread da ishga tushiramiz
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    logger.info("🎉 Flask server boshlandi!")
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
