import workspace
import workspace_shelloutput


def describeindetail():
    workspaces_dirs = workspace.list_workspaces_dirs()
    workspaces = [workspace.Workspace(_workspace) for _workspace in workspaces_dirs]
    workspace_shelloutput.print_workspaces_with_main_repos(workspaces, is_detailed=True)
    workspace_shelloutput.print_workspaces_without_main_repos(workspaces)
