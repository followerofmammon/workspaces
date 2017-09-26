from dirsync import dirtree
from dirsync import printer
from dirsync import treepicker

import workspace
import configuration


_result = None


def remove_non_workspace_entries(fstree):
    workspaces_dirs = workspace.list_workspaces_dirs()
    for node in fstree.children(fstree.root):
        entry = node.data
        if entry.name not in workspaces_dirs:
            fstree.remove_node(node.identifier)


def pick():
    fstree = dirtree.DirTree.factory_from_filesystem(configuration.root_dir,
                                                     max_depth=2,
                                                     dirs_only=True,
                                                     include_hidden=False)
    remove_non_workspace_entries(fstree)

    picker = treepicker.TreePicker(fstree, min_nr_options=1, max_nr_options=1)
    global _result
    _result = picker.pick_one()


def interactive():
    printer.wrapper(pick)
    if _result is not None:
        with open("/tmp/_workspaces.chosen", "w") as output_file:
            output_file.write(_result.full_filesystem_path())


if __name__ == "__main__":
    fstree = dirtree.DirTree.factory_from_filesystem("/home", max_depth=2, dirs_only=True, include_hidden=False)
    import pdb
    pdb.set_trace()
