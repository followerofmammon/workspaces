from dirsync import treeprinter


import tree


def describeallworkspaces():
    workspaces_tree = tree.get()
    tree_printer = treeprinter.TreePrinter(workspaces_tree, including_root=False)
    tree_printer.calculate_lines_to_print(workspaces_tree.root, [], None)
    tree_printer.print_tree(print_info_line=False)
