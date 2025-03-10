from flask import Flask, request
import telebot
import os

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
app = Flask(__name__)
bot = telebot.TeleBot(API_TOKEN)

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
    return 'Webhook received!', 200

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Men nCruiseBot botiman. Savollaringizni yozing!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
