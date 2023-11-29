import os
import sys


module_aliases = {
    "git": ["g"],
}


def get_module_name(m):
    m = sys.argv[1]
    for k, v in module_aliases.items():
        if m in v:
            m = k
            break
    return m


def run_module(m, args):
    os.system(f"python -m pylinhsu.{m} {' '.join(args)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        m = get_module_name(sys.argv[1])
        run_module(m, sys.argv[2:])
