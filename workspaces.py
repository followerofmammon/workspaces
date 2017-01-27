#!/usr/bin/python
import os
import yaml
import argparse
import subprocess
from termcolor import colored


DEFAULT_WORKSPACES_ROOT_DIR = os.path.join(os.path.expanduser("~"), "work", "code")
DEFAULT_REPOSITORY_TO_SHOW_BY_PRIORITY = ["strato-storage", "monkey", "rackattack-physical"]
REPO_CONFIG_FILENAME = ".workspaces.yml"


def print_warning(warning):
    print "*************"
    print "Warning:"
    print "\t", warning
    print "*************"
    print

def get_main_repo(workspace_path):
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
    head_description = subprocess.check_output(cmd)
    head_description = "\n".join(["\t" + line for line in head_description.splitlines()[:5]])
    cmd = ["git", "--work-tree", repo_path, "--git-dir", git_dir, "branch"]
    branch = subprocess.check_output(cmd)
    branch = branch.splitlines()[0].strip("\t *")
    return dict(repo=repo, branch=branch, head_description=head_description)


def choose_strings_colors(strings):
    strings = list(strings)
    strings.sort()
    colors = ["red", "green", "blue", "magenta", "cyan", "yellow", "grey"] * 10
    string_to_color = dict(zip(strings, colors))
    return string_to_color


def print_workspaces_with_main_repos(workspaces):
    repos = list(set([workspace['repo'] for workspace in workspaces.values()]))
    repos_colors = choose_strings_colors(repos)
    workspaces_colors = choose_strings_colors(workspaces.keys())
    repos = set([workspace['repo'] for workspace in workspaces.itervalues()])
    for repo in repos:
        relevant_workspaces = [workspace_name for workspace_name in workspaces
                               if workspaces[workspace_name]['repo'] == repo]
        for workspace_name in relevant_workspaces:
            workspace = workspaces[workspace_name]
            colored_repo = colored(repo, repos_colors[repo])
            bold_workspace = colored(workspace_name, attrs=['bold'],
                                     color=workspaces_colors[workspace_name])
            print "%(repo)s [%(workspace_name)s]" % dict(workspace_name=bold_workspace,
                                                         repo=colored_repo)
            print "\tbranch: %(branch)s" % workspace
            print workspace['head_description']
            print


def print_workspaces_without_main_repos(workspaces):
    print "Did not find a main repository for the following workspaces:\n\t",
    print "\n\t".join(workspaces)

def print_workspaces(workspaces, colors):
    workspaces_with_main_repos = {workspace_name: workspace for (workspace_name, workspace)
        in workspaces.iteritems() if workspace is not None}
    print_workspaces_with_main_repos(workspaces_with_main_repos)
    workspaces_without_main_repos = [workspace_name for workspace_name in workspaces
                                     if workspace_name not in workspaces_with_main_repos]
    print_workspaces_without_main_repos(workspaces_without_main_repos)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="describe",
                        choices=["list", "describe", "getrootdir"])
    return parser.parse_args()


def get_dirs(rootdir):
    return [dirname for dirname in os.listdir(rootdir) if os.path.isdir(os.path.join(rootdir, dirname))]

def main():
    args = parse_args()
    workspaces_root_dir = os.getenv("WORKSPACES_ROOT_DIR", DEFAULT_WORKSPACES_ROOT_DIR)

    if args.command == 'list':
        workspaces = get_dirs(workspaces_root_dir)
        for workspace in workspaces:
            print workspace
    elif args.command == 'describe':
        workspaces = get_dirs(workspaces_root_dir)
        descriptions = dict()
        for workspace in workspaces:
            description = get_workspace_description(workspaces_root_dir, workspace)
            descriptions[workspace] = description
        print_workspaces(descriptions, workspaces_root_dir)
    elif args.command == 'getrootdir':
        print workspaces_root_dir

if __name__ == "__main__":
    main()
