import re


CODE_BLOCK_TAG = '//@'


def print_code_lines(code_lines):
    for cl in code_lines:
        print(cl, end='')


def get_regexes(cl):
    p = cl.find(CODE_BLOCK_TAG)
    cl = cl[p+len(CODE_BLOCK_TAG)+1:]
    regexes = cl.strip().split(' ')
    return regexes


def match_test_name(cl, test):
    regexes = get_regexes(cl)
    for r in regexes:
        if re.match(r, test):
            return True
    return False


def uncomment_code_line(code_lines, start):
    result_comment = re.match(r' *(// )+', code_lines[start])
    if result_comment:
        result_space = re.match(r' *', code_lines[start])
        p = result_space.span()[1]
        code_lines[start] = code_lines[start][:p] + \
            code_lines[start][result_comment.span()[1]:]
        # print(code_lines[start], end='')
        return True
    else:
        return False


def uncomment_code_block(code_lines, start):
    i = start
    while uncomment_code_line(code_lines, i):
        i += 1
    # print(f'Uncommented code block at line {start} starting with `{code_lines[start][:-1]}`.')


def comment_code_line(code_lines, start):
    if code_lines[start] == '\n':
        return False
    result_comment = re.match(r' *(// )+', code_lines[start])
    if result_comment:
        return False
    else:
        result_space = re.match(r' *', code_lines[start])
        p = result_space.span()[1]
        code_lines[start] = code_lines[start][:p] + \
            '// ' + code_lines[start][p:]
        # print(code_lines[start], end='')
        return True


def comment_code_block(code_lines, start):
    i = start
    while comment_code_line(code_lines, i):
        i += 1
    # print(f'  Commented code block at line {start} starting with `{code_lines[start][:-1]}`.')


def filter_code_blocks_for_test(code_lines, test):
    for i, cl in enumerate(code_lines):
        if CODE_BLOCK_TAG in cl:
            if match_test_name(cl, test):
                uncomment_code_block(code_lines, i)
            else:
                comment_code_block(code_lines, i)
