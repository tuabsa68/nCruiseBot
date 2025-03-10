import os
import telebot
import openai
from flask import Flask, request

# Telegram ва OpenAI API калитларини киритинг
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "\U0001F44B Assalomu alaykum! Men nCruiseBot botiman. Sizga InCruises haqida yordam bera olaman. Savollaringizni yozing!")

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response["choices"][0]["message"]["content"])
    except Exception as e:
        bot.reply_to(message, "\u274C Xatolik yuz berdi. Keyinroq urinib ko'ring.")

app = Flask(__name__)

if __name__ == "__main__":
    print("\U0001F916 Bot ишга тушди!")

    # Webhook'ни ўрнатиш
    WEBHOOK_URL = f"{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/"
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    bot.polling(none_stop=True)
