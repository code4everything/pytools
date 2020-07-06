# coding:utf8

# run: python fops.py cmds

# -------------------------------------------- #
# rm:cmd,file_pattern:string[,root:string]
# -------------------------------------------- #
# mv:cmd,file_pattern:string[,root:string]
# -------------------------------------------- #
# cp:cmd,file_pattern:string[,root:string]
# -------------------------------------------- #
# find,file_pattern:string[,root:string]
# -------------------------------------------- #

import sys
import os
import re


def remove_by(file_pattern: str, root: str):
    for (dirpath, dirnames, filenames) in os.walk(root):
        for filename in filenames:
            path = '%s%s%s' % (dirpath, os.path.sep, filename)
            if re.search(file_pattern, path):
                print('remove file %s' % path)
                os.remove(path)


# print(sys.argv)
for arg in sys.argv[1:]:
    cmd_arg = str.split(arg, ',')[1:]

    if len(cmd_arg) < 1:
        print('missing file pattern')
        exit()
    file_pattern = cmd_arg[0]
    root = '.'

    if len(cmd_arg) > 1:
        root = cmd_arg[1]

    if str.startswith(arg, 'rm'):
        remove_by(file_pattern, root)
