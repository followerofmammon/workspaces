import os

import workspace
import configuration
import workspacetomainrepo


def list_items_for_auto_copmletion():
    workspaces_dirs = workspace.list_workspaces_dirs()
    for workspace_dir in workspaces_dirs:
        print workspace_dir
        workspace_path = os.path.join(configuration.root_dir, workspace_dir)
        main_repo = workspacetomainrepo.get_main_repo(workspace_path)
        if main_repo is not None:
            main_repo_path = os.path.join(workspace_path, main_repo)
            if os.path.exists(main_repo_path):
                print os.path.join(workspace_dir, main_repo)
