from termcolor import colored


def info(s):
    print(colored(s, 'green'))


def error(s):
    print(colored(s, 'red'))


def green(s):
    return colored(s, 'green')


def red(s):
    return colored(s, 'red')


def yellow(s):
    return colored(s, 'yellow')
