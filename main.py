from time import sleep
from functions import check_internet, get_content, insert_info_db, show_notify
import schedule


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
    sleep(5)


if __name__ == '__main__':
    schedule.every().day.at('12:21').do(main)
    while True:
        schedule.run_pending()
