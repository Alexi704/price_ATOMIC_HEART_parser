from time import sleep
from functions import check_internet, get_content, insert_info_db, show_notify, time_start_program

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


if __name__ == '__main__':
    while True:
        start_info = time_start_program()
        print(start_info, 'это старт инфо')
        if start_info is True:
            main()
        else:
            # запускаем таймер обратного отсчета в терминале
            _TIME = start_info.seconds
            m, s = divmod(_TIME, 60)
            h, m = divmod(m, 60)
            info_time_left = f'До следующего парсинга\nAtomic Heart: ' \
                             f'{str(int(h)).rjust(2, "0")}:{str(int(m)).rjust(2, "0")}:{str(int(s)).rjust(2, "0")}'
            # выводим в уведомления винды сколько нам осталось ждать до следующего парсинга
            # show_notify(info_time_left, duration='short')
            # вывод в терминале информации сколько нам осталось ждать до следующего парсинга
            while _TIME > 0:
                m, s = divmod(_TIME, 60)
                h, m = divmod(m, 60)
                print(f"\rДо следующего парсинга: {int(h)}".rjust(3, '0'), f"{int(m)}".rjust(2, '0'),
                      f"{s}".rjust(2, '0'), sep=':', end='')
                _TIME -= 1
                sleep(1)
