import os
import openai

import telebot
from pydub import AudioSegment
import speech_recognition as sr
from tempfile import NamedTemporaryFile

# Получение токенов из переменных окружения для безопасности
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Инициализация бота и OpenAI
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Инициализация распознавания речи
recognizer = sr.Recognizer()

# Словарь для хранения истории чата
chat_history = {}


def generate_openai_response(chat_id, text):
    """
    Генерация ответа с использованием модели GPT от OpenAI.
    """
    if chat_id not in chat_history:
        chat_history[chat_id] = []

    chat_history[chat_id].append({"role": "user", "content": text})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Используйте актуальную модель
        messages=chat_history[chat_id],
        max_tokens=1000
    )

    if response.choices and response.choices[0].message.content:
        chat_history[chat_id].append({"role": "assistant", "content": response.choices[0].message.content})
        return response.choices[0].message.content
    else:
        return "Извините, я не смог понять ваше сообщение."

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """
    Обработка текстовых и голосовых сообщений.
    Бот отвечает только если сообщение содержит 'Привет', 'hi', 'Ева' или 'eva'.
    """
    try:
        text = ''
        if message.content_type == 'text':
            text = message.text
        elif message.content_type == 'voice':
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with NamedTemporaryFile(suffix='.ogg') as ogg_file:
                ogg_file.write(downloaded_file)
                ogg_file.flush()
                audio = AudioSegment.from_ogg(ogg_file.name)
                
                with NamedTemporaryFile(suffix='.wav') as wav_file:
                    audio.export(wav_file.name, format='wav')
                    with sr.AudioFile(wav_file.name) as source:
                        audio_data = recognizer.record(source)
                        text = recognizer.recognize_google(audio_data, language='ru-RU')

        # Проверка наличия ключевых слов для активации бота
        if any(keyword in text.lower() for keyword in ['привет', 'hi', 'ева', 'eva', 'Eva', 'Ева']):
            response = generate_openai_response(message.chat.id, text)
            bot.reply_to(message, response)
        else:
            # Бот не отвечает, если ключевые слова отсутствуют
            print("Сообщение не содержит ключевых слов для активации бота.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        # Теперь добавим логирование стека вызовов, чтобы получить более подробную информацию
        import traceback
        traceback.print_exc()  # Это выведет полный стек вызовов исключения в консоль
        bot.reply_to(message, "Извините, произошла ошибка при обработке вашего сообщения.")


# Запуск бота в режиме опроса с бесконечным циклом
bot.polling(non_stop=True)
