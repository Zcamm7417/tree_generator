import os, pathlib, sys

PIPE = '|'
ELBOW = '|___'
TEE = '|---'
PIPE_PREFIX = '|    '
SPACE_PREFIX = '     '

#class initializer
class DirectoryTree:
    def __init__(self, root_dir, dir_only=False, output_file=sys.stdout):
        self._output_file = output_file
        #creating an instance attribute ._generator with the class initializer
        self._generator = _TreeGenerator(root_dir, dir_only)
    #defining a function generate with self that will create a file in writable format and append all output
    def generate(self):
        tree = self._generator.build_tree()
        if self._output_file != sys.stdout:
            tree.insert(0, "'''")
            tree.append("'''")
            self._output_file = open(
                self._output_file, mode= 'w', encoding  = 'UTF-8'
            )
        with self._output_file as stream:
            for entry in tree:
                print(entry, file = stream)
#defining a function class that traverse the file system and generates the directory tree diagram
class _TreeGenerator:
    #defining the class initializer and turn the root_dir into a pthlib.Path object
    def __init__(self, root_dir, dir_only=False):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._tree = [] #empty list that store the entries that shape the directory tree diagram
    #defining a public method function to generate the tree
    def build_tree(self):
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree
    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)
    #a function that two argument, directory: hold the path in pathlib.Path that you want to walk, prefix: holds a prefix string that is used to draw the tree diagram
    def _tree_body(self, directory, prefix = ''):
        #.iterdir call returns an iterator over the files contain in the directory
        #entries = directory.iterdir()
        entries = self._prepare_entries(directory)
        entries_count = len(entries)
        for index, entry in enumerate(entries): #start a for loop that iterate over the entries
            connector = ELBOW if index == entries_count -1 else TEE
            if entry.is_dir(): #checking if the entry is a directory
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)
    def _prepare_entries(self, directory):
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()] #conditional statement to check if the current entry is a directory
            return entries
        entries= sorted(entries, key=lambda entry: entry.is_file()) #sort the entries in the directory using sorted with a lambda function to return true or false if entry is a file.
        return entries
    def _add_directory(
        self, directory, index, entries_count, prefix, connector
    ):
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        #a conditional statement that update prefix according to the current entry
        if index != entries_count -1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory = directory,
            prefix = prefix,
        )
        self._tree.append(prefix.rstrip())
    def _add_file(self, file, prefix, connector): #appending a file entry to the directory tree list
        self._tree.append(f"{prefix}{connector} {file.name}")
