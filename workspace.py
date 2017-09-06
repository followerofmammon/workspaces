import os
import subprocess

import printwarning
import configuration
import workspacetomainrepo


class Workspace(object):
    def __init__(self, name):
        self.name = name
        self._main_repo = None
        self.workspace_path = os.path.join(configuration.root_dir, name)
        self.repo = workspacetomainrepo.get_main_repo(self.workspace_path)
        self._git_dir = None
        if self.repo is None:
            return None
        self._read()

    def _read(self):
        self.repo_path = os.path.join(self.workspace_path, self.repo)
        self._git_dir = os.path.join(self.repo_path, ".git")

        cmd = ["git", "--work-tree", self.repo_path, "--git-dir", self._git_dir, "status", "--porcelain"]
        status = subprocess.check_output(cmd)
        status = status.splitlines()
        self.untracked_files_modified = any(line for line in status if line.startswith("??"))
        self.tracked_files_modified = any(line for line in status if not line.startswith("??"))
        self.branch = self._read_branch()

    def get_head_description(self):
        cmd = ["git", "--work-tree", self.repo_path, "--git-dir", self._git_dir, "show", "--quiet",
               "--oneline"]
        try:
            head_description = subprocess.check_output(cmd)
        except subprocess.CalledProcessError:
            printwarning.printwarning("%s is not a git repository" % (self.repo_path))
            return None
        head_description = "\n".join(head_description.splitlines()[:5])
        return head_description

    def _read_branch(self):
        cmd = ["git", "--work-tree", self.repo_path, "--git-dir", self._git_dir, "branch"]
        branch = subprocess.check_output(cmd)
        branchLine = [line.strip("\t *") for line in branch.splitlines() if line.startswith("* ")]
        return branchLine[0] if branchLine else "No branch"
