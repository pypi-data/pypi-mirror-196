"""
A pipe that saves an additional copy of the files. In my case, I'm using it
to put an additional copy in ~/public_html so I can read it into GSheets
"""
from distutils.dir_util import copy_tree

def copy_to_dir(pl, path):
    copy_tree(pl.grid_output_path, path)
    print(f"Output dir copied to {path}")