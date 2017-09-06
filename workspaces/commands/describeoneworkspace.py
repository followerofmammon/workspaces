import argparse

import workspace
import workspace_shelloutput


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath")
    parser.add_argument("-l", "--list", action="store_true", default=False)
    return parser.parse_args(args)


def describeoneworkspace(args):
    args = parse_args(args)
    _workspace = workspace.Workspace.factory_from_path(args.dirpath)
    workspaces = [_workspace]
    workspace_shelloutput.print_workspaces_with_main_repos(workspaces, is_detailed=args.list)
    workspace_shelloutput.print_workspaces_without_main_repos(workspaces)
