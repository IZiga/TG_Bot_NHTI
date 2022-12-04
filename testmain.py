import telebot
import config
import applog
import datetime
import pandas as pd
import DataBase as DB
import subprocess
import tempfile
import time
import os
import requests
from telebot.types import InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo


log = applog.get_logger('Test')
bot = telebot.TeleBot(token=config.token)

datetime_OFF = 1


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'start',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    rep = bot.reply_to(message, "Howdy, how are you doing?")
    new_row = {'user_id': rep.from_user.id,
               'message_id': rep.message_id,
               'chat_id': rep.chat.id,
               'timestamp': rep.date,
               'type': rep.content_type}
    df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)


@bot.message_handler(commands=['OFFflud'])
def dell_mess(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'OFFflud',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    if message.from_user.id in config.major_id:
        global datetime_OFF
        rep = bot.send_photo(chat_id=message.chat.id, photo=open('img/in_work.jpg','rb'), caption="У меня пока обед!")
        datetime_OFF = message.date
        log.info(datetime_OFF)
    else:
        rep = bot.send_message('не достаточно привелегии обратитесь к администратору')
    new_row = {'user_id': rep.from_user.id,
               'message_id': rep.message_id,
               'chat_id': rep.chat.id,
               'timestamp': rep.date,
               'type': rep.content_type}
    df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)


@bot.message_handler(commands=['get_lec'])
def get_lectures(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'get_lec',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    try:
        log.info('Команда сработала')
        directory = 'lectures/'
        directory += message.text.split()[1]+'/'
        files_name = os.listdir(directory)
        media = []
        for file_name in files_name:
            file = open(directory+file_name, 'rb')
            media.append(InputMediaDocument(file))
        rep = bot.send_media_group(chat_id=message.chat.id,
                                   media=media,)
    except FileNotFoundError as not_found_er:
        log('File не обнаружен')
        log.error(not_found_er)
        rep = bot.send_message(chat_id=message.chat.id,
                               text='Такой лекции нету',)
    except Exception as e:
        log.error(e)
        rep = bot.send_message(chat_id=message.chat.id,
                         text="❗️Неизвестная ошибка")
    if type(rep) == list:
        for item in rep:
            new_row = {'user_id': item.from_user.id,
                       'message_id': item.message_id,
                       'chat_id': item.chat.id,
                       'timestamp': item.date,
                       'type': item.content_type}
            df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    else:
        new_row = {'user_id': rep.from_user.id, 
                   'message_id': rep.message_id,
                   'chat_id': rep.chat.id,
                   'timestamp': rep.date,
                   'type': rep.content_type}
        df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)
    pass


@bot.message_handler(commands=['lectures'])
def get_lectures(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'lectures',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    try:
        directory = 'lectures/'
        files_name = os.listdir(directory)
        mes = '\n'.join(files_name)
        rep = bot.send_message(chat_id=message.chat.id,
                               text=mes)
    except Exception as e:
        log.error(e)
        rep = bot.send_message(chat_id=message.chat.id,
                               text="❗️Неизвестная ошибка")
    new_row = {'user_id': rep.from_user.id,
               'message_id': rep.message_id,
               'chat_id': rep.chat.id,
               'timestamp': rep.date,
               'type': rep.content_type}
    df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)


@bot.message_handler(commands=['practical'])
def get_lectures(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'practical',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    try:
        directory = 'practical/'
        files_name = os.listdir(directory)
        mes = '\n'.join(files_name)
        rep = bot.send_message(chat_id=message.chat.id,
                               text=mes)
    except Exception as e:
        log.error(e)
        rep = bot.send_message(chat_id=message.chat.id,
                               text="❗️Неизвестная ошибка")
    new_row = {'user_id': rep.from_user.id,
               'message_id': rep.message_id,
               'chat_id': rep.chat.id,
               'timestamp': rep.date,
               'type': rep.content_type}
    df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)


@bot.message_handler(commands=['get_pract', 'get_practical', 'get_prac'])
def get_lectures(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'get_practical',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    try:
        log.info('Команда сработала')
        directory = 'practical/'
        directory += message.text.split()[1]+'/'
        files_name = os.listdir(directory)
        media = []
        for file_name in files_name:
            file = open(directory+file_name, 'rb')
            media.append(InputMediaDocument(file))
        rep = bot.send_media_group(chat_id=message.chat.id,
                                   media=media,)
    except FileNotFoundError as not_found_er:
        log('File не обнаружен')
        log.error(not_found_er)
        rep = bot.send_message(chat_id=message.chat.id,
                               text='Такой лекции нету',)
    except Exception as e:
        log.error(e)
        rep = bot.send_message(chat_id=message.chat.id,
                         text="❗️Неизвестная ошибка")
    if type(rep) == list:
        for item in rep:
            new_row = {'user_id': item.from_user.id,
                       'message_id': item.message_id,
                       'chat_id': item.chat.id,
                       'timestamp': item.date,
                       'type': item.content_type}
            df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    else:
        new_row = {'user_id': rep.from_user.id,
                   'message_id': rep.message_id,
                   'chat_id': rep.chat.id,
                   'timestamp': rep.date,
                   'type': rep.content_type}
        df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)
    pass


@bot.message_handler(commands=['exams'])
def get_exams(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'exams',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    log.info('test Ок')
    timestamp = datetime.datetime.fromtimestamp(message.date)
    text = DB.mes_exams(timestamp)
    rep = bot.send_message(chat_id=message.chat.id, text=text)
    print('ок')
    new_row = {'user_id': rep.from_user.id,
               'message_id': rep.message_id,
               'chat_id': rep.chat.id,
               'timestamp': rep.date,
               'type': rep.content_type}
    df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)


@bot.message_handler(commands=['schedules_today'])
def get_schedule_today(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'schedules_today',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    log.info('test Ок')

    timestamp = datetime.datetime.fromtimestamp(message.date)
    text = DB.get_lees_inf(timestamp)
    rep = bot.send_message(chat_id=message.chat.id, text=text)
    print('ок')
    new_row = {'user_id': rep.from_user.id,
               'message_id': rep.message_id,
               'chat_id': rep.chat.id,
               'timestamp': rep.date,
               'type': rep.content_type}
    df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)


@bot.message_handler(commands=['schedules_tomorrow'])
def get_schedule_tomorrow(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'schedules_tomorrow',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    log.info('test Ок nex')
    timestamp = datetime.datetime.fromtimestamp(message.date+24*60*60)
    today = timestamp.day
    timestamp = timestamp.replace(day=today)

    text = DB.get_lees_inf(timestamp)
    rep = bot.send_message(chat_id=message.chat.id, text=text)
    print('ок')
    new_row = {'user_id': rep.from_user.id,
               'message_id': rep.message_id,
               'chat_id': rep.chat.id,
               'timestamp': rep.date,
               'type': rep.content_type}
    df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)


@bot.message_handler(commands=['homework'])
def get_schedule_date(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'homework',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    try:
        # TODO: препесать для предмета
        arg = message.text.split()[1:]
        t = ' '.join(arg)
        data_hw = pd.read_excel('Homework.xlsx')
        now = datetime.datetime.now()
        data_hw = data_hw.query("date_end > @now & class == @t")
        data_hw['date_start'] = data_hw.date_start.dt.strftime("%d.%m.%Y")
        data_hw['date_end'] = data_hw.date_end.dt.strftime("%d.%m.%Y")
        data_hw['file_name'] = 'Homework/' + data_hw.date_end + '/' + data_hw['class'] + '/'
        for data in data_hw:
            direct = data.file_name
            files = os.listdir(direct)
            media = []
            for file in files:
                file = open(direct+file, 'rb')
                media.append(InputMediaDocument(file))
            bot.send_media_group(chat_id=message.chat.id, media=media,)
            text = f'Домашка с:\t{data.date_start}\nДоделать до:\t{data.data_end}\nПредмет:\t{data["class"]}'
            rep = bot.send_message(chat_id=message.chat.id, text=text)

            new_row = {'user_id': rep.from_user.id,
                       'message_id': rep.message_id,
                       'chat_id': rep.chat.id,
                       'timestamp': rep.date,
                       'type': rep.content_type}
            df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    except Exception as e:
        data_hw = pd.read_excel('Homework.xlsx')
        now = datetime.datetime.now()
        data_hw = data_hw.query("date_end > @now")
        data_hw['date_start'] = data_hw.date_start.dt.strftime("%d.%m.%Y")
        data_hw['date_end'] = data_hw.date_end.dt.strftime("%d.%m.%Y")
        data_hw['file_name'] = 'Homework/' + data_hw.date_end + '/' + data_hw['class'] + '/'
        data = data_hw.to_dict('records')
        for d in data:
            print(d)
            direct = d['file_name']
            files = os.listdir(direct)
            media = []
            for file in files:
                file = open(direct+file, 'rb')
                media.append(InputMediaDocument(file))
            text = f'Домашка с:\t{d["date_start"]}\nДоделать до:\t{d["date_end"]}\nПредмет:\t{d["class"]}'
            rep = bot.send_message(chat_id=message.chat.id, text=text)
            bot.send_media_group(chat_id=message.chat.id, media=media,) 


            new_row = {'user_id': rep.from_user.id,
                       'message_id': rep.message_id,
                       'chat_id': rep.chat.id,
                       'timestamp': rep.date,
                       'type': rep.content_type}
            df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)


@bot.message_handler(commands=['date'])
def get_schedule_date(message):
    df_user_mess = pd.read_csv('Data/user_msg.csv')
    user_id = message.from_user.id
    chat_id = message.chat.id
    new_row = {'user_id': user_id,
               'message_id': message.id,
               'chat_id': chat_id,
               'timestamp': message.date,
               'type': message.content_type,
               'text': message.text,
               'command': 'date',
               'is_chat': 1 if user_id == chat_id else 0}
    df_user_mess = df_user_mess.append(new_row, ignore_index=True)
    df_user_mess.to_csv('Data/user_msg.csv', index=False)
    log.info(f'{user_id} in {chat_id} print {message.text}')

    df_bot_mess = pd.read_csv('Data/bot_msg.csv')
    try:
        arg = message.text.split()[1]
        day, month, year = [int(i) for i in arg.split('.')]
        timestamp = datetime.datetime.fromtimestamp(message.date)
        timestamp = timestamp.replace(day=day, month=month, year=year)
        text = DB.get_lees_inf(timestamp)
        rep = bot.send_message(chat_id=message.chat.id, text=text)
        print('ок')
    except Exception as e:
        rep = bot.send_message(chat_id=message.chat.id, text='❗️ Ты что то ввел неправильно')
        log.error(e)
    new_row = {'user_id': rep.from_user.id,
               'message_id': rep.message_id,
               'chat_id': rep.chat.id,
               'timestamp': rep.date,
               'type': rep.content_type}
    df_bot_mess = df_bot_mess.append(new_row, ignore_index=True)
    df_bot_mess.to_csv('Data/bot_msg.csv', index=False)


@bot.message_handler(content_types=['text'])
def save_text(message,):
    # message_data = pd.read_csv('Data/message_data.csv', encoding='utf-8')
    if 5*60 > message.date - datetime_OFF:
        print(message.date - datetime_OFF)
        if message.chat.id > 0:
            bot.delete_message(message.chat.id, message_id=message.id)
    elif message.chat.id > 0:
        df_user_mess = pd.read_csv('Data/msg.csv')
        user_id = message.from_user.id
        chat_id = message.chat.id
        new_row = {'user_id': user_id,
                   'message_id': message.id,
                   'chat_id': chat_id,
                   'timestamp': message.date,
                   'type': message.content_type,
                   'text': message.text,
                   'is_chat': 1 if user_id == chat_id else 0}
        df_user_mess = df_user_mess.append(new_row, ignore_index=True)
        df_user_mess.to_csv('Data/msg.csv', index=False)
        log.info(f'{user_id} in {chat_id} print {message.text}')



bot.infinity_polling()
