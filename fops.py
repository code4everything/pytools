# coding:utf8

# run: python fops.py cmds

# ------------------------------------------------------------------------- #
# rm:cmd,file_pattern:string,root:string
# ------------------------------------------------------------------------- #
# mv:cmd,file_pattern:string,root:string,target:string
# ------------------------------------------------------------------------- #
# cp:cmd,file_pattern:string,root:string,target:string
# ------------------------------------------------------------------------- #
# find,file_pattern:string,root:string
# ------------------------------------------------------------------------- #
# mkdir,folder:string
# ------------------------------------------------------------------------- #

import sys
import os
import re
import shutil


def file_operation(file_pattern: str, root: str, target: str, callback):
    for (dirpath, dirnames, filenames) in os.walk(root):
        for filename in filenames:
            path = '%s%s%s' % (dirpath, os.path.sep, filename)
            if re.search(file_pattern, path):
                target = '%s%s%s' % (target, '' if target.endswith(
                    os.path.sep) else os.path.sep, filename)
                callback(path, target)


def callback_of_finding(path: str, target: str):
    print(path)


def callback_of_removing(path: str, target: str):
    print('remove file %s' % path)
    os.remove(path)


def callback_of_copying(path: str, target: str):
    print('copy file %s to %s' % (path, target))
    shutil.copyfile(path, target)
    
def callback_of_moving(path: str, target: str):
    print('move file %s to %s' % (path, target))
    shutil.move(path, target)


# print(sys.argv)
for arg in sys.argv[1:]:
    cmd_arg = str.split(arg, ',')[1:]
    cmd_arg.sort
    if len(cmd_arg) < 1:
        print('missing file pattern')
        exit()
    file_pattern = cmd_arg[0]
    root = '.'

    if len(cmd_arg) > 1:
        root = cmd_arg[1]

    target = '.'
    if len(cmd_arg) > 2:
        target = cmd_arg[2]

    if str.startswith(arg, 'rm'):
        file_operation(file_pattern, root, target, callback_of_removing)
    if str.startswith(arg, 'find'):
        file_operation(file_pattern, root, target, callback_of_finding)
    if str.startswith(arg, 'cp'):
        file_operation(file_pattern, root, target, callback_of_copying)
    if str.startswith(arg, 'mv'):
        file_operation(file_pattern, root, target, callback_of_moving)
    if str.startswith(arg, 'mkdir'):
        os.makedirs(file_pattern)
