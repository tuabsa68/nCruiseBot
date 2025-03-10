import os
import telebot
import openai
from flask import Flask, request

# API калитлари
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Assalomu alaykum! Men nCruiseBot botiman. Savollaringizни ёзинг!")

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Xatolik: {e}")
        bot.reply_to(message, "❌ Xatolik юз берди. Кейинроқ уриниб кўринг.")

if __name__ == "__main__":
    WEBHOOK_URL = f"{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/"
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

