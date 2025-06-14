import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

# --- Ρυθμίσεις ---
MASTER_USER_ID = int(os.getenv("MASTER_USER_ID"))
COPY_USERS = list(map(int, os.getenv("COPY_USERS", "").split(",")))
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Συνάρτηση για εκτέλεση copy trade (μόνο ειδοποίηση, όχι ακόμα API execution)
async def copy_trade(trade_text):
    for user_id in COPY_USERS:
        try:
            await app.bot.send_message(chat_id=user_id, text=f"📥 Copy Trade Signal:\n{trade_text}")
        except Exception as e:
            print(f"❌ Error sending to {user_id}: {e}")

# Όταν ο Master Trader στέλνει μήνυμα στο group
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    if user_id == MASTER_USER_ID:
        await update.message.reply_text("✅ Trade received. Copying to users...")
        await copy_trade(message)

# Εκκίνηση bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 CopyTrade Bot activated!")

# Ρύθμιση bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ CopyTrade Bot is running...")
app.run_polling()
