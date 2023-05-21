{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "5215ae1b-fc95-4529-b4d8-152c82c65471",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import openai\n",
    "import telebot\n",
    "\n",
    "# Получаем токены из переменных окружения для безопасности\n",
    "TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')\n",
    "OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')\n",
    "\n",
    "# Задаем токен бота и ключ API\n",
    "bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)\n",
    "openai.api_key = OPENAI_API_KEY\n",
    "\n",
    "# Задаем идентификатор группы\n",
    "group_id = -1001647255083  # replace with your group chat ID\n",
    "\n",
    "@bot.message_handler(func=lambda _: True)\n",
    "def handle_message(message):\n",
    "    # Используем 'try-except' для обработки ошибок при взаимодействии с OpenAI\n",
    "    try:\n",
    "        engine = \"text-davinci-003\"\n",
    "        prompt = message.text\n",
    "        completion = openai.Completion.create(engine=engine, prompt=prompt, temperature=0.5, max_tokens=4000)\n",
    "\n",
    "        # Проверяем наличие ожидаемого поля в ответе от OpenAI\n",
    "        if 'choices' in completion and len(completion.choices) > 0 and 'text' in completion.choices[0]:\n",
    "            bot.send_message(chat_id=group_id, text=completion.choices[0]['text'])\n",
    "        else:\n",
    "            bot.send_message(chat_id=group_id, text=\"Sorry, I couldn't understand your message.\")\n",
    "\n",
    "    except Exception as e:\n",
    "        print(f\"An error occurred: {e}\")\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "c2f9ee26-45e4-461f-b61a-940e678835dd",
   "metadata": {},
   "outputs": [
    {
     "ename": "Exception",
     "evalue": "Bot token is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mException\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[6], line 1\u001b[0m\n\u001b[0;32m----> 1\u001b[0m bot\u001b[39m.\u001b[39;49mpolling()\n",
      "File \u001b[0;32m~/anaconda3/lib/python3.10/site-packages/telebot/__init__.py:1040\u001b[0m, in \u001b[0;36mTeleBot.polling\u001b[0;34m(self, non_stop, skip_pending, interval, timeout, long_polling_timeout, logger_level, allowed_updates, none_stop, restart_on_change, path_to_watch)\u001b[0m\n\u001b[1;32m   1037\u001b[0m \u001b[39mif\u001b[39;00m restart_on_change:\n\u001b[1;32m   1038\u001b[0m     \u001b[39mself\u001b[39m\u001b[39m.\u001b[39m_setup_change_detector(path_to_watch)\n\u001b[0;32m-> 1040\u001b[0m logger\u001b[39m.\u001b[39minfo(\u001b[39m'\u001b[39m\u001b[39mStarting your bot with username: [@\u001b[39m\u001b[39m%s\u001b[39;00m\u001b[39m]\u001b[39m\u001b[39m'\u001b[39m, \u001b[39mself\u001b[39;49m\u001b[39m.\u001b[39;49muser\u001b[39m.\u001b[39musername)\n\u001b[1;32m   1042\u001b[0m \u001b[39mif\u001b[39;00m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mthreaded:\n\u001b[1;32m   1043\u001b[0m     \u001b[39mself\u001b[39m\u001b[39m.\u001b[39m__threaded_polling(non_stop\u001b[39m=\u001b[39mnon_stop, interval\u001b[39m=\u001b[39minterval, timeout\u001b[39m=\u001b[39mtimeout, long_polling_timeout\u001b[39m=\u001b[39mlong_polling_timeout,\n\u001b[1;32m   1044\u001b[0m                             logger_level\u001b[39m=\u001b[39mlogger_level, allowed_updates\u001b[39m=\u001b[39mallowed_updates)\n",
      "File \u001b[0;32m~/anaconda3/lib/python3.10/site-packages/telebot/__init__.py:273\u001b[0m, in \u001b[0;36mTeleBot.user\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    265\u001b[0m \u001b[39m\"\"\"\u001b[39;00m\n\u001b[1;32m    266\u001b[0m \u001b[39mThe User object representing this bot.\u001b[39;00m\n\u001b[1;32m    267\u001b[0m \u001b[39mEquivalent to bot.get_me() but the result is cached so only one API call is needed.\u001b[39;00m\n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m    270\u001b[0m \u001b[39m:rtype: :class:`telebot.types.User`\u001b[39;00m\n\u001b[1;32m    271\u001b[0m \u001b[39m\"\"\"\u001b[39;00m\n\u001b[1;32m    272\u001b[0m \u001b[39mif\u001b[39;00m \u001b[39mnot\u001b[39;00m \u001b[39mhasattr\u001b[39m(\u001b[39mself\u001b[39m, \u001b[39m\"\u001b[39m\u001b[39m_user\u001b[39m\u001b[39m\"\u001b[39m):\n\u001b[0;32m--> 273\u001b[0m     \u001b[39mself\u001b[39m\u001b[39m.\u001b[39m_user \u001b[39m=\u001b[39m \u001b[39mself\u001b[39;49m\u001b[39m.\u001b[39;49mget_me()\n\u001b[1;32m    274\u001b[0m \u001b[39mreturn\u001b[39;00m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39m_user\n",
      "File \u001b[0;32m~/anaconda3/lib/python3.10/site-packages/telebot/__init__.py:1236\u001b[0m, in \u001b[0;36mTeleBot.get_me\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m   1229\u001b[0m \u001b[39mdef\u001b[39;00m \u001b[39mget_me\u001b[39m(\u001b[39mself\u001b[39m) \u001b[39m-\u001b[39m\u001b[39m>\u001b[39m types\u001b[39m.\u001b[39mUser:\n\u001b[1;32m   1230\u001b[0m     \u001b[39m\"\"\"\u001b[39;00m\n\u001b[1;32m   1231\u001b[0m \u001b[39m    A simple method for testing your bot's authentication token. Requires no parameters.\u001b[39;00m\n\u001b[1;32m   1232\u001b[0m \u001b[39m    Returns basic information about the bot in form of a User object.\u001b[39;00m\n\u001b[1;32m   1233\u001b[0m \n\u001b[1;32m   1234\u001b[0m \u001b[39m    Telegram documentation: https://core.telegram.org/bots/api#getme\u001b[39;00m\n\u001b[1;32m   1235\u001b[0m \u001b[39m    \"\"\"\u001b[39;00m\n\u001b[0;32m-> 1236\u001b[0m     result \u001b[39m=\u001b[39m apihelper\u001b[39m.\u001b[39;49mget_me(\u001b[39mself\u001b[39;49m\u001b[39m.\u001b[39;49mtoken)\n\u001b[1;32m   1237\u001b[0m     \u001b[39mreturn\u001b[39;00m types\u001b[39m.\u001b[39mUser\u001b[39m.\u001b[39mde_json(result)\n",
      "File \u001b[0;32m~/anaconda3/lib/python3.10/site-packages/telebot/apihelper.py:196\u001b[0m, in \u001b[0;36mget_me\u001b[0;34m(token)\u001b[0m\n\u001b[1;32m    194\u001b[0m \u001b[39mdef\u001b[39;00m \u001b[39mget_me\u001b[39m(token):\n\u001b[1;32m    195\u001b[0m     method_url \u001b[39m=\u001b[39m \u001b[39mr\u001b[39m\u001b[39m'\u001b[39m\u001b[39mgetMe\u001b[39m\u001b[39m'\u001b[39m\n\u001b[0;32m--> 196\u001b[0m     \u001b[39mreturn\u001b[39;00m _make_request(token, method_url)\n",
      "File \u001b[0;32m~/anaconda3/lib/python3.10/site-packages/telebot/apihelper.py:80\u001b[0m, in \u001b[0;36m_make_request\u001b[0;34m(token, method_name, method, params, files)\u001b[0m\n\u001b[1;32m     70\u001b[0m \u001b[39m\"\"\"\u001b[39;00m\n\u001b[1;32m     71\u001b[0m \u001b[39mMakes a request to the Telegram API.\u001b[39;00m\n\u001b[1;32m     72\u001b[0m \u001b[39m:param token: The bot's API token. (Created with @BotFather)\u001b[39;00m\n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m     77\u001b[0m \u001b[39m:return: The result parsed to a JSON dictionary.\u001b[39;00m\n\u001b[1;32m     78\u001b[0m \u001b[39m\"\"\"\u001b[39;00m\n\u001b[1;32m     79\u001b[0m \u001b[39mif\u001b[39;00m \u001b[39mnot\u001b[39;00m token:\n\u001b[0;32m---> 80\u001b[0m     \u001b[39mraise\u001b[39;00m \u001b[39mException\u001b[39;00m(\u001b[39m'\u001b[39m\u001b[39mBot token is not defined\u001b[39m\u001b[39m'\u001b[39m)\n\u001b[1;32m     81\u001b[0m \u001b[39mif\u001b[39;00m API_URL:\n\u001b[1;32m     82\u001b[0m     \u001b[39m# noinspection PyUnresolvedReferences\u001b[39;00m\n\u001b[1;32m     83\u001b[0m     request_url \u001b[39m=\u001b[39m API_URL\u001b[39m.\u001b[39mformat(token, method_name)\n",
      "\u001b[0;31mException\u001b[0m: Bot token is not defined"
     ]
    }
   ],
   "source": [
    "bot.polling()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
