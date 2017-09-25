#!/usr/bin/python
import sys
import argparse

import configuration
from commands import autocompletionlist
from commands import describeoneworkspace
from explicit_commands import interactive
from commands import describeallworkspaces
from explicit_commands import describeindetail


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("command",
                        choices=[
                                 "describeoneworkspace",
                                 "describeallworkspaces",
                                 "getrootdir",
                                 "explicitcommand",
                                 "autocompletionlist",
                                 ])
    args = sys.argv[1:2]
    inner_args = sys.argv[2:]
    return parser.parse_args(args), inner_args


def explicit_command(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=str, nargs="?")
    parser.add_argument("-l", "--list", default=False, action="store_true")
    parser.add_argument("-i", "--interactive", default=False, action="store_true")
    return parser.parse_args(args)

def main():
    args, inner_args = parse_args()
    if args.command == 'autocompletionlist':
        autocompletionlist.list_items_for_auto_copmletion()
    elif args.command == 'describeallworkspaces':
        describeallworkspaces.describeallworkspaces()
    elif args.command == 'describeoneworkspace':
        describeoneworkspace.describeoneworkspace(inner_args)
    elif args.command == 'getrootdir':
        print configuration.root_dir
    elif args.command == 'explicitcommand':
        args = explicit_command(inner_args)
        if args.workspace is None:
            if args.list:
                describeindetail.describeindetail()
            elif args.interactive:
                interactive.interactive()
        else:
            describeindetail.describeindetail()


if __name__ == "__main__":
    main()
