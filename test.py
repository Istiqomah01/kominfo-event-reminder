import app
import os
import pandas as pd
from datetime import datetime
import time
import telebot
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
# group_id = os.getenv("GROUP_ID")
test_group_id = os.getenv("TEST_GROUP_ID")

bot = telebot.TeleBot(TOKEN)

bot.send_message(test_group_id, "bruhhhh", parse_mode='Markdown')
if __name__ == '__main__':
    app.birthday_job("birthday_list.csv", test_group_id, bot)
    app.event_job("event_insta.csv", test_group_id, bot)