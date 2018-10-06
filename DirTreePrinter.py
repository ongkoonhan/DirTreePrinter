import os
import fnmatch
import string
from collections import deque


class _dir_tree_printer:

    def __init__(self):
        self.print_list = ["root/"]
        self.ignore_list = [".git/"]
        self.bar_vert = chr(9474)
        self.bar_horz = chr(9472)
        self.bar_T = chr(9500)


    def _should_ignore(self, entry):
        for pat in self.ignore_list:
            if fnmatch.fnmatch(entry, pat):
                print(entry)
                return True
        return False


    def _print_sub_dir(self, sub_dir_name, traversal_path):
        traversal_path = traversal_path[:-1]
        str_print = []
        for traversed in traversal_path:
            if traversed == "1":
                str_print.append(self.bar_vert + " "*3)
            else:
                str_print.append(" " *4)
        str_print.extend([self.bar_T + self.bar_horz*3, sub_dir_name])
        str_print = "".join(str_print)
        self.print_list.append(str_print)


    def _print_files(self, files, traversal_path):
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


    def _walk_dir(self, dir, traversal_path=""):
        files = []
        sub_dirs = deque([])

        for entry in os.scandir(dir):
            name = entry.name
            if entry.is_dir():
                name += "/"
                sub_dirs.append(name)
            elif entry.is_file():
                files.append(name)

        if len(sub_dirs) <= 1:
            traversal_path += "0"
            self._print_files(files, traversal_path)   # Print files
        else:
            traversal_path += "1"
            self._print_files(files, traversal_path)   # Print files

            while True:
                sub_dir = sub_dirs.popleft()
                self._print_sub_dir(sub_dir, traversal_path)   # Print sub_dirs

                if len(sub_dirs) > 0:
                    self._walk_dir(os.path.join(dir, sub_dir), traversal_path)  # Recursive DFS
                else:
                    break


    def _walk_dir_with_ignore(self, dir, traversal_path="", ignore=False):
        files = []
        sub_dirs = deque([])

        for entry in os.scandir(dir):
            name = entry.name
            if entry.is_dir():
                name += "/"
                if ignore and self._should_ignore(name):
                    continue
                sub_dirs.append(name)
            elif entry.is_file():
                if ignore and self._should_ignore(name):
                    continue
                files.append(name)

        if len(sub_dirs) <= 1:
            traversal_path += "0"
            self._print_files(files, traversal_path)   # Print files
        else:
            traversal_path += "1"
            self._print_files(files, traversal_path)   # Print files

            while True:
                sub_dir = sub_dirs.popleft()
                self._print_sub_dir(sub_dir, traversal_path)   # Print sub_dirs

                if len(sub_dirs) > 0:
                    self._walk_dir_with_ignore(os.path.join(dir, sub_dir), traversal_path, ignore)  # Recursive DFS
                else:
                    break


def print_dir_tree(outfile, ignorefile=None):
    printer = _dir_tree_printer()
    outfile = os.path.join(outfile)

    if os.path.exists(outfile):
        os.remove(outfile)

    # Build ignore list
    if ignorefile is not None:
        ignore = os.path.join(ignorefile)
        assert os.path.exists(ignorefile), "{0} does not exist!".format(ignore)
        ws = [ws for ws in string.whitespace]
        with open(ignore, "r") as f:
            for line in f:
                if line not in ws:
                    if not line.startswith("#"):
                        printer.ignore_list.append(line.rstrip("\n"))

    # Run walk
    if ignorefile is not None:
        printer._walk_dir_with_ignore(outfile)
    else:
        printer._walk_dir(outfile)

    # Print tree
    with open(outfile, "a", encoding="utf-8") as f:
        for line in printer.print_list:
            f.write(line + "\n")




























