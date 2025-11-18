import telebot
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

def chatgpt_reply(message):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    try:
        reply = result["choices"][0]["message"]["content"]
    except:
        reply = "❗ خطا! لطفاً دوباره امتحان کن."

    return reply


@bot.message_handler(func=lambda m: True)
def all_messages(message):
    user_text = message.text
    bot.reply_to(message, "⏳ در حال پردازش...")

    answer = chatgpt_reply(user_text)
    bot.reply_to(message, answer)


bot.infinity_polling()
