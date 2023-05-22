import os
import openai
import telebot

# Получаем токены из переменных окружения для безопасности
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Задаем токен бота и ключ API
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Задаем словарь для хранения истории чата
chat_history = {}

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    # Используем 'try-except' для обработки ошибок при взаимодействии с OpenAI
    try:
        # Если история чата для этой группы еще не начата, начинаем ее
        if message.chat.id not in chat_history:
            chat_history[message.chat.id] = [{"role": "system", "content": 'You are ChatGPT, a large language model AI.'}]
        
        # Добавляем новое сообщение в историю чата
        chat_history[message.chat.id].append({"role": "user", "content": message.text})

        # Используем 'gpt-3.5-turbo' для создания ответа, включая историю чата в качестве контекста
        model = "gpt-3.5-turbo"
        completion = openai.ChatCompletion.create(model=model, messages=chat_history[message.chat.id], max_tokens=150)

        # Проверяем наличие ожидаемого поля в ответе от OpenAI
        if 'choices' in completion and len(completion.choices) > 0 and 'message' in completion.choices[0] and 'content' in completion.choices[0]['message']:
            # Добавляем ответ бота в историю чата
            chat_history[message.chat.id].append({"role": "assistant", "content": completion.choices[0]['message']['content']})
            
            bot.reply_to(message, completion.choices[0]['message']['content'])
        else:
            bot.reply_to(message, "Sorry, I couldn't understand your message.")

    except Exception as e:
        print(f"An error occurred: {e}")




bot.polling()





