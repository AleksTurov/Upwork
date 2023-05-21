import os
import openai
import telebot

# Получаем токены из переменных окружения для безопасности
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Задаем токен бота и ключ API
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Задаем идентификатор группы
group_id = -1001647255083  # replace with your group chat ID

@bot.message_handler(func=lambda _: True)
def handle_message(message):
    # Используем 'try-except' для обработки ошибок при взаимодействии с OpenAI
    try:
        engine = "text-davinci-003"
        prompt = message.text
        completion = openai.Completion.create(engine=engine, prompt=prompt, temperature=0.5, max_tokens=4000)

        # Проверяем наличие ожидаемого поля в ответе от OpenAI
        if 'choices' in completion and len(completion.choices) > 0 and 'text' in completion.choices[0]:
            bot.send_message(chat_id=group_id, text=completion.choices[0]['text'])
        else:
            bot.send_message(chat_id=group_id, text="Sorry, I couldn't understand your message.")

    except Exception as e:
        print(f"An error occurred: {e}")

bot.polling()



































































