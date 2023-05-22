name: Bot Telegramm gpt3.5

on: 
  push:
    branches:
      - master

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: 3.10

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install openai telebot pytelegramBotApi

    - name: Run bot
      env:  # Задаем переменные окружения, которые будут доступны во время этого шага
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        python bot_telegram/bot_ChartGPT2.py


