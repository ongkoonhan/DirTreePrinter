import os
import fnmatch
import string
from collections import deque


class __dir_tree_printer:

    def __init__(self, root_name=None, other_ignore_list=None):
        self.print_list = ["root/"] if root_name is None else [root_name]
        self.ignore_list = [".git/"] if other_ignore_list is None else list(other_ignore_list)
        self.bar_vert = chr(9474)
        self.bar_horz = chr(9472)
        self.bar_T = chr(9500)


    def should_ignore(self, entry, path):
        for pat in self.ignore_list:
            if fnmatch.fnmatch(entry, pat):
                print("-- ignore pattern: {0} -> ignored: {1}".format(pat, path))
                return True
        return False


    def print_sub_dir(self, sub_dir_name, traversal_path):
        traversal_path = traversal_path[:-1]
        str_print = []
        for traversed in traversal_path:
            if traversed == "1":
                str_print.append(self.bar_vert + " "*3)
            else:
                str_print.append(" "*4)
        str_print.extend([self.bar_T + self.bar_horz*3, sub_dir_name])
        str_print = "".join(str_print)
        self.print_list.append(str_print)


    def print_files(self, files, traversal_path):
        for file in files:
            str_print = []
            for traversed in traversal_path:
                if traversed == "1":
                    str_print.append(self.bar_vert + " "*3)
                else:
                    str_print.append(" "*4)
            str_print.append(file)
            str_print = "".join(str_print)
            self.print_list.append(str_print)


    def walk_dir(self, dir, traversal_path=""):
        files = []
        sub_dirs = deque([])

        for entry in os.scandir(dir):
            name = entry.name
            if entry.is_dir():
                name += "/"
                sub_dirs.append(name)
            elif entry.is_file():
                files.append(name)

        if len(sub_dirs) == 0:
            traversal_path += "0"
        else:
            traversal_path += "1"
        self.print_files(files, traversal_path)  # Print files

        while True:
            if len(sub_dirs) > 0:
                sub_dir = sub_dirs.popleft()
                self.print_sub_dir(sub_dir, traversal_path)  # Print sub_dirs

                if len(sub_dirs) == 0:  # Modify after printing (last sub_dir)
                    traversal_path = traversal_path[:-1] + "0"

                self.walk_dir(os.path.join(dir, sub_dir), traversal_path)  # Recursive DFS
            else:
                break


    def walk_dir_with_ignore(self, dir, traversal_path=""):
        files = []
        sub_dirs = deque([])

        for entry in os.scandir(dir):
            name = entry.name
            if entry.is_dir():
                name += "/"
                if self.should_ignore(name, os.path.join(dir, name)):
                    continue
                sub_dirs.append(name)
            elif entry.is_file():
                if self.should_ignore(name, os.path.join(dir, name)):
                    continue
                files.append(name)

        if len(sub_dirs) == 0:
            traversal_path += "0"
        else:
            traversal_path += "1"
        self.print_files(files, traversal_path)  # Print files

        while True:
            if len(sub_dirs) > 0:
                sub_dir = sub_dirs.popleft()
                self.print_sub_dir(sub_dir, traversal_path)   # Print sub_dirs

                if len(sub_dirs) == 0:  # Modify after printing (last sub_dir)
                    traversal_path = traversal_path[:-1] + "0"

                self.walk_dir_with_ignore(os.path.join(dir, sub_dir), traversal_path)  # Recursive DFS
            else:
                break


def print_dir_tree(dir, outfile_name, gitignore_file=None, root_name=None, other_ignore_list=None):
    printer = __dir_tree_printer(root_name=root_name, other_ignore_list=other_ignore_list)
    outfile = os.path.join(outfile_name)

    if os.path.exists(outfile):
        os.remove(outfile)

    # Build ignore list
    if gitignore_file is not None:
        ignore = os.path.join(gitignore_file)
        assert os.path.exists(gitignore_file), "{0} does not exist!".format(ignore)
        ws = [ws for ws in string.whitespace]
        with open(ignore, "r") as f:
            for line in f:
                if line not in ws:
                    if not line.startswith("#"):
                        printer.ignore_list.append(line.rstrip("\n"))

    # Run walk
    if gitignore_file is not None:
        printer.walk_dir_with_ignore(dir)
    else:
        printer.walk_dir(dir)

    # Print tree
    with open(outfile, "a", encoding="utf-8") as f:
        for line in printer.print_list:
            f.write(line + "\n")

