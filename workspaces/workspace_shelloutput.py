import os
import itertools


def prettify_workspaces_tree(workspaces_tree, workspaces, is_detailed=False):
    workspaces_colors = _choose_strings_colors([workspace.name for workspace in workspaces])
    main_repos = list(set(itertools.chain(*[workspace.main_repos for workspace in workspaces])))
    repo_colors = _choose_strings_colors(main_repos)
    for node in workspaces_tree.children(workspaces_tree.root):
        workspace_name = node.data.name
        workspace = [workspace for workspace in workspaces if workspace.name == workspace_name][0]
        node.tag = _get_workspace_output(workspace, workspaces_colors, is_detailed, repo_colors)


def get_workspace_output(workspace):
    workspaces_colors = _choose_strings_colors([workspace.name])
    repo_colors = _choose_strings_colors(workspace.main_repos)
    return _get_workspace_output(workspace, workspaces_colors, False, repo_colors)


def _choose_strings_colors(strings):
    strings = list(strings)
    strings.sort()
    colors = ["red", "green", "blue", "magenta", "yellow", "grey"] * 10
    string_to_color = dict(zip(strings, colors))
    return string_to_color


def _get_workspace_output(workspace, workspaces_colors, is_detailed, repo_colors):
    lines = list()

    # Header line
    color = None
    branch = workspace.branch()
    if branch is not None:
        color = workspaces_colors[workspace.name]
    line = list()
    line.append(("[", None, False))
    line.append((workspace.name, color, workspace.is_branch_checked_out()))
    line.append(("]", None, False))
    lines.append(line)

    prefix = "    "
    # Main repo
    for repo_name, repo in workspace.main_repos.iteritems():
        line = list()
        line.append((prefix + repo_name, repo_colors[repo_name], False))
        line.append((": ", None, False))

        # Branch
        string_part = ""
        branch = repo.branch
        if repo.is_branch_checked_out():
            color = workspaces_colors[workspace.name]
        else:
            color = None
        string_part += branch + " "
        line.append((string_part, color, repo.is_branch_checked_out()))
        string_part = ""
        if repo.tracked_files_modified:
            string_part += "[M]"
        if repo.untracked_files_modified:
            string_part += "[??]"
        line.append((string_part, None, False))
        lines.append(line)

        # Commit line
        head_description = "".join(repo.head_description.splitlines()[:5])
        line = list()
        line.append((prefix + head_description, None, False))
        lines.append(line)

    if is_detailed:
        line = list()
        line.append((prefix + 'Repositories:', None, False))
        lines.append(line)
        entries = workspace.listdir()
        entries_lines = [[(("%s/%s" % (workspace.name, entry,),), None, False)] for entry in entries]
        lines.extend(entries_lines)

    return lines


def _is_workdir_inside_workspace(workspace):
    curdir = os.path.abspath(os.path.curdir)
    return (curdir + os.path.sep).startswith(workspace.path + os.path.sep)
