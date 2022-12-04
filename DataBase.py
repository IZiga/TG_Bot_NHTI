import sqlite3 as sql
import datetime




def get_lees_inf(time_stamp: datetime):
    """

    Вернеть преоброзованое готовое сообщение

    :param time_stamp: время в datetime

    :return: Текст для сообщение

    """
    con = sql.connect('example.db', check_same_thread=False)
    cur = con.cursor()
    day = time_stamp.day

    # __________Обращаемся к 1 таблице________
    month = time_stamp.month
    year = time_stamp.year
    req = f"SELECT * FROM schedule_day Where day={day} AND month={month} AND year={year};"
    cur.execute(req)
    mes = ''
    for lesson_inf in cur.fetchall():
        mes += f"📖 {lesson_inf[0]} \n 👨‍🏫 {lesson_inf[1]} \n 🚪 каб. {lesson_inf[8]}\n 📝 {lesson_inf[2]} \n 🕕 с {lesson_inf[6]} \n 🕚 по {lesson_inf[7]}\n\n"

    # __________Обращаемся к 2 таблице________

    n_day = time_stamp.weekday()
    n_week = time_stamp.isocalendar().week % 2
    req = f"SELECT * FROM schedule Where n_day={n_day} AND n_week={n_week};"
    cur.execute(req)
    for lesson_inf in cur.fetchall():
        mes += f"📖 {lesson_inf[0]} \n 👨‍🏫 {lesson_inf[6]} \n 🚪 каб. {lesson_inf[8]}\n 📝 {lesson_inf[7]}\n 🕕 с {lesson_inf[1]} \n 🕚 по {lesson_inf[2]} \n\n"

    return mes if not(mes=='') else 'по расписанию Курим бамбуг'


def mes_exams(time_stamp: datetime):
    """

        Вернеть преоброзованое готовое сообщение

        :param time_stamp: время в datetime

        :return: Текст для сообщение

    """
    day = time_stamp.day
    month = time_stamp.month
    year = time_stamp.year
    con = sql.connect('example.db', check_same_thread=False)
    cur = con.cursor()
    ex_type = ['Экзамен', 'Консультация']
    req = f"SELECT * FROM schedule_day Where (type='Экзамен' OR type='Консультация')AND " \
          f"(year>{year} OR (year={year} AND ( month>{month}  OR (month={month} AND day>={day}))));"
    cur.execute(req)
    mes = ''
    for lesson_inf in cur.fetchall():
        if lesson_inf[2] == ex_type[0]:
            mes += f"🛑 {lesson_inf[2]} {lesson_inf[3]}.{lesson_inf[4]}.{lesson_inf[5]} \n 📖 {lesson_inf[0]} \n 👨‍🏫 {lesson_inf[1]} \n 🚪 каб. {lesson_inf[8]}\n 🕕 с {lesson_inf[6]} \n 🕚 по {lesson_inf[7]}\n\n"
        elif lesson_inf[2] == ex_type[1]:
            mes += f"⚠️{lesson_inf[2]} {lesson_inf[3]}.{lesson_inf[4]}.{lesson_inf[5]} \n 📖 {lesson_inf[0]} \n 👨‍🏫 {lesson_inf[1]} \n 🚪 каб. {lesson_inf[8]}\n 🕕 с {lesson_inf[6]} \n 🕚 по {lesson_inf[7]}\n\n"
        else:
            print('Ошибка!!!')
        continue
    return mes if not(mes=='') else 'на расслабоне на чили'