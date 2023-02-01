from mysql.connector import connect, Error
from keyboa import Keyboa
from telebot import types
from settings import *
import re
from datetime import date
from google_service import *


def save_data(data_row):
    try:
        with connect(
            host='localhost',
            user='1',
            password='Proba1',
            database='Bot_motivation'
        ) as connection:
            cursor = connection.cursor()
            add_row = '''INSERT INTO base_table(date, category, activity, amount, characteristic, description, user_id) VALUES (%(date)s, %(category)s, %(activity)s, %(amount)s, %(characteristic)s, %(description)s, %(user_id)s)'''
            cursor.execute(add_row, data_row)
            connection.commit()
    except Error as e:
        print(e)


#клавиатуры
def make_keyboard_start():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(BUTTON_TEXT['start'])
    markup.add(button1)
    return markup


def make_keyboard_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(BUTTON_TEXT['add_row'])
    button2 = types.KeyboardButton(BUTTON_TEXT['shere_friends'])
    button3 = types.KeyboardButton(BUTTON_TEXT['information'])
    button4 = types.KeyboardButton(BUTTON_TEXT['help'])
    button5 = types.KeyboardButton(BUTTON_TEXT['To_do'])
    button6 = types.KeyboardButton(BUTTON_TEXT['text_training'])
    markup.add(button1, button2)
    markup.add(button3, button4)
    markup.add(button5, button6)
    return markup


def make_keyboard_add_row():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(BUTTON_TEXT['cancel'])
    markup.add(button1)
    return markup


#парсинг тренировки
def pars_data(message_text, chat_id):
    data_for_upload = {}
    data_for_upload = {column: None for column in columns}
    list_data = re.split('[\n]', message_text)
    data_for_upload['date'] = date.today()
    data_for_upload['category'] = list_data[0].split(':')[0].lower()
    data_for_upload['user_id'] = chat_id
    for i in list_data[1:]:
        activity_data = re.split(r"\s+", i)
        data_for_upload['activity'] = activity_data[0].lower()
        if len(activity_data[1:]) > 1:
            amount = 0
            for j in activity_data[1:]:
                try:
                    amount = amount + int(j)
                except:
                    print('в данных подхода есть недопустимые символы')
        else:
            amount = activity_data[1]
        data_for_upload['amount'] = amount
        print(data_for_upload)
        save_data(data_for_upload)
        send_google_sheet(chat_id)


def create_notice_text(data_for_upload):
    message_text = f'<b>Пользоваетель:</b> {users[str(data_for_upload["user_id"])]} \n'
    for i in data_for_upload:
        if data_for_upload[i] != None and i != 'user_id' and i != 'category':
            message_text += title_for_notice[i] + ' ' + str(data_for_upload[i]) + '\n'
    return message_text
