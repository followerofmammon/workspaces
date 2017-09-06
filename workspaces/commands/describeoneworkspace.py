import argparse

import workspace
import workspace_shelloutput


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath")
    return parser.parse_args(args)


def describeoneworkspace(args):
    args = parse_args(args)
    _workspace = workspace.Workspace.factory_from_path(args.dirpath)
    workspaces = [_workspace]
    workspace_shelloutput.print_workspaces_with_main_repos(workspaces)
    workspace_shelloutput.print_workspaces_without_main_repos(workspaces)
