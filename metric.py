import psycopg2
from datetime import datetime
from config import load_config


def join_base():
    try:
        connection = psycopg2.connect(host=load_config().db.host, user=load_config().db.userb,
                                      port=load_config().db.port,
                                      password=load_config().db.password, database=load_config().db.db_name)
        connection.autocommit = True

        return connection

    except Exception as ex:
        print('This is ERROR ', ex)


def count_rows_day(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d.%m.%y')
        formatted_date = date_obj.strftime('%Y-%m-%d')

        connection = join_base()
        cursor = join_base().cursor()

        query = 'SELECT COUNT(*) FROM users WHERE entr_date = %s;'
        cursor.execute(query, (formatted_date,))
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return f"Количество строк с датой {formatted_date}: {count}"

    except Exception as ex:
        print('This is ERROR', ex)
        return 'Некорректные данные'


def count_rows_mon(month):
    try:
        month_obj = datetime.strptime(month, '%m.%y')
        formatted_month = month_obj.strftime('%m.%y')

        connection = join_base()
        cursor = connection.cursor()

        query = '''SELECT COUNT(*) FROM users WHERE to_char(entr_date, 'MM.YY') = %s;'''
        cursor.execute(query, (formatted_month,))
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return f'Количество строк с месяцем {formatted_month}: {count}'

    except Exception as ex:
        print('This is ERROR', ex)
        return 'Некорректные данные'