import pandas as pd
from datetime import datetime
import time
import telebot
import schedule
import os
from os import environ

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

def birthday_month_name(birthday_month):
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

    return month[birthday_month]

def get_today_birthday(data):
    today_day = datetime.today().day
    today_month = datetime.today().month
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
            bulan = birthday_month_name(data[1].loc['Birthday_month'])
            tahun = data[1].loc['Birthday_year']
            umur = datetime.today().year - data[1].loc['Birthday_year']

            output += f"\n{no}. *{nama}*, {tanggal} {bulan} {tahun}, {umur} Tahun"

        return output

def get_this_month_birthday(data):
    this_month = datetime.today().month
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
            bulan = birthday_month_name(data[1].loc['Birthday_month'])
            tahun = data[1].loc['Birthday_year']
            umur = datetime.today().year - data[1].loc['Birthday_year']

            output += f"\n{no}. *{nama}*, {tanggal} {bulan} {tahun}, {umur} Tahun"

        return output

def send_birthday_info(data, chat_id):
    if datetime.today().day == 1:
        month_message = get_this_month_birthday(data)
        if month_message is not None:
            bot.send_message(chat_id, month_message, parse_mode='Markdown')
            print(f"sending message: {month_message}\n{datetime.now()}\n")
        else:
            print(f"tidak ada ulang tahun bulan ini, {datetime.now()}")

    today_message = get_today_birthday(data)
    if today_message is not None:
        bot.send_message(chat_id, today_message, parse_mode='Markdown')
        print(f"sending message: {today_message}\n{datetime.now()}\n")
    else:
        print(f"tidak ada ulang tahun hari ini, {datetime.now()}")         

def birthday_job(dataframe, chat_id):
    data = birthday_dataframe_prep(dataframe)
    send_birthday_info(data, chat_id)

if __name__=="__main__":
    TOKEN = environ["TOKEN"]
    group_id = environ["GROUP_ID"]

    bot = telebot.TeleBot(TOKEN)

    # schedule.every(3).seconds.do(birthday_job, "birthday_list.csv", i[1])
    schedule.every().day.at("00:30").do(birthday_job, "birthday_list.csv", group_id)

    while True:
        schedule.run_pending()
        time.sleep(1)
    # data = birthday_dataframe_prep("birthday_list.csv")
    # print(get_this_month_birthday(data))

