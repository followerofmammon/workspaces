import os
import termcolor

import configuration


def print_workspaces_with_main_repos(workspaces):
    main_repos = list(set([workspace.main_repo for workspace in workspaces]))
    repo_colors = _choose_strings_colors(main_repos)
    workspaces_colors = _choose_strings_colors([workspace.name for workspace in workspaces])
    main_repo_output = [_get_main_repo_output(main_repo, workspaces, repo_colors, workspaces_colors)
                        for main_repo in main_repos]
    print "\n\n".join(main_repo_output)


def print_workspaces_without_main_repos(workspaces):
    workspaces = [workspace.name for workspace in workspaces if workspace.name is None]
    global configuration
    if configuration.ignore_unknown:
        return
    if workspaces:
        workspaces_names = [workspace.name for workspace in workspaces]
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


def _choose_strings_colors(strings):
    strings = list(strings)
    strings.sort()
    colors = ["red", "green", "blue", "magenta", "cyan", "yellow", "grey"] * 10
    string_to_color = dict(zip(strings, colors))
    return string_to_color


def _get_main_repo_output(main_repo, workspaces, repo_colors, workspaces_colors):
    colored_repo = termcolor.colored(main_repo, repo_colors[main_repo])
    output = colored_repo + ":\n"
    relevant_workspaces = [workspace for workspace in workspaces if workspace.main_repo == main_repo]
    relevant_workspaces.sort()
    workspaces_output = [_get_workspace_output(workspace, main_repo, workspaces_colors)
                         for workspace in relevant_workspaces]
    output += "\n\n".join(workspaces_output)
    return output


def _get_workspace_output(workspace, main_repo, workspaces_colors):
    formatted_name = workspace.name
    if workspace.is_branch_checked_out():
        formatted_name = termcolor.colored(formatted_name, attrs=['bold'],
                                           color=workspaces_colors[workspace.name])
    header_line = "[%(name)s]" % dict(name=formatted_name)
    if workspace.tracked_files_modified:
        header_line += "[M]"
    if workspace.untracked_files_modified:
        header_line += "[??]"

    formatted_branch = workspace.branch
    if workspace.is_branch_checked_out():
        formatted_branch = termcolor.colored(formatted_branch, attrs=['bold'],
                                             color=workspaces_colors[workspace.name])
    branch_line = "branch: %s" % (formatted_branch,)

    head_description = "\n".join(workspace.head_description.splitlines()[:5])
    commit_line = ''.join(["" + description for description in head_description.splitlines()])

    lines = [header_line, branch_line, commit_line]
    prefix = "---->\t" if _is_workdir_inside_workspace(workspace) else "\t"
    return '\n'.join(["%s%s" % (prefix, line) for line in lines])


def _is_workdir_inside_workspace(workspace):
    curdir = os.path.abspath(os.path.curdir)
    return (curdir + os.path.sep).startswith(workspace.path + os.path.sep)
