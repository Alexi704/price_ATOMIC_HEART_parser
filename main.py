from time import sleep
from functions import check_internet, get_content, insert_info_db


check_url = 'http://www.google.com/'
donor_url = 'https://atomicheart.vkplay.ru/'


if __name__ == '__main__':
    while check_internet(check_url) is False:
        # print('... нет интернета ... ждем немного ... ')
        sleep(5)
    prices = get_content(donor_url)
    insert_info_db(prices)
