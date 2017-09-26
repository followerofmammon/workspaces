import os
import subprocess
from dirsync import dirtree

import workspace
import printwarning
import configuration
import workspacetomainrepo


class Workspace(object):
    def __init__(self, name):
        self.path = os.path.join(configuration.root_dir, name)
        self.main_repo = workspacetomainrepo.get_main_repo(self.path)
        self.name = name
        self.untracked_files_modified = None
        self.tracked_files_modified = None
        self.branch = None
        self.head_description = None
        if self.main_repo is not None:
            self._read()

    @staticmethod
    def factory_from_path(_path):
        dirpath = os.path.join(configuration.root_dir, _path)
        if not os.path.isdir(dirpath):
            raise ValueError(dirpath, "not a directory")
        workspace_name = dirpath.split(configuration.root_dir)[1].split(os.path.sep)[1]
        return Workspace(workspace_name)

    def is_branch_checked_out(self):
        if self.main_repo is None:
            return False
        return not self.branch.startswith("(HEAD detached ")

    def listdir(self):
        entries = os.listdir(self.path)
        return sorted(entries)

    def _read(self):
        status = self._git_command("status", "--porcelain")
        status = status.splitlines()
        self.untracked_files_modified = any(line for line in status if line.startswith("??"))
        self.tracked_files_modified = any(line for line in status if not line.startswith("??"))
        self.branch = self._read_branch()
        self.head_description = self._git_command("show", "--quiet", "--oneline")

    def _read_branch(self):
        branch = self._git_command("branch")
        branchLine = [line.strip("\t *") for line in branch.splitlines() if line.startswith("* ")]
        return branchLine[0] if branchLine else "No branch"

    def _git_command(self, *args):
        repo_path = os.path.join(self.path, self.main_repo)
        git_dir = os.path.join(repo_path, ".git")
        args = ["git", "--work-tree", repo_path, "--git-dir", git_dir] + list(args)
        try:
            result = subprocess.check_output(args)
        except subprocess.CalledProcessError:
            printwarning.printwarning("%s is not a git repository" % (repo_path))
            result = None
        return result


def _remove_non_workspace_entries(fstree):
    workspaces_dirs = workspace.list_workspaces_dirs()
    for node in fstree.children(fstree.root):
        entry = node.data
        if entry.name not in workspaces_dirs:
            fstree.remove_node(node.identifier)


def list_workspaces_dirs():
    return [dirname for dirname in os.listdir(configuration.root_dir) if
            os.path.isdir(os.path.join(configuration.root_dir, dirname)) and
            dirname not in configuration.dirs_to_ignore]


def get_workspaces_tree():
    fstree = dirtree.DirTree.factory_from_filesystem(configuration.root_dir,
                                                     max_depth=2,
                                                     dirs_only=True,
                                                     include_hidden=False,
                                                     silent=True)
    _remove_non_workspace_entries(fstree)
    return fstree
