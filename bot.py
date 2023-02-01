import os.path
import shutil
import telebot
import requests
from settings import *
from my_functions import *
from google_service import *
import re
from telebot import types
from keyboa import Keyboa
from datetime import date


bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

class Data:
    data_for_upload = {}


#обратный вызов
data_for_edit = {}
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data in categoryes:
        if call.data == 'уникальный отчет':
            bot.send_message(call.message.chat.id, 'функция в разработке')
        else:
            Data.data_for_upload['user_id'] = call.message.chat.id
            Data.data_for_upload['category'] = call.data
            bot.send_message(call.message.chat.id, '⬆️⬆️⬆️⬆️⬆️⬆️', reply_markup=make_keyboard_add_row())
            show_list_activities(call)
            data_for_edit['first_inline'] = [call.message.id, call.message.chat.id]
    elif call.data in inline_keyboards['add_amount']:
        if call.data == inline_keyboards['add_amount'][0]:
            ms = bot.send_message(call.message.chat.id, 'введи сколько сделал')
            data_for_edit['amount'] = [ms.id, ms.chat.id]
            bot.register_next_step_handler(call.message, get_amount)
        else:
            edit_inline_shere(buttons_key='add_characteristic', message_text='Добавить характеристику')
    elif call.data in activities['тренировка'] or call.data in activities['программирование']:
        Data.data_for_upload['date'] = str(date.today())
        Data.data_for_upload['activity'] = call.data
        edit_inline_shere(buttons_key='add_amount', message_text='Можешь не указывать количественную характеристику')
    elif call.data in inline_keyboards['add_characteristic']:
        if call.data ==  inline_keyboards['add_characteristic'][0]:
            ms = bot.send_message(call.message.chat.id, 'введи характеристику')
            data_for_edit['characteristic'] = [ms.id, ms.chat.id]
            bot.register_next_step_handler(call.message, get_characteristic)

        if call.data == inline_keyboards['add_characteristic'][1]:
            edit_inline_shere(buttons_key='shere_with_friend', message_text='Поделиться достижением?')
    elif call.data in inline_keyboards['shere_with_friend']:
        save_data(Data.data_for_upload)
        if call.data == inline_keyboards['shere_with_friend'][0]:
            shere_friend(call)
        if call.data == inline_keyboards['shere_with_friend'][1]:
            bot.send_message(call.message.chat.id, '✅ данные добалены', reply_markup=make_keyboard_main_menu())
            send_google_sheet(call.message.chat.id)




def show_list_activities(call):
    keyboard = Keyboa(items=activities[call.data], items_in_row=2)
    bot.edit_message_text(text=call.data, message_id=call.message.id, chat_id=call.message.chat.id, reply_markup=keyboard())


def get_amount(message):
    Data.data_for_upload['amount'] = int(message.text)
    edit_inline_shere(buttons_key='add_characteristic', message_text='Добавить характеристику')
    bot.delete_message(message_id=data_for_edit['amount'][0], chat_id=data_for_edit['amount'][1])


def edit_inline_shere(buttons_key, message_text):
    keyboard = Keyboa(items=inline_keyboards[buttons_key], items_in_row=2)
    bot.edit_message_text(text=message_text, message_id=data_for_edit['first_inline'][0], chat_id=data_for_edit['first_inline'][1],
                          reply_markup=keyboard())


def shere_friend(call):
    if call.message.chat.id == 1622588506:
        # chat_id = 1227443938
        chat_id = 1622588506
        name = 'Арсений'
    else:
        chat_id = 1622588506
        name = 'Максим'
    bot.send_message(chat_id, create_notice_text(Data.data_for_upload))
    bot.send_message(call.message.chat.id, '✅ данные загружены. Друг узнал о вашем достижении, ждите ответа', reply_markup=make_keyboard_main_menu())
    send_google_sheet(call.message.chat.id)


def get_characteristic(message):
    Data.data_for_upload['characteristic'] = message.text
    edit_inline_shere(buttons_key='shere_with_friend', message_text='Хочешь поделиться результатом?')
    bot.delete_message(message_id=data_for_edit['characteristic'][0], chat_id=data_for_edit['characteristic'][1])



@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, MESSAGE_TEXT['start'], reply_markup=make_keyboard_start())


@bot.message_handler(commands=['update'])
def welcome(message):
    send_google_sheet(message.chat.id)


@bot.message_handler(content_types=['text'], regexp=BUTTON_TEXT['start'])
def start_button(message):
    bot.send_message(message.chat.id, MESSAGE_TEXT['main_menu'], reply_markup=make_keyboard_main_menu())


@bot.message_handler(content_types=['text'], regexp=BUTTON_TEXT['cancel'])
def start_button(message):
    bot.send_message(message.chat.id, MESSAGE_TEXT['main_menu'], reply_markup=make_keyboard_main_menu())


@bot.message_handler(content_types=['text'], regexp=BUTTON_TEXT['add_row'])
def one_button(message):
    Data.data_for_upload = {column:None for column in columns}
    keyboard = Keyboa(items=categoryes, items_in_row=2)
    bot.send_message(message.chat.id, MESSAGE_TEXT['activities'], reply_markup=keyboard())


@bot.message_handler(content_types=['text'], regexp=BUTTON_TEXT['shere_friends'])
def two_button(message):
    bot.send_message(message.chat.id, 'функция в разработке')


@bot.message_handler(content_types=['text'], regexp=BUTTON_TEXT['information'])
def three_button(message):
    bot.send_message(message.chat.id, 'функция в разработке')


@bot.message_handler(content_types=['text'], regexp=BUTTON_TEXT['help'])
def four_button(message):
    bot.send_message(message.chat.id, 'функция в разработке')


@bot.message_handler(content_types=['text'], regexp=BUTTON_TEXT['To_do'])
def start_button(message):
    bot.send_message(message.chat.id, MESSAGE_TEXT['add_To_do'], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, add_To_do)


def add_To_do(message):
    if message.chat.id == 1622588506:
        chat_id = 1622588506
        name = 'Арсений'
    else:
        chat_id = 1622588506
        name = 'Максим'
    bot.send_message(chat_id, f'{name} только что сделал план на следующий день')
    bot.send_message(chat_id, message.text)
    bot.send_message(message.chat.id, 'Данные отправлены',
                     reply_markup=make_keyboard_main_menu())


@bot.message_handler(content_types=['text'], regexp=BUTTON_TEXT['text_training'])
def start_button(message):
    bot.send_message(message.chat.id, MESSAGE_TEXT['add_text_training_1'], reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, MESSAGE_TEXT['add_text_training_2'])
    bot.register_next_step_handler(message, add_text_training)


def add_text_training(message):
    pars_data(message_text=message.text, chat_id=message.chat.id)
    bot.send_message(message.chat.id, '✅ данные добалены', reply_markup=make_keyboard_main_menu())


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)