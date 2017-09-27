import workspace
import workspace_shelloutput


def _remove_workspace_without_main_repo(workspaces_tree, workspaces):
    workspaces_nodes = workspaces_tree.children(workspaces_tree.root)
    for node in workspaces_nodes:
        workspace_obj = [workspace for workspace in workspaces if workspace.name == node.data.name][0]
        if workspace_obj.main_repo is None:
            workspaces_tree.remove_node(node.identifier)


def get():
    workspaces_tree = workspace.get_workspaces_tree()
    workspaces_dirs = workspaces_tree.children(workspaces_tree.root)
    workspaces = [workspace.Workspace(_workspace.data.name) for _workspace in workspaces_dirs]
    _remove_workspace_without_main_repo(workspaces_tree, workspaces)
    workspace_shelloutput.prettify_workspaces_tree(workspaces_tree, workspaces)
    return workspaces_tree
