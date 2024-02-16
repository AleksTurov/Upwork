import os
import openai
import telebot
from pydub import AudioSegment
import speech_recognition as sr
from tempfile import NamedTemporaryFile

# Получение токенов из переменных окружения
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
    """Генерация ответа с использованием модели GPT от OpenAI."""
    if chat_id not in chat_history:
        chat_history[chat_id] = [
            {"role": "system", "content": "You are Eva, a personal assistant."},
            {"role": "assistant", "content": "Hello! I'm Eva, your personal assistant."},
            {"role": "assistant", "content": 'Привет! Меня зовут Ева, я Ваш персональный консультант.'}
        ]

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
    """Обработка текстовых и голосовых сообщений."""
    try:
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
        else:
            return  # Пропускаем обработку, если сообщение не текст и не голос

        response = generate_openai_response(message.chat.id, text)
        bot.reply_to(message, response)
        
    try:
        print("Обработка сообщения:", message.text)
        # Ваш код обработки сообщения здесь
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        bot.reply_to(message, "Извините, произошла ошибка при обработке вашего сообщения.")

# Запуск бота
bot.polling(non_stop=True)

