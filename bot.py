import os
import telebot
import openai
from flask import Flask, request

# Telegram ва OpenAI API калитларини киритинг
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid request', 400

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Assalomu alaykum! Men nCruiseBot botiman. Savollaringizni yozing!")

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response["choices"][0]["message"]["content"])
    except Exception as e:
        bot.reply_to(message, "❌ Xatolik yuz berdi. Keyinroq urinib ko'ring.")

if __name__ == "__main__":
    print("🤖 Bot ishga tushdi!")

    # Webhook URL
    WEBHOOK_URL = f"{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/"

    # Webhook'ни ўрнатиш
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
