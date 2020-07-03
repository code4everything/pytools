# coding:utf8

# run: python fops.py cmds

# -------------------------------------------- #
# rm:cmd,file_pattern:string
# -------------------------------------------- #

import glob
import sys
import os


def remove_by_file_pattern(args: list):
    if len(args) < 1:
        print('missing file pattern')
        return
    file_pattern = args[0]
    for filename in glob.glob(file_pattern):
        os.remove(filename)


for arg in sys.argv[1:]:
    cmd_arg = str.split(arg, ',')[1:]

    if str.startswith(arg, 'rm'):
        remove_by_file_pattern(cmd_arg)
