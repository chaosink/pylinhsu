import os
import sys


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    args = ' '.join(sys.argv[2:])

    if cmd == 'ga':
        os.system(f'git commit --amend --no-edit')
    if cmd == 'gcp':
        os.system(f'git cherry-pick {args}')
    if cmd == 'gll':
        os.system(f'git log --oneline')
    if cmd == 'glg':
        os.system(f'git log --all --decorate --oneline --graph')
    if cmd == 'g':
        os.system(f'python -m pylinhsu.git {args}')
