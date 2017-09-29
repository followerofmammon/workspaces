import os
import yaml

import printwarning
import configuration


def get_main_repos(workspace_path):
    global configuration
    config_filename = os.path.join(workspace_path, configuration.REPO_CONFIG_FILENAME)
    if os.path.exists(config_filename) and not os.path.isdir(config_filename):
        try:
            with open(config_filename) as config:
                config = yaml.load(config)
        except:
            printwarning.printwarning("failed to parse %(filename)s as yaml" % dict(filename=config_filename))
            return list()

        main_repos = None
        if 'main_repo' in config:
            main_repos = config['main_repo']
        elif 'main_repos' in config:
            main_repos = config['main_repos']

        if main_repos is not None:
            if isinstance(main_repos, str):
                main_repos = [main_repos]
            return _filter_existing_repos(workspace_path, main_repos)

    main_repos = configuration.DEFAULT_REPOSITORY_TO_SHOW_BY_PRIORITY
    workspace_to_main_repos = dict()
    if (hasattr(configuration, 'workspace_to_main_repos') and
        isinstance(configuration.workspace_to_main_repos, dict)):
        workspace_to_main_repos = configuration.workspace_to_main_repos
    elif (hasattr(configuration, 'workspace_to_main_repo') and
        isinstance(configuration.workspace_to_main_repo, dict)):
        workspace_to_main_repos = configuration.workspace_to_main_repo

    workspace_name = os.path.basename(workspace_path)
    if workspace_name in workspace_to_main_repos:
        if isinstance(workspace_to_main_repos[workspace_name], list):
            main_repos = workspace_to_main_repos[workspace_name]
        elif isinstance(workspace_to_main_repos[workspace_name], str):
            main_repos = [workspace_to_main_repos[workspace_name]]

    return _filter_existing_repos(workspace_path, main_repos)


def _filter_existing_repos(workspace_path, repo_names):
    existing = list()
    for repo_name in repo_names:
        repo_path = os.path.join(workspace_path, repo_name)
        if os.path.exists(repo_path) and os.path.isdir(repo_path):
            existing.append(repo_name)
    return existing
