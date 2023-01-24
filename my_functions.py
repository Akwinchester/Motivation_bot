from mysql.connector import connect, Error

try:
    with connect(
        host='localhost',
        user='1',
        password='Proba1',
        database='Bot_motivation'
    ) as connection:
        cursor = connection.cursor()
        sql_add_row = '''INSERT INTO base_table(activity, amount, unit) VALUES ('отжимания', 20, 'повторов'), ('подтягивания',  14, 'повторов')'''
        cursor.execute(sql_add_row)
        connection.commit()
except Error as e:
    print(e)