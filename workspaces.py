#!/usr/bin/python
import os
import sys
import yaml
import argparse
import tabulate
import subprocess
from termcolor import colored


DEFAULT_WORKSPACES_ROOT_DIR = os.path.join(os.path.expanduser("~"), "work", "code")
DEFAULT_REPOSITORY_TO_SHOW_BY_PRIORITY = ["strato-storage", "monkey"]
REPO_CONFIG_FILENAME = ".workspaces.yml"
WORKSPACES_CONFIG_FILENAME = "/etc/workspaces.yml"


configuration = dict()


def print_warning(warning):
    print "*************"
    print "Warning:"
    print "\t", warning
    print "*************"
    print

def get_main_repo(workspace_path):
    global configuration
    config_filename = os.path.join(workspace_path, REPO_CONFIG_FILENAME)
    if os.path.exists(config_filename) and not os.path.isdir(config_filename):
        try:
            with open(config_filename) as config:
                config = yaml.load(config)
        except:
            print_warning("failed to parse %(filename)s as yaml" % dict(filename=config_filename))
            return None
        if 'main_repo' in config:
            main_repo = config['main_repo']
        else:
            print_warning("No 'main_repo' field in %(filename)s" % dict(filename=config_filename))
            return None
        repo_path = os.path.join(workspace_path, config['main_repo'])
        if os.path.exists(repo_path) and os.path.isdir(repo_path):
            return os.path.basename(repo_path)
        else:
            print_warning("Main repo as specified in %(filename)s does not exist" % (
                  dict(filename=config_filename)))

    workspace_to_main_repo = configuration.get('workspace_to_main_repo', dict())
    if isinstance(workspace_to_main_repo, dict):
        workspace_name = os.path.basename(workspace_path)
        if workspace_name in workspace_to_main_repo:
            repo = workspace_to_main_repo[workspace_name]
        elif workspace_path in workspace_to_main_repo:
            repo = workspace_to_main_repo[workspace_path]
        else:
            repo = None
        if repo is not None:
            repo_path = os.path.join(workspace_path, repo)
            if os.path.exists(repo_path) and os.path.isdir(repo_path):
                return repo
            else:
                print_warning("Warning: Repo dir %s does not exist in workspace %s as configured in %s" % (
                              repo, workspace_name, WORKSPACES_CONFIG_FILENAME))
                return None
    else:
        print_warning("workspace_to_main_repo in the %s should be a dictionary of workspaces to "
                      "main repository dir names" % (WORKSPACES_CONFIG_FILENAME,))

    for repo in DEFAULT_REPOSITORY_TO_SHOW_BY_PRIORITY:
        repo_path = os.path.join(workspace_path, repo)
        if os.path.exists(repo_path) and os.path.isdir(repo_path):
            return repo
    return None


def get_workspace_description(workspaces_root_dir, workspace_dirname):
    workspace_path = os.path.join(workspaces_root_dir, workspace_dirname)
    repo = get_main_repo(workspace_path)
    if repo is None:
        return None

    repo_path = os.path.join(workspace_path, repo)
    git_dir = os.path.join(repo_path, ".git")
    cmd = ["git", "--work-tree", repo_path, "--git-dir", git_dir, "show", "--quiet", "--oneline"]
    try:
        head_description = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        print_warning("%s is not a git repository" % (repo_path))
        return None
    head_description = "\n".join(head_description.splitlines()[:5])

    cmd = ["git", "--work-tree", repo_path, "--git-dir", git_dir, "branch"]
    branch = subprocess.check_output(cmd)
    branchLine = [line.strip("\t *") for line in branch.splitlines() if line.startswith("* ")]
    if branchLine:
        branch = branchLine[0]
    else:
        branch = "No branch"

    cmd = ["git", "--work-tree", repo_path, "--git-dir", git_dir, "status", "--porcelain"]
    status = subprocess.check_output(cmd)
    status = status.splitlines()
    untracked_files_modified = bool([line for line in status if line.startswith("??")])
    tracked_files_modified = bool([line for line in status if not line.startswith("??")])

    return dict(repo=repo, branch=branch, head_description=head_description,
                untracked_files_modified=untracked_files_modified,
                tracked_files_modified=tracked_files_modified)


def choose_strings_colors(strings):
    strings = list(strings)
    strings.sort()
    colors = ["red", "green", "blue", "magenta", "cyan", "yellow", "grey"] * 10
    string_to_color = dict(zip(strings, colors))
    return string_to_color


def print_workspaces_with_main_repos(workspaces, rootdir):
    repos = list(set([workspace['repo'] for workspace in workspaces.values()]))
    repos_colors = choose_strings_colors(repos)
    workspaces_colors = choose_strings_colors(workspaces.keys())
    repos = list(set([workspace['repo'] for workspace in workspaces.itervalues()]))
    for repo in repos:
        colored_repo = colored(repo, repos_colors[repo])
        print colored_repo + ":"
        relevant_workspaces = [workspace_name for workspace_name in workspaces
                               if workspaces[workspace_name]['repo'] == repo]
        relevant_workspaces.sort()
        for workspace_name in relevant_workspaces:
            workspace_path = os.path.abspath(os.path.join(rootdir, workspace_name))
            curdir = os.path.abspath(os.path.curdir)
            in_workspace = (curdir + os.path.sep).startswith(workspace_path + os.path.sep)
            workspace = workspaces[workspace_name]
            is_branch_checked_out = not workspace['branch'].startswith("(HEAD detached ")
            if is_branch_checked_out:
                workspace_name_output = colored(workspace_name, attrs=['bold'],
                                        color=workspaces_colors[workspace_name])
            else:
                workspace_name_output = workspace_name
            workspace_output = ""
            workspace_output += "[%(workspace_name)s]" % dict(workspace_name=workspace_name_output)
            if workspace['tracked_files_modified']:
                workspace_output += "[M]"
            if workspace['untracked_files_modified']:
                workspace_output += "[??]"
            workspace_output += "\n"
            if is_branch_checked_out:
                branch_output = colored(workspace['branch'], attrs=['bold'],
                                        color=workspaces_colors[workspace_name])
            else:
                branch_output = workspace['branch']
            workspace_output += "branch: %s\n" % (branch_output,)
            head = ''.join(["" + description for description in workspace['head_description'].splitlines()])
            workspace_output += head

            prefix = "---->\t" if in_workspace else "\t"
            workspace_lines = workspace_output.splitlines()
            workspace_lines = ["%s%s" % (prefix, line) for line in workspace_lines]
            workspace_output = "\n".join(workspace_lines)
            is_last = workspace_name == relevant_workspaces[-1] and (repo == repos[-1])
            if not is_last:
                workspace_output += "\n"
            print workspace_output


def print_workspaces_without_main_repos(workspaces, rootdir):
    global configuration
    if configuration.get('ignore_unknown', False):
        return
    if workspaces:
        print "Did not find a main repository for the following workspaces:\n\t",
        print "\n\t".join(workspaces)
        print ("To set a specific main repository for a workspace, you can either: \n"
               "* add a '.workspaces.yml' inside the workspace dir, and add the line "
               "'main_repo: <your_repo_dirname>' to it.")
        print ("* Add a workspace_to_main_repo dictionary in /etc/workspaces.yml that maps a workspace "
               "name to the name of its main repository name")
        print
        print ("To ignore a dir in the workspace root dir (to not see this message), set ignore_unknown "
               " to true in %s." % (WORKSPACES_CONFIG_FILENAME,))
        print
        print "If the dir '%s' is not your workspace root dir, you can either:" % (rootdir,)
        print_workspace_root_dir_options()

def print_workspaces(workspaces, workspaces_root_dir):
    workspaces_with_main_repos = {workspace_name: workspace for (workspace_name, workspace)
        in workspaces.iteritems() if workspace is not None}
    print_workspaces_with_main_repos(workspaces_with_main_repos, workspaces_root_dir)
    workspaces_without_main_repos = [workspace_name for workspace_name in workspaces
                                     if workspace_name not in workspaces_with_main_repos]
    print_workspaces_without_main_repos(workspaces_without_main_repos, workspaces_root_dir)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="describe",
                        choices=["list", "describe", "getrootdir"])
    return parser.parse_args()


def get_workspaces(rootdir):
    global configuration
    dirs = [dirname for dirname in os.listdir(rootdir) if os.path.isdir(os.path.join(rootdir, dirname))]
    dirs_to_ignore = configuration.get('dirs_to_ignore', list())
    if isinstance(dirs_to_ignore, str):
        dirs_to_ignore = [dirs_to_ignore]
    elif not isinstance(dirs_to_ignore, list):
        print_warning("Badly formed 'dirs_to_ignore' in configuration file %" % (WORKSPACES_CONFIG_FILENAME,))
        dirs_to_ignore = list()
    return [_dir for _dir in dirs if _dir not in dirs_to_ignore]


def read_configuration():
    global configuration
    with open(WORKSPACES_CONFIG_FILENAME) as config_file:
        try:
            configuration = yaml.load(config_file)
        except:
            print "Failed to parse config filename ", config_filename

def get_root_dir_from_config_file():
    global configuration
    if "root_dir" not in configuration:
        print "Warning: 'root_dir' is not configured in config file ", config_filename
        return None
    root_dir = configuration['root_dir']
    if root_dir.startswith("~/"):
        inner_part = root_dir[2:]
        root_dir = os.path.join(os.path.expanduser("~"), inner_part)
    return root_dir


def print_workspace_root_dir_options():
        print "* set the WORKSPACES_ROOT_DIR env var"
        print "* Add root_dir: <your_root_dir> to %s" % (WORKSPACES_CONFIG_FILENAME,)

def get_workspaces_root_dir(configuration):
    if "WORKSPACES_ROOT_DIR" in os.environ:
        root_dir = os.environ["WORKSPACES_ROOT_DIR"]
    elif os.path.exists(WORKSPACES_CONFIG_FILENAME):
        root_dir = get_root_dir_from_config_file()
    else:
         root_dir = DEFAULT_WORKSPACES_ROOT_DIR
    if not os.path.exists(root_dir):
        print ("It appears that the current configured workspaces rootdir '%s' does not exist. To "
               "configure the right root dir, you can either:" % (root_dir,))
        print_workspace_root_dir_options()
        print "Or, you could create this root dir :)"
        sys.exit(1)
    return root_dir


def main():
    args = parse_args()
    read_configuration()
    workspaces_root_dir = get_workspaces_root_dir(configuration)

    if args.command == 'list':
        workspaces = get_workspaces(workspaces_root_dir)
        for workspace in workspaces:
            print workspace
            workspace_path = os.path.join(workspaces_root_dir, workspace)
            main_repo = get_main_repo(workspace_path)
            if main_repo is not None:
                main_repo_path = os.path.join(workspace_path, main_repo)
                if os.path.exists(main_repo_path):
                    print os.path.join(workspace, main_repo)
    elif args.command == 'describe':
        workspaces = get_workspaces(workspaces_root_dir)
        descriptions = dict()
        for workspace in workspaces:
            description = get_workspace_description(workspaces_root_dir, workspace)
            descriptions[workspace] = description
        print_workspaces(descriptions, workspaces_root_dir)
    elif args.command == 'getrootdir':
        print workspaces_root_dir

if __name__ == "__main__":
    main()
