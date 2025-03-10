import telebot
import os
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Ботга хабар юборилганда ушбу функция ишга тушади
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, f"Siz yozdingiz: {message.text}")

# Webhook учун маршрут
@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

# Webhookни ўрнатиш учун маршрут
@app.route("/", methods=["GET", "POST"])
def webhook():
    bot.remove_webhook()
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    bot.set_webhook(url=webhook_url)
    return "Webhook o'rnatildi!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
