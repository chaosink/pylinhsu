from termcolor import colored


def info(s):
    print(colored(s, 'green'))


def error(s):
    print(colored(s, 'red'))
