#!/bin/bash

function _workspaces_help {
    echo "This tool lists workspaces in a predefined directory, and describes the current git HEAD"
    echo "in the 'main' git repositories, for each workspace."
    echo
    echo "- To list workspaces, run with no args."
    echo
    echo "- To go into workspace dir, run with the dir as the first argument."
    echo
    echo "- To change the workspaces root dir, either:"
    echo "    * set WORKSPACES_ROOT_DIR env var."
    echo "    * set root_dir in the /etc/workspaces.yml configuration file."
    echo
    echo "- To set specific main repositories for a workspace, either:"
    echo "    * add a '.workspaces.yml' inside the workspace dir, and add 'main_repos: [repo_dir1, repo_dir2, ...]' in yaml format."
    echo "    * Add a workspace_to_main_repos dictionary in /etc/workspaces.yml that maps a workspace name to the name of its main repository name."
}

if [[ "$1" == "-h" ]]; then
    _workspaces_help
else
    if [ "$1" == "--help" ]; then
        _workspaces_help
    else
        if [ -n "$1" ]; then
            root_dir="`inner_workspaces_script getrootdir`"
            workspace_dir="$root_dir/$1"
            if [ -d $workspace_dir ]; then
                cd $workspace_dir
                inner_workspaces_script describeoneworkspace $@
            else
                echo Dir $workspace_dir does not exist.
                echo
                _workspaces_help
            fi
        else
            rm /tmp/_workspaces.chosen -rf
            inner_workspaces_script explicitcommand -i
            if [ -f /tmp/_workspaces.chosen ]; then
                cd `cat /tmp/_workspaces.chosen`;
            fi
            if [ $? -ne 0 ]; then
                _workspaces_help
            fi
        fi
    fi
fi
