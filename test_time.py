# from datetime import datetime, timedelta
# from functions import get_last_time_access_site
#
# last_access_site = get_last_time_access_site()
# print(type(last_access_site), last_access_site)
#
# now_time = datetime.now()
# print(type(now_time), now_time)
#
# delta = last_access_site + timedelta(days=1)
# print(type(delta), delta)
#
# if now_time > delta:
#     print('время запустить программу')
# else:
#     time_wait = delta - now_time
#     print(f'надо подождать еще {time_wait}')
#     how_sec = time_wait.total_seconds()
#     print(f'в секундах это: {how_sec}')

from time import sleep

_TIME = 10  # Just for example, remove this

while _TIME > 0:
    m, s = divmod(_TIME, 60)
    h, m = divmod(m, 60)
    print(f"\r{int(h)}".rjust(3,'0'), f"{int(m)}".rjust(2,'0'),
          f"{s}".rjust(2,'0'), sep=':', end='')
    _TIME -= 1
    sleep(1)
else:
    print("\r  Completed !  ")
