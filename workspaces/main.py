#!/usr/bin/python
import sys
import argparse

import configuration
from commands import autocompletionlist
from commands import describeoneworkspace
from commands import describeallworkspaces


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="describe",
                        choices=["list",
                                 "describe-one-workspace",
                                 "describe-all-workspaces",
                                 "getrootdir"])
    args = sys.argv[1:2]
    inner_args = sys.argv[2:]
    return parser.parse_args(args), inner_args


def main():
    args, inner_args = parse_args()
    if args.command == 'list':
        autocompletionlist.list_items_for_auto_copmletion()
    elif args.command == 'describe-all-workspaces':
        describeallworkspaces.describeallworkspaces()
    elif args.command == 'describe-one-workspace':
        describeoneworkspace.describeoneworkspace(inner_args)
    elif args.command == 'getrootdir':
        print configuration.root_dir

if __name__ == "__main__":
    main()
