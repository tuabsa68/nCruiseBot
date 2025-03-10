import telebot
import os
from flask import Flask, request

# Muhit o'zgaruvchilaridan token olish
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Flask ilovasini yaratish
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return 'Unsupported Media Type', 415

# Bot komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Ассалому алайкум! Мен nCruiseBot ботиман. Саволларингизни ёзинг!")

# Matnli xabarlarni qayta ishlash
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Siz yubordingiz: {message.text}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
