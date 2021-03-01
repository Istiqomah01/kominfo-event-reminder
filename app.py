import pandas as pd
from datetime import datetime, timedelta
import time
import telebot
import schedule
import os
from os import environ
import pytz

from dotenv import load_dotenv
load_dotenv()

#setup timezone
WIB = pytz.timezone('Asia/Jakarta')
today_datetime = datetime.now(tz = WIB)


#Birthday Stuff

def birthday_dataframe_prep(data):
    df = pd.read_csv(data)
    df["Birthday"] = pd.to_datetime(df["Birthday"], dayfirst=True)
    df["Birthday_day"] = df["Birthday"].dt.day
    df["Birthday_month"] = df["Birthday"].dt.month
    df["Birthday_year"] = df["Birthday"].dt.year
    df.sort_values(by=["Birthday_month", "Birthday_day"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index += 1

    return df

def month_name(month_num):
    month = {1:'Januari',
            2:'Februari',
            3:'Maret',
            4:'April',
            5:'Mei',
            6:'Juni',
            7:'Juli',
            8:'Agustus',
            9:'September',
            10:'Oktober',
            11:'November',
            12:'Desember'}

    return month[month_num]

def get_today_birthday(data):
    today_day = today_datetime.day
    today_month = today_datetime.month
    mask = (data["Birthday_day"] == today_day) & (data["Birthday_month"] == today_month)
    birthday = data.loc[mask]
    birthday.reset_index(drop=True, inplace=True)
    birthday.index += 1

    if birthday.empty:
        return None
    else:
        output = "Ulang Tahun Hari ini:"
        for data in birthday.iterrows():
            no = data[0]
            nama = data[1].loc['Name']
            tanggal = data[1].loc['Birthday_day']
            bulan = month_name(data[1].loc['Birthday_month'])
            tahun = data[1].loc['Birthday_year']
            umur = datetime.today().year - data[1].loc['Birthday_year']

            output += f"\n{no}. *{nama}*, {tanggal} {bulan} {tahun}, {umur} Tahun"

        return output

def get_tomorrow_birthday(data):
    one_day = timedelta(days=1)
    tomorrow = today_datetime + one_day

    tomorrow_day = tomorrow.day
    tomorrow_month = tomorrow.month
    mask = (data["Birthday_day"] == tomorrow_day) & (data["Birthday_month"] == tomorrow_month)
    birthday = data.loc[mask]
    birthday.reset_index(drop=True, inplace=True)
    birthday.index += 1

    if birthday.empty:
        return None
    else:
        output = "Ulang Tahun Besok:"
        for data in birthday.iterrows():
            no = data[0]
            nama = data[1].loc['Name']
            tanggal = data[1].loc['Birthday_day']
            bulan = month_name(data[1].loc['Birthday_month'])
            tahun = data[1].loc['Birthday_year']
            umur = datetime.today().year - data[1].loc['Birthday_year']

            output += f"\n{no}. *{nama}*, {tanggal} {bulan} {tahun}, {umur} Tahun"

        return output

def get_this_month_birthday(data):
    this_month = today_datetime.month
    mask = (data["Birthday_month"] == this_month)
    birthday = data.loc[mask]
    birthday.reset_index(drop=True, inplace=True)
    birthday.index += 1

    if birthday.empty:
        return None
    else:
        output = "Ulang Tahun Bulan ini:"
        for data in birthday.iterrows():
            no = data[0]
            nama = data[1].loc['Name']
            tanggal = data[1].loc['Birthday_day']
            bulan = month_name(data[1].loc['Birthday_month'])
            tahun = data[1].loc['Birthday_year']
            umur = datetime.today().year - data[1].loc['Birthday_year']

            output += f"\n{no}. *{nama}*, {tanggal} {bulan} {tahun}, {umur} Tahun"

        return output

def send_birthday_info(data, chat_id, bot):
    # Send message for the month
    if today_datetime.day == 1:
        month_message = get_this_month_birthday(data)
        if month_message is not None:
            bot.send_message(chat_id, month_message, parse_mode='Markdown')
            print(f"sending message: {month_message}\n{datetime.now()}\n")
        else:
            print(f"tidak ada ulang tahun bulan ini, {datetime.now()}")

    # Send message for today
    today_message = get_today_birthday(data)
    if today_message is not None:
        bot.send_message(chat_id, today_message, parse_mode='Markdown')
        print(f"sending message: {today_message}\n{datetime.now()}\n")
    else:
        print(f"tidak ada ulang tahun hari ini, {datetime.now()}")        

    # Send message for tomorrow
    tomorrow_message =  get_tomorrow_birthday(data)
    if tomorrow_message is not None:
        bot.send_message(chat_id, tomorrow_message, parse_mode='Markdown')
        print(f"sending message: {tomorrow_message}\n{datetime.now()}\n")
    else:
        print(f"tidak ada ulang tahun besok, {datetime.now()}") 


#Instagram Event

def event_dataframe_prep(data):
    df = pd.read_csv(data)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Date_day"] = df["Date"].dt.day
    df["Date_month"] = df["Date"].dt.month
    df["Date_year"] = df["Date"].dt.year
    df.sort_values(by=["Date_month", "Date_day"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index += 1

    return df

def get_today_event(data):
    today_day = today_datetime.day
    today_month = today_datetime.month
    mask = (data["Date_day"] == today_day) & (data["Date_month"] == today_month)
    event = data.loc[mask]
    event.reset_index(drop=True, inplace=True)
    event.index += 1

    if event.empty:
        return None
    else:
        output = "Event Hari ini:"
        for data in event.iterrows():
            no = data[0]
            nama = data[1].loc['Event']
            tanggal = data[1].loc['Date_day']
            bulan = month_name(data[1].loc['Date_month'])
            tahun = data[1].loc['Date_year']

            output += f"\n{no}. *{nama}*, {tanggal} {bulan} {tahun}"

        return output

def get_tomorrow_event(data):
    one_day = timedelta(days=1)
    tomorrow = today_datetime + one_day

    tomorrow_day = tomorrow.day
    tomorrow_month = tomorrow.month
    mask = (data["Date_day"] == tomorrow_day) & (data["Date_month"] == tomorrow_month)
    event = data.loc[mask]
    event.reset_index(drop=True, inplace=True)
    event.index += 1

    if event.empty:
        return None
    else:
        output = "Event Besok:"
        for data in event.iterrows():
            no = data[0]
            nama = data[1].loc['Event']
            tanggal = data[1].loc['Date_day']
            bulan = month_name(data[1].loc['Date_month'])
            tahun = data[1].loc['Date_year']

            output += f"\n{no}. *{nama}*, {tanggal} {bulan} {tahun}"

        return output

def get_this_month_event(data):
    today_month = today_datetime.month
    mask = (data["Date_month"] == today_month)
    event = data.loc[mask]
    event.reset_index(drop=True, inplace=True)
    event.index += 1

    if event.empty:
        return None
    else:
        output = "Event Bulan ini:"
        for data in event.iterrows():
            no = data[0]
            nama = data[1].loc['Event']
            tanggal = data[1].loc['Date_day']
            bulan = month_name(data[1].loc['Date_month'])
            tahun = data[1].loc['Date_year']

            output += f"\n{no}. *{nama}*, {tanggal} {bulan} {tahun}"

        return output

def send_event_info(data, chat_id, bot):
    # Send message for the month
    if today_datetime.day == 1:
        month_message = get_this_month_event(data)
        if month_message is not None:
            bot.send_message(chat_id, month_message, parse_mode='Markdown')
            print(f"sending message: {month_message}\n{datetime.now()}\n")
        else:
            print(f"tidak ada event bulan ini, {datetime.now()}")

    # Send message for today
    today_message = get_today_event(data)
    if today_message is not None:
        bot.send_message(chat_id, today_message, parse_mode='Markdown')
        print(f"sending message: {today_message}\n{datetime.now()}\n")
    else:
        print(f"tidak ada event hari ini, {datetime.now()}")  

    # Send message for tomorrow
    tomorrow_message =  get_tomorrow_event(data)
    if tomorrow_message is not None:
        bot.send_message(chat_id, tomorrow_message, parse_mode='Markdown')
        print(f"sending message: {tomorrow_message}\n{datetime.now()}\n")
    else:
        print(f"tidak ada event besok, {datetime.now()}")    


#schedule job

def birthday_job(dataframe, chat_id, bot):
    data = birthday_dataframe_prep(dataframe)
    send_birthday_info(data, chat_id, bot)

def event_job(dataframe, chat_id, bot):
    data = event_dataframe_prep(dataframe)
    send_event_info(data, chat_id, bot)

#logging every one minute

def is_working():
    print(f"the application is still running, {datetime.now()}, GROUP_ID: {environ['GROUP_ID']}, TOKEN: {environ['TOKEN']}, Timezone: {environ['TZ']}")


if __name__=="__main__":
    TOKEN = environ["TOKEN"]
    group_id = environ["GROUP_ID"]

    bot = telebot.TeleBot(TOKEN)

    schedule.every(1).minutes.do(is_working)
    schedule.every().day.at("00:30").do(birthday_job, "birthday_list.csv", group_id, bot)
    schedule.every().day.at("00:30").do(event_job, "event_insta.csv", group_id, bot)

    while True:
        schedule.run_pending()
        time.sleep(1)

    # data = event_dataframe_prep("event_insta.csv")
    # print(get_this_month_event(data))
    # print(get_today_event(data))

