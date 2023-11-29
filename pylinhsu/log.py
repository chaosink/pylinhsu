from termcolor import colored


def green(s):
    return colored(s, "green")


def yellow(s):
    return colored(s, "yellow")


def red(s):
    return colored(s, "red")


def info(s):
    print(green(s))


def warning(s):
    print(yellow(s))


def error(s):
    print(red(s))
