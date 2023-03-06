from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import sqlite3
import requests
from win11toast import toast as show_notify

useragent = "Mozilla/5.0(Windows NT10.0; Win64; x64) AppleWebKit/537.36(HTML,like Gecko) Chrome/109.0.0.0 " \
            "Safari/537.36 OPR/95.0.0.0(Edition Yx 05)"
DATABASE_PATH = 'data.db'


def check_internet(url):
    try:
        response = requests.head(url, timeout=1)
        status_code = response.status_code
        if status_code == 200:
            return True
    except requests.ConnectionError:
        return False


def get_content(url):
    """
    Получение информации о ценах на продукцию
    :param url: 'https://atomicheart.vkplay.ru/'
    :return: словарь {"наименование продукта" : цена, "наименование продукта" : цена, ...}
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension",
                                    False)  # убираем сообщения о том, что браузером управляют автоматически
    options.add_experimental_option("excludeSwitches", [
        "enable-automation"])  # убираем сообщения о том, что браузером управляют автоматически
    options.add_argument(f"user-agent={useragent}")  # задаем User Agent
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')  # запускаем вебдрайвер в фоновом режиме !!!

    with webdriver.Chrome(options=options) as browser:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

    product_names = []
    for product_name in soup.find_all('div', class_='pack-purchase-card__header'):
        product_names.append(product_name.get_text())

    all_price = []
    for item in soup.find_all('div', class_='button__price'):
        price = item.find('span', class_='price').text.split()
        price = int(price[0])
        all_price.append(price)

    return dict(zip(product_names, all_price))


def now_time():
    """Получение текущего времени"""
    return datetime.now().strftime("%d-%m-%Y %H:%M")


def get_last_price_from_db():
    """Получаем последние цены на продукцию из БД"""
    with sqlite3.connect(DATABASE_PATH) as connect:
        cursor = connect.cursor()
        query = "SELECT name, price, MAX(date) FROM product_price GROUP BY name"
        cursor.execute(query)
        return cursor.fetchall()


def get_last_time_access_site():
    """Получаем время последнего обращения к сайту (в формате datatime)"""

    with sqlite3.connect(DATABASE_PATH) as connect:
        cursor = connect.cursor()
        query = "SELECT MAX(date) FROM time_access_site"
        cursor.execute(query)
        date = cursor.fetchone()[0]
        if date is not None:
            # date = cursor.fetchone()[0]
            return datetime.strptime(date, '%d-%m-%Y %H:%M')
        return datetime(1977, 1, 25, 23, 10)


def insert_info_db(prices_dict: dict):
    """В случае изменения цен, вставляем данные с новыми ценами в БД"""
    time = now_time()
    # вставляем время последнего обращения в табличку БД 'time_access_site'
    with sqlite3.connect(DATABASE_PATH) as connect:
        cursor = connect.cursor()
        param = (time,)
        query = "INSERT INTO time_access_site ('date') VALUES (?)"
        cursor.execute(query, param)

    # выбираем из БД последние цены на продукцию
    last_data = get_last_price_from_db()

    last_data_dict = {}
    for item in last_data:
        last_data_dict[item[0]] = item[1]

    notify = ''
    with sqlite3.connect(DATABASE_PATH) as connect:
        for prod_name, new_price in prices_dict.items():
            if last_data_dict == {}:
                old_price = 0
            else:
                old_price = last_data_dict[prod_name]
            if new_price != old_price:
                cursor = connect.cursor()
                param = (prod_name, new_price, time)
                query = "INSERT INTO product_price ('name', 'price', 'date') VALUES (?, ?, ?)"
                cursor.execute(query, param)
                if new_price > old_price:
                    notify += f'{new_price} р. "{prod_name}" - цена УВЕЛИЧИЛАСЬ, ' \
                              f'(стало дороже на {new_price - old_price} руб.)\n'
                elif new_price < old_price:
                    notify += f'{new_price} р. "{prod_name}" - цена СНИЗИЛАСЬ, ' \
                              f'(стало дешевле на {old_price - new_price} руб.)\n'
            else:
                notify += f'{new_price}р. "{prod_name}" - старая цена.\n'

        print(notify)
        show_notify(notify, duration='long')
