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

@app.route("/", methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "OK", 200
    else:
        return "Bot is running!", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Assalomu alaykum! Men nCruiseBot botiman. Sizga InCruises haqida yordam bera olaman. Savollaringizni yozing!")

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response["choices"][0]["message"]["content"])
    except Exception as e:
        bot.reply_to(message, "❌ Xatolik yuz berdi. Keyinroq urinib ko'ring.")

if __name__ == "__main__":
    WEBHOOK_URL = f"https://myincruisebot.onrender.com/"
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
