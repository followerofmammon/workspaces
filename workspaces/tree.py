import workspace
import workspace_shelloutput


def get():
    workspaces_tree = workspace.get_workspaces_tree()
    workspaces_dirs = workspaces_tree.children(workspaces_tree.root)
    workspaces = [workspace.Workspace(_workspace.data.name) for _workspace in workspaces_dirs]
    workspace_shelloutput.prettify_workspaces_tree(workspaces_tree, workspaces)
    return workspaces_tree
