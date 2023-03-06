from time import sleep
from functions import check_internet, get_content, insert_info_db, show_notify, get_last_time_access_site, \
    time_start_program, timer_wait


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
        if start_info is True:
            main()
        else:
            # запускаем таймер обратного отсчета в терминале
            _TIME = start_info.seconds
            while _TIME > 0:
                timer_wait(_TIME)
