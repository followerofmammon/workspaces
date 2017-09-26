#!/bin/bash

function _workspaces_help {
    echo This tool lists workspaces in a predefined directory, and describes the current git HEAD
    echo in the 'main' git repository, for each workspace.
    echo
    echo - To list workspaces, run with no args.
    echo      * To specify repositories, run with -l.
    echo      * To choose a dir in interactive mode, run with -i.
    echo
    echo - To go into workspace dir, run with the dir as the first argument.
    echo
    echo - To change the workspaces root dir, either:
    echo "    * set WORKSPACES_ROOT_DIR env var."
    echo "    * set root_dir in the /etc/workspaces.yml configuration file."
    echo
    echo - To set a specific main repository for a workspace, either:
    echo "    * add a '.workspaces.yml' inside the workspace dir, and add the line 'main_repo: <your_repo_dirname>' to it."
    echo "    * Add a workspace_to_main_repo dictionary in /etc/workspaces.yml that maps a workspace name to the name of its main repository name"
}

if [[ -z $1 ]]; then
    inner_workspaces_script describeallworkspaces
else
    if [ "$1" == "--help" ]; then
        _workspaces_help
    else
        root_dir="`inner_workspaces_script getrootdir`"
        workspace_dir="$root_dir/$1"
        if [ -d $workspace_dir ]; then
            cd $workspace_dir
            inner_workspaces_script describeoneworkspace $@
        else
            rm /tmp/_workspaces.chosen -rf
            inner_workspaces_script explicitcommand $@
            if [ "$1" == "-i" ]; then
                cd `cat /tmp/_workspaces.chosen`;
            fi
            if [ $? -ne 0 ]; then
                _workspaces_help
            fi
        fi
    fi
fi
