import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from mysql.connector import connect, Error, connection
from settings import *

# Подсоединение к Google Таблицам
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)

# sheet = client.create("Motivation_log")
# sheet.share('maxim1800maxim1800maxim@gmail.com', perm_type='user', role='writer')
# sheet = client.open('Motivation_log').sheet1
# df = pd.read_csv('data.csv', delimiter=',')

# sheet.update([df.columns.values.tolist()] + df.values.tolist())

def send_google_sheet(chat_id):
    try:
        with connect(
            host='localhost',
            user='1',
            password='Proba1',
            database='Bot_motivation'
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT DATE_FORMAT(date,"%d.%m.%Y") AS date, category, activity, amount, characteristic, description FROM base_table WHERE user_id = {chat_id}')
            data = cursor.fetchall()
            sheet = client.open(table_name[str(chat_id)]).sheet1
            sheet.update(data)
    except Error as e:
        print(e)
