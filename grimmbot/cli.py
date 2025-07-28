import argparse

from .echo_bot import EchoBot
from .reverse_bot import ReverseBot
from .uppercase_bot import UppercaseBot
from .coordinator import Coordinator

BOT_MAP = {
    'echo': EchoBot,
    'reverse': ReverseBot,
    'upper': UppercaseBot,
}

def main():
    parser = argparse.ArgumentParser(description='Run a chain of simple bots.')
    parser.add_argument('message', help='Message to process')
    parser.add_argument('-b', '--bots', nargs='+', choices=list(BOT_MAP.keys()), default=['echo'],
                        help='Bots to apply in sequence')
    args = parser.parse_args()

    bots = [BOT_MAP[name]() for name in args.bots]
    coordinator = Coordinator(bots)
    result = coordinator.process(args.message)
    print(result)

if __name__ == '__main__':
    main()
