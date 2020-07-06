# coding:utf8

# run: python fout.py './file_pattern*' cmds

# --------------------------------------------------------------------------------------- #
# limit:cmd,offset:int,size:int|a(all)
# --------------------------------------------------------------------------------------- #
# grep:cmd,extract_ex:bool,regexp:string[,regexp]...
# --------------------------------------------------------------------------------------- #
# sort:cmd[,a|n:cmd[,sep:string[,col:int]]]
# --------------------------------------------------------------------------------------- #
# unique:cmd[,show_count:bool[,sep:string[,col:int]]]
# --------------------------------------------------------------------------------------- #
# cut:cmd,sep:string,joiner:string,field:int[,field]...
# --------------------------------------------------------------------------------------- #
# cmd_sep[*]:cmd
# --------------------------------------------------------------------------------------- #
# reverse:cmd
# --------------------------------------------------------------------------------------- #
# count:cmd
# --------------------------------------------------------------------------------------- #
# copy:cmd
# --------------------------------------------------------------------------------------- #

import sys
import glob
import re
import pyperclip

if len(sys.argv) < 2:
    print('missing file pattern')
    exit()

file_pattern = sys.argv[1]

cmd_sep = ','


def parse_by_limit(args: list, lines: list):
    """
    支持倒着取行数
    """
    offset = int(args[0])
    size = args[1]

    if size == 'a' or size == 'all':
        if offset < 0:
            return lines[:len(lines)+offset+1]
        return lines[offset:]
    if offset < 0:
        end = len(lines)+offset+1
        return lines[end-int(size):end]
    return lines[offset:offset+int(size)]


def parse_by_regexp(args: list, lines: list):
    extract_ex = 't' == args[0] or 'true' == args[0]
    regexp = '.*'.join(args[1:])

    match_lines = []
    can_extract = False

    for line in lines:
        if can_extract:
            if re.match(r'\d{4}(-\d{2}){2}.*', line):
                can_extract = False
            else:
                # 提取异常数据
                match_lines.append(line)
        if re.search(regexp, line, re.I):
            match_lines.append(line)
            can_extract = extract_ex
    return match_lines


def parse_by_sort(args: list, lines: list):
    args = parse_unique_and_sort_args(args)
    sort_by_number = 'n' == args[0]
    col = int(args[2])

    def get_sort_token(line: str):
        if len(args[1]) > 0:
            fields = str.split(line, args[1])
            line = ''
            if len(fields) > col:
                line = fields[col]
        if sort_by_number and len(line) < 1:
            line = '0'
        return int(line) if sort_by_number else line
    lines.sort(key=get_sort_token)
    return lines


def parse_by_unique(args: list, lines: list):
    args = parse_unique_and_sort_args(args)
    show_count = 't' == args[0] or 'true' == args[0]
    col = int(args[2])

    unique_lines = []
    line_col_map = {}
    unique_map = {}

    # 去重
    for line in lines:
        fileds = [line] if len(args[1]) < 1 else str.split(line, args[1])
        key = fileds[col]
        count = unique_map.get(key, 0)
        if count == 0:
            unique_lines.insert
            unique_lines.append(line)
            line_col_map[line] = key
        unique_map[key] = count+1
    if not show_count:
        return unique_lines
    for i in range(0, len(unique_lines)):
        unique_lines = [
            ' '.join([str(unique_map[line_col_map[line]]), line]) for line in unique_lines]
    return unique_lines


def parse_unique_and_sort_args(args: list):
    parsed_args = ['a', '', '0']
    if len(args) > 2:
        parsed_args[2] = args[2]
    if len(args) > 1:
        parsed_args[1] = args[1]
    if len(args) > 0:
        parsed_args[0] = args[0]
    return parsed_args


def parse_by_cut(args: list, lines: list):
    """
    重组字符串
    """
    if len(args) < 1:
        return lines
    sep = args[0]
    cols = [int(arg) for arg in args[2:]]
    joiner = args[1] if len(args) > 1 else ''

    # 拼接指定列
    joinned_lines = []
    for line in lines:
        fields = str.split(line, sep)
        if len(cols) > 0:
            fields = [fields[col] for col in cols]
        joinned_lines.append(joiner.join(fields))
    return joinned_lines


def parse_by_cmd(cmd: str, lines: list):
    """
    按命令解析字符
    """
    args = str.split(cmd, cmd_sep)[1:]

    if str.startswith(cmd, 'limit'):
        return parse_by_limit(args, lines)
    if str.startswith(cmd, 'grep'):
        return parse_by_regexp(args, lines)
    if str.startswith(cmd, 'cut'):
        return parse_by_cut(args, lines)
    if str.startswith(cmd, 'unique'):
        return parse_by_unique(args, lines)
    if str.startswith(cmd, 'sort'):
        return parse_by_sort(args, lines)
    if str.startswith(cmd, 'count'):
        return [str(len(lines))]
    if str.startswith(cmd, 'reverse'):
        lines.reverse()
    if str.startswith(cmd, 'copy'):
        pyperclip.copy('\n'.join(lines))
        return []
    return lines


# 读取文件内容
lines = []
for filename in glob.glob(file_pattern):
    with open(filename, 'r', encoding='utf8') as fr:
        lines.extend(str.strip(line, '\n')
                     for line in fr.readlines() if len(line) > 0)

# 依次解析命令
# print(sys.argv)
# lines = [line for line in lines if len(line) > 0]
for arg in sys.argv[2:]:
    if str.startswith(arg, 'cmd_sep'):
        cmd_sep = ''.join(arg[7:])
        continue
    lines = parse_by_cmd(str.lower(arg), lines)
print('\n'.join(lines))
