# coding:utf8

# --------------------------------------------------------------------------------------- #
# limit:cmd,offset:int,size:int|A(all)
# --------------------------------------------------------------------------------------- #
# re:cmd,extract_e:bool,regexp:string[,regexp...]
# --------------------------------------------------------------------------------------- #
# sort:cmd,a|n:cmd,sep:string,col:int
# --------------------------------------------------------------------------------------- #
# unique:cmd,show_count:bool,sep:string,col:int
# --------------------------------------------------------------------------------------- #
# cut,sep:string,joiner:string,field:int[,field...]
# --------------------------------------------------------------------------------------- #
# cmd_sep[,]
# --------------------------------------------------------------------------------------- #

import sys
import glob
import re

"""
if len(sys.argv) < 2:
    print('missing file pattern')
    exit()

file_pattern = sys.argv[2]
"""

file_pattern = 'user-web.2019-10-30.user-web-002.0.log'
cmd_sep = ','

def parse_by_limit(args: list, lines: list):
    """
    支持倒着取行数
    """
    offset = int(args[0])
    size = args[1]

    print(offset, size)
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
    print('\'%s\'' % regexp)

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
    return lines


def parse_by_unique(args: list, lines: list):
    return lines


def parse_by_cut(args: list, lines: list):
    """
    重组字符串
    """
    if len(args) < 1:
        return lines
    sep = args[0]
    cols = args[2:]
    joiner = args[1] if len(args) > 1 else ''

    # 拼接指定列
    joinned_lines = []
    for line in lines:
        fields = str.split(line, sep)
        if len(cols) > 0:
            handled_fields = []
            for col in cols:
                handled_fields.append(fields[int(col)])
            fields = handled_fields
        joinned_lines.append(joiner.join(fields))
    return joinned_lines


def parse_by_cmd(cmd: str, content: str):
    """
    按命令解析字符
    """
    lines = str.split(content, '\n')
    args = str.split(cmd, cmd_sep)[1:]
    parsed_lines = lines

    if str.startswith(cmd, 'limit'):
        parsed_lines = parse_by_limit(args, lines)

    if str.startswith(cmd, 're'):
        parsed_lines = parse_by_regexp(args, lines)

    if str.startswith(cmd, 'cut'):
        parsed_lines = parse_by_cut(args, lines)

    return '\n'.join(parsed_lines)


# 读取文件内容
content = ''
for filename in glob.glob(file_pattern):
    with open(filename, 'r', encoding='utf8') as fr:
        content += fr.read()+'\r\n'

# 依次解析命令
print(sys.argv)
for arg in sys.argv[1:]:
    if str.startswith(arg, 'cmd_sep'):
        cmd_sep = ''.join(arg[7:])
        continue
    content = parse_by_cmd(str.lower(arg), content)

print(content)
