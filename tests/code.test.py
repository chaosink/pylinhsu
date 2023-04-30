import pylinhsu.code as cd
from io import StringIO


def test_filter_code_blocks_for_test():
    content = '''

    0;

    1;
    // 1

    // 2
    2;

    //@ 3
    3;

    // //@ 4
    // 4;

    // //@ 5
    // 5;

    '''
    f = StringIO(content)
    code_lines = f.readlines()

    cd.filter_code_blocks_for_test(code_lines, '4')
    cd.print_code_lines(code_lines)


if __name__ == '__main__':
    test_filter_code_blocks_for_test()
