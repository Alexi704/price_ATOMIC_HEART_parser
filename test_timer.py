from time import sleep

_TIME = 10  # Just for example, remove this

while _TIME > 0:
    m, s = divmod(_TIME, 60)
    h, m = divmod(m, 60)
    print(f"\rДо следующего запуска: {int(h)}".rjust(3,'0'), f"{int(m)}".rjust(2,'0'),
          f"{s}".rjust(2,'0'), sep=':', end='')
    _TIME -= 1
    sleep(1)
else:
    print("\r  Completed !!!                                                ")
    sleep(5)
