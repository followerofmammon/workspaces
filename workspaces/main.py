#!/usr/bin/python
import argparse

import configuration
from commands import describe
from commands import autocompletionlist


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="describe",
                        choices=["list", "describe", "getrootdir"])
    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == 'list':
        autocompletionlist.list_items_for_auto_copmletion()
    elif args.command == 'describe':
        describe.describe()
    elif args.command == 'getrootdir':
        print configuration.read_configuration

if __name__ == "__main__":
    main()
