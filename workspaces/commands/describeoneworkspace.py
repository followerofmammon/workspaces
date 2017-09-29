import argparse

import workspace
from dirsync import printer
import workspace_shelloutput


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath")
    parser.add_argument("-l", "--list", action="store_true", default=False)
    return parser.parse_args(args)


def describeoneworkspace(args):
    args = parse_args(args)
    _workspace = workspace.Workspace.factory_from_path(args.dirpath)
    lines = workspace_shelloutput.get_workspace_output(_workspace)
    for line in lines:
        for string, color, is_bold in line:
            printer.print_string(string, color, is_bold)
        printer.print_string("\n", None, False)
