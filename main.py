from time import sleep


from functions import check_internet, get_content, insert_info_db, show_notify, get_last_time_access_site
from datetime import datetime, timedelta, time


check_url = 'https://www.google.com/'
donor_url = 'https://atomicheart.vkplay.ru/'


def main():
    while check_internet(check_url) is False:
        print('... нет интернета ... ждем немного ... ')
        sleep(5)
    print('... начат сбор информации на ATOMIC HEART ...')
    show_notify('... начат сбор информации на ATOMIC HEART ...', duration='short')
    prices = get_content(donor_url)
    insert_info_db(prices)
    print('... сбор закончен ...')


def time_start_program():
    # получаем время последнего обращения к сайту по МСК
    last_access_site = get_last_time_access_site() - timedelta(hours=4)
    # истечение суток когда обращались к сайту последний раз
    end_of_day_last_access = datetime.combine(last_access_site, time(23, 59, 59))
    # получаем текущее время по МСК
    now_time = datetime.now() - timedelta(hours=4)
    # print(last_access_site, 'время последнего обращения к сайту')
    # print(end_of_day_last_access, 'время окончания постановки на паузу')

    if now_time.day > end_of_day_last_access.day:
        # print('время запустить программу')
        return True
    else:
        # узнаем время ожидания
        time_wait = end_of_day_last_access - now_time
        return time_wait


if __name__ == '__main__':
    while True:
        start_info = time_start_program()
        if start_info is True:
            main()
        else:
            # запускаем таймер обратного отсчета в терминале
            _TIME = start_info.seconds
            while _TIME > 0:
                m, s = divmod(_TIME, 60)
                h, m = divmod(m, 60)
                print(f"\rДо следующего парсинга: {int(h)}".rjust(3, '0'), f"{int(m)}".rjust(2, '0'),
                      f"{s}".rjust(2, '0'), sep=':', end='')
                _TIME -= 1
                sleep(1)

