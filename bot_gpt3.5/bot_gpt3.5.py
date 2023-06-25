import os
import openai
import telebot
import pytesseract
from PIL import Image
import io

from pydub import AudioSegment #для преобразования аудиофайлов и обнаружения тишины в них.

import speech_recognition as sr #для распознавания речи в аудиофайлах.


# Получаем токены из переменных окружения для безопасности
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Задаем токен бота и ключ API
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Инициализация Speech Recognition(аудио)
r = sr.Recognizer()

# Задаем словарь для хранения истории чата
chat_history = {}

@bot.message_handler(func=lambda m: any(word in m.text.lower() for word in ['ева','Ева', 'Привет', 'Hi', 'привет']))

def handle_message(message):
    # Используем 'try-except' для обработки ошибок при взаимодействии с OpenAI
    try:
        # Если история чата для этой группы еще не начата, начинаем ее
        if message.chat.id not in chat_history:
            chat_history[message.chat.id] = [
                {"role": "system", "content": 'You are Eva, a personal assistant.'},
                {"role": "assistant", "content": 'Привет! Меня зовут Ева, я Ваш персональный консультант.'}
            ]

        # Добавляем новое сообщение в историю чата
        chat_history[message.chat.id].append({"role": "user", "content": message.text})

        # Используем 'gpt-3.5-turbo' для создания ответа, включая историю чата в качестве контекста
        model = "gpt-3.5-turbo"
        completion = openai.ChatCompletion.create(model=model, messages=chat_history[message.chat.id], max_tokens=1000)

        # Проверяем наличие ожидаемого поля в ответе от OpenAI
        if 'choices' in completion and len(completion.choices) > 0 and 'message' in completion.choices[0] and 'content' in completion.choices[0]['message']:
            # Добавляем ответ бота в историю чата
            chat_history[message.chat.id].append({"role": "assistant", "content": completion.choices[0]['message']['content']})

            bot.reply_to(message, completion.choices[0]['message']['content'])
        else:
            bot.reply_to(message, "Sorry, I couldn't understand your message.")

    except Exception as e:
        print(f"An error occurred: {e}")

@bot.message_handler(content_types=['voice'])
def handle_audio(message):
    try:
        # Получение информации о файле от Telegram
        file_info = bot.get_file(message.voice.file_id)

        # Загрузка файла
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохранение файла
        with open('voice.ogg', 'wb') as new_file:
            new_file.write(downloaded_file)

        # Преобразование файла в формат .wav для последующего распознавания речи
        audio = AudioSegment.from_ogg('voice.ogg')
        audio.export('voice.wav', format='wav')

        # Загрузка .wav файла
        audio_file = sr.AudioFile('voice.wav')

        # Использование модуля распознавания речи для преобразования аудио в текст
        with audio_file as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='ru-RU')

        # Проверка на наличие имени 'Eva' в тексте
        if 'Eva' in text or 'Ева' in text or 'Привет' in text or 'Hi' in text:
            # Если история чата для этого пользователя еще не начата, начинаем ее
            if message.chat.id not in chat_history:
                chat_history[message.chat.id] = [
                    {"role": "system", "content": 'You are Eva, a personal assistant.'},
                    {"role": "assistant", "content": 'Привет! Меня зовут Ева, я Ваш персональный консультант.'}
                ]


            # Добавляем новое сообщение в историю чата
            chat_history[message.chat.id].append({"role": "user", "content": text})

            # Используем 'gpt-3.5-turbo' для создания ответа, включая историю чата в качестве контекста
            model = "gpt-3.5-turbo"
            completion = openai.ChatCompletion.create(model=model, messages=chat_history[message.chat.id], max_tokens=1000)

            # Проверяем наличие ожидаемого поля в ответе от OpenAI
            if 'choices' in completion and len(completion.choices) > 0 and 'message' in completion.choices[0] and 'content' in completion.choices[0]['message']:
                # Добавляем ответ бота в историю чата
                chat_history[message.chat.id].append({"role": "assistant", "content": completion.choices[0]['message']['content']})

                bot.reply_to(message, completion.choices[0]['message']['content'])
            else:
                bot.reply_to(message, "Sorry, I couldn't understand your message.")
        else:
            bot.reply_to(message, "I am Eva. Please mention my name in your audio message.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        bot.reply_to(message, "Sorry, an error occurred while processing your audio message.")


import cv2
import numpy as np

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    process_photo_message(message)
    
def process_photo_message(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        nparr = np.frombuffer(downloaded_file, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Предварительная обработка изображения
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)  # преобразование в оттенки серого
        resized = cv2.resize(gray, (800, 800))  # изменение размера изображения

        # Использование Tesseract для распознавания текста
        text = pytesseract.image_to_string(resized, lang='eng')

        # Выводим обнаруженный текст
        bot.reply_to(message, text)

    except Exception as e:
        print(f"An error occurred: {e}")
        bot.reply_to(message, "Sorry, an error occurred while processing your photo.")


bot.polling()
