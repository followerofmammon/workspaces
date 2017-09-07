import os
import sys
import yaml

import printwarning


DEFAULT_WORKSPACES_ROOT_DIR = os.path.join(os.path.expanduser("~"), "work", "code")
DEFAULT_REPOSITORY_TO_SHOW_BY_PRIORITY = ["strato-storage", "monkey"]
REPO_CONFIG_FILENAME = ".workspaces.yml"
WORKSPACES_CONFIG_FILENAME = "/etc/workspaces.yml"

root_dir = None
ignore_unknown = False
dirs_to_ignore = list()
workspace_to_main_repo = dict()


def _set_workspaces_root_dir():
    global root_dir
    if root_dir is None:
        if "WORKSPACES_ROOT_DIR" in os.environ:
            root_dir = os.environ["WORKSPACES_ROOT_DIR"]
        else:
            root_dir = DEFAULT_WORKSPACES_ROOT_DIR
        if not os.path.exists(root_dir):
            print ("It appears that the current configured workspaces rootdir '%s' does not exist. To "
                "configure the right root dir, you can either:" % (root_dir,))
            print "* set the WORKSPACES_ROOT_DIR env var"
            print "* Add root_dir: <your_root_dir> to %s" % (WORKSPACES_CONFIG_FILENAME,)
            print "Or, you could create this root dir :)"
            sys.exit(1)
    else:
        if root_dir.startswith("~/"):
            inner_part = root_dir[2:]
            root_dir = os.path.join(os.path.expanduser("~"), inner_part)
    root_dir = os.path.realpath(root_dir)


def read_configuration():
    global dirs_to_ignore
    global workspace_to_main_repo
    with open(WORKSPACES_CONFIG_FILENAME) as config_file:
        try:
            configuration = yaml.load(config_file)
        except:
            print "Failed to parse config filename ", WORKSPACES_CONFIG_FILENAME
            return
        for varname, value in configuration.iteritems():
            globals()[varname] = value
    if root_dir is None:
        print "Warning: 'root_dir' is not configured in config file ", WORKSPACES_CONFIG_FILENAME
    else:
        _set_workspaces_root_dir()
    if dirs_to_ignore is None:
        dirs_to_ignore = list()
    elif isinstance(dirs_to_ignore, str):
        dirs_to_ignore = [dirs_to_ignore]
    elif not isinstance(dirs_to_ignore, list):
        printwarning.printwarning("Badly formed 'dirs_to_ignore' in configuration file %" %
                                  (configuration.WORKSPACES_CONFIG_FILENAME,))
    if not isinstance(workspace_to_main_repo, dict):
        printwarning.printwarning("workspace_to_main_repo in %s should be a dictionary of workspaces to "
                                  "main repository dir names" % (configuration.WORKSPACES_CONFIG_FILENAME,))


read_configuration()
