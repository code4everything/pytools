# coding:utf8

# run: python fops.py cmds

# -------------------------------------------- #
# rm:cmd,file_pattern:string
# -------------------------------------------- #

import sys
import os
import re


def remove_by_file_pattern(args: list):
    if len(args) < 1:
        print('missing file pattern')
        return
    file_pattern = args[0]
    for (dirpath, dirnames, filenames) in os.walk('.'):
        for filename in filenames:
            path = '%s%s%s' % (dirpath, os.path.sep, filename)
            if re.search(file_pattern, path):
                print('remove file %s' % path)
                os.remove(path)


# print(sys.argv)
for arg in sys.argv[1:]:
    cmd_arg = str.split(arg, ',')[1:]

    if str.startswith(arg, 'rm'):
        remove_by_file_pattern(cmd_arg)
