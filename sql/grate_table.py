import sqlite3
from os.path import isfile, join
from functions import DATABASE_PATH

INIT_GRATE_FILE_PATH = 'init.sql'


def get_sql_from_file(file_name):
    """
    Получаем чистый sql из файла
    :param file_name: полный путь до файла
    :return: строка с запросом
    """
    connect = ''
    if isfile(file_name):
        with open(file_name, encoding='utf-8') as file:
            connect = file.read()
    return connect


def create_table():
    """Создаем таблицу"""
    with sqlite3.connect(join('../', DATABASE_PATH)) as connection:
        cursor = connection.cursor()
        query = get_sql_from_file(INIT_GRATE_FILE_PATH)
        cursor.executescript(query)


if __name__ == '__main__':
    create_table()
