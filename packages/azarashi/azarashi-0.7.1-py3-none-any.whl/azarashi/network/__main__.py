import argparse
import sys
from . import transmitter
from . import receiver


def main():
    parser = argparse.ArgumentParser('azarashi network util')
    parser.add_argment('-t', '--transmitter', action='store_true', help='transmitter mode')
    parser.add_argment('-r', '--receiver', action='store_true', help='receiver mode')
    args = parser.parse_args()

    if args.transmitter:
        return (transmitter.main())
    elif args.receiver:
        return (receiver.main())
    else:
        print("set an option '-t' or '-r'", file=sys.stderr)
        return 1


if __main__ == '__main__':
    exit(main())
