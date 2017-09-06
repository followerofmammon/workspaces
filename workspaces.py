#!/usr/bin/python
import os
import argparse
from termcolor import colored

import workspace
import configuration
import workspacetomainrepo


def choose_strings_colors(strings):
    strings = list(strings)
    strings.sort()
    colors = ["red", "green", "blue", "magenta", "cyan", "yellow", "grey"] * 10
    string_to_color = dict(zip(strings, colors))
    return string_to_color


def print_workspaces_with_main_repos(workspaces):
    repos = list(set([_workspace.repo for _workspace in workspaces]))
    repos_colors = choose_strings_colors(repos)
    workspaces_colors = choose_strings_colors([_workspace.name for _workspace in workspaces])
    for repo in repos:
        colored_repo = colored(repo, repos_colors[repo])
        print colored_repo + ":"
        relevant_workspaces = [_workspace for _workspace in workspaces if _workspace.repo == repo]
        relevant_workspaces.sort()
        for _workspace in relevant_workspaces:
            workspace_name = _workspace.name
            workspace_path = os.path.abspath(os.path.join(configuration.root_dir, _workspace.name))
            curdir = os.path.abspath(os.path.curdir)
            in_workspace = (curdir + os.path.sep).startswith(workspace_path + os.path.sep)
            is_branch_checked_out = not _workspace.branch.startswith("(HEAD detached ")
            if is_branch_checked_out:
                workspace_name_output = colored(_workspace.name, attrs=['bold'],
                                        color=workspaces_colors[_workspace.name])
            else:
                workspace_name_output = _workspace.name
            workspace_output = ""
            workspace_output += "[%(workspace_name)s]" % dict(workspace_name=workspace_name_output)
            if _workspace.tracked_files_modified:
                workspace_output += "[M]"
            if _workspace.untracked_files_modified:
                workspace_output += "[??]"
            workspace_output += "\n"
            if is_branch_checked_out:
                branch_output = colored(_workspace.branch, attrs=['bold'],
                                        color=workspaces_colors[_workspace.name])
            else:
                branch_output = _workspace.branch
            workspace_output += "branch: %s\n" % (branch_output,)
            head_description = _workspace.get_head_description()
            head = ''.join(["" + description for description in head_description.splitlines()])
            workspace_output += head

            prefix = "---->\t" if in_workspace else "\t"
            workspace_lines = workspace_output.splitlines()
            workspace_lines = ["%s%s" % (prefix, line) for line in workspace_lines]
            workspace_output = "\n".join(workspace_lines)
            is_last = _workspace.name == relevant_workspaces[-1] and (repo == repos[-1])
            if not is_last:
                workspace_output += "\n"
            print workspace_output


def print_workspaces_without_main_repos(workspaces):
    workspaces = [_workspace.name for _workspace in workspaces if _workspace.name is None]
    global configuration
    if configuration.ignore_unknown:
        return
    if workspaces:
        workspaces_names = [_workspace.name for _workspace in workspaces]
        print "Did not find a main repository for the following workspaces:\n\t",
        print "\n\t".join(workspaces_names)
        print ("To set a specific main repository for a workspace, you can either: \n"
               "* add a '.workspaces.yml' inside the workspace dir, and add the line "
               "'main_repo: <your_repo_dirname>' to it.")
        print ("* Add a workspace_to_main_repo dictionary in /etc/workspaces.yml that maps a workspace "
               "name to the name of its main repository name")
        print
        print ("To ignore a dir in the workspace root dir (to not see this message), set ignore_unknown "
               " to true in %s." % (configuration.WORKSPACES_CONFIG_FILENAME,))
        print
        print "If the dir '%s' is not your workspace root dir, you can either:" % (configuration.root_dir,)


def print_workspaces(workspaces):
    print_workspaces_with_main_repos(workspaces)
    print_workspaces_without_main_repos(workspaces)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="describe",
                        choices=["list", "describe", "getrootdir"])
    return parser.parse_args()


def get_workspaces_dirpaths(rootdir):
    dirs = [dirname for dirname in os.listdir(rootdir) if os.path.isdir(os.path.join(rootdir, dirname))]
    return [_dir for _dir in dirs if _dir not in configuration.dirs_to_ignore]


def list_items_for_auto_copmletion():
    workspaces = get_workspaces_dirpaths(configuration.root_dir)
    for workspace in workspaces:
        print workspace
        workspace_path = os.path.join(configuration.root_dir, workspace)
        main_repo = workspacetomainrepo.get_main_repo(workspace_path)
        if main_repo is not None:
            main_repo_path = os.path.join(workspace_path, main_repo)
            if os.path.exists(main_repo_path):
                print os.path.join(workspace, main_repo)


def describe_workspaces():
    workspaces_dirs = get_workspaces_dirpaths(configuration.root_dir)
    workspaces = [workspace.Workspace(_workspace) for _workspace in workspaces_dirs]
    print_workspaces(workspaces)


def main():
    args = parse_args()
    if args.command == 'list':
        list_items_for_auto_copmletion()
    elif args.command == 'describe':
        describe_workspaces()
    elif args.command == 'getrootdir':
        print configuration.read_configuration

if __name__ == "__main__":
    main()
