#cli.py, here is the script that interact with the user of rptree generator

import argparse, pathlib, sys
#I created a .py file staring with ./ and ending with /, declaring the .py as a module to be called.
from . import __version__
from .rptree import DirectoryTree

#defining a function main
def main():
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir) #converting root_dir into a pathlib.Path object
    if not root_dir.is_dir(): #a quick check if the entry is a valid directory
        print('The specified root directory does not exist!')
        sys.exit()
    tree = DirectoryTree(root_dir, dir_only = args.dir_only, output_file=args.output_file)
    tree.generate()
    parse_cmd_line_arguments()
#defining a function that privides all CLI related features
def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog = 'tree',
        description = 'Tree, a directory tree generator',
        epilog = 'Thanks for using TREE!',
    )
    parser.version = f"Tree v{__version__}"
    parser.add_argument(
        '-d',
        '--dir-only',
        action = 'store_true',
        help = 'Generate a directory-only tree',
    )
    parser.add_argument('-v','--version',action = 'version')
    parser.add_argument(
        'root_dir',
        metavar = 'ROOT_DIR',
        nargs = '?',
        default = '.',
        help = 'Generate a full directory tree starting at ROOT_DIR',
    )
    parser.add_argument(
        '-o',
        '--output-file',
        metavar = 'OUTPUT_FILE',
        nargs = '?',
        default = sys.stdout,
        help = 'Generate a full directory tree and save it to a file',
    )
    #the first thing to be display when script run
    return parser.parse_args(input('Enter root_dir: ').split())
    #return parser.parse_args()
