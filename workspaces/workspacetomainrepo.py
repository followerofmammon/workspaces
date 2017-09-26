import os
import yaml

import printwarning
import configuration


def get_main_repo(workspace_path):
    global configuration
    config_filename = os.path.join(workspace_path, configuration.REPO_CONFIG_FILENAME)
    if os.path.exists(config_filename) and not os.path.isdir(config_filename):
        try:
            with open(config_filename) as config:
                config = yaml.load(config)
        except:
            printwarning.printwarning("failed to parse %(filename)s as yaml" % dict(filename=config_filename))
            return None
        if 'main_repo' not in config:
            printwarning.printwarning("No 'main_repo' field in %(filename)s" % dict(filename=config_filename))
            return None
        repo_path = os.path.join(workspace_path, config['main_repo'])
        if os.path.exists(repo_path) and os.path.isdir(repo_path):
            return os.path.basename(repo_path)
        else:
            printwarning.printwarning("Main repo as specified in %(filename)s does not exist" %
                                      (dict(filename=config_filename)))

    workspace_to_main_repo = configuration.workspace_to_main_repo
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
                printwarning.parintwarning("Warning: Repo dir %s does not exist in workspace %s as configured "
                                           "in %s" % (repo, workspace_name,
                                                      configuration.WORKSPACES_CONFIG_FILENAME))
                return None
    else:
        printwarning.printwarning("workspace_to_main_repo in the %s should be a dictionary of workspaces to "
                                  "main repository dir names" % (configuration.WORKSPACES_CONFIG_FILENAME,))

    for repo in configuration.DEFAULT_REPOSITORY_TO_SHOW_BY_PRIORITY:
        repo_path = os.path.join(workspace_path, repo)
        if os.path.exists(repo_path) and os.path.isdir(repo_path):
            return repo
    return None
