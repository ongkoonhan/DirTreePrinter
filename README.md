# DirTreePrinter
Print your directory structure, with gitignore

```
import DirTreePrinter as d

d.print_dir_tree(dir, outfile_name, gitignore_file=None, root_name=None, other_ignore_list=None)
```
* **dir -** path of root directory to traverse
* **outfile_name -** name of text file containing the printed directory tree
* **gitignore_file (optional, default=None) -** path of .gitignore file containing the patterns you want to ignore in the printing
* **root_name (optional, default="root/") -** manual option to change the printed name of the root directory
* **other_ignore_list (optional, default=[".git/"]) -** manual option to include other patterns to ignore that are not specified in the gitignore file
