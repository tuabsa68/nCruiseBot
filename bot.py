import telebot
import os
from flask import Flask, request

# Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Flask app
app = Flask(__name__)

# Home route to check if the server is live
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200

# Webhook route to receive updates
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode("UTF-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "OK", 200
    return "Invalid request", 400

# Bot start command handler
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "👋 Ассалому алайкум! Мен nCruiseBot ботиман. Саволларингизни ёзинг!")

# Echo handler for any text messages
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id, f"Siz yubordingiz: {message.text}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
