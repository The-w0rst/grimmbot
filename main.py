from bots.bot1.bot1 import Bot1
from bots.bot2.bot2 import Bot2
from bots.bot3.bot3 import Bot3


def main():
    b1 = Bot1()
    b2 = Bot2()
    b3 = Bot3()

    print('Bot1 says:', b1.respond('Hello there!'))
    print('Bot2 reports time:', b2.get_time())
    print('Bot3 tells a joke:', b3.tell_joke())


if __name__ == '__main__':
    main()
