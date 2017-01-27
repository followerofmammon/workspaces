#!/bin/bash
if [[ -z $1 ]]; then
    inner_workspaces_script describe
else
    if [ "$1" == "--help" ]; then
        echo This tool lists workspaces in a predefined directory, and describes the current git HEAD
        echo in the 'main' git repository, for each workspace.
        echo
        echo - To list workspaces, run with no args.
        echo
        echo - To change the workspaces root dir, either set WORKSPACES_ROOT_DIR env var, or edit the default
        echo rootdir in the workspaces python script.
        echo
        echo - To set a specific main repository for a workspace, add a '.workspaces.yml' inside the workspace
        echo dir, and add the line 'main_repo: <your_repo_dirname>'
    else
        root_dir="`inner_workspaces_script getrootdir`"
        workspace_dir="$root_dir/$1"
        if [ -d $workspace_dir ]; then
            cd $workspace_dir
        else
            echo Workspace \"$1\" does not exist in $rootdir
        fi
    fi
fi
