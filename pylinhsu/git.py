import os
import uuid
import argparse
from pylinhsu.log import info, error
from pylinhsu.os import get_command_output


# ----------------------------------------------------------------------------------------------------
# Helper functions, assuming already in a Git repo dir.


def get_git_hashes():
    hashes = get_command_output("git log --format=%h")
    return hashes.strip().split("\n")


def get_git_current_branch():
    branch_current = get_command_output("git rev-parse --abbrev-ref HEAD")
    return branch_current.strip().split("\n")[0]


# ----------------------------------------------------------------------------------------------------
# GitContext


class GitContext:
    """Change/recover Git branch and working dir."""

    def __init__(self, branch, work_dir):
        self.branch = branch
        self.work_dir = work_dir

    def __enter__(self):
        self.work_dir_bak = os.getcwd()
        if self.work_dir_bak != self.work_dir:
            os.chdir(self.work_dir)
        self.branch_bak = get_git_current_branch()
        if self.branch is None:
            self.branch = get_git_current_branch()
        if self.branch_bak != self.branch:
            os.system(f"git checkout {self.branch}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.branch_bak != self.branch:
            os.system(f"git checkout {self.branch_bak}")
        if self.work_dir_bak != self.work_dir:
            os.chdir(self.work_dir_bak)


# ----------------------------------------------------------------------------------------------------
# Functions for sub-commands.


def recommit(hash, branch=None, work_dir="."):
    """Recommit all commits after the commit with the specified hash."""
    with GitContext(branch, work_dir) as gc:
        hashes = get_git_hashes()
        hl = len(hashes[0])
        if len(hash) < hl:
            error(
                f"Hash length should be {hl} at least for this repo, however {len(hash)} given!"
            )
            return
        hash = hash[:hl]

        try:
            hashes = hashes[: hashes.index(hash)]
        except ValueError:
            error(f"Cannot find hash {hash} in commit logs!")
            return
        hashes.reverse()

        branch_tmp = str(uuid.uuid4())[:8]
        os.system(f"git checkout -b {branch_tmp}")
        os.system(f"git reset --hard {hash}")
        for hash in hashes:
            os.system(f"git cherry-pick {hash}")
            os.system("git commit --amend --reset-author --no-edit")
        info(f"Recommit on temp branch {branch_tmp} in dir {gc.work_dir} done!")

        os.system(f"git checkout {gc.branch}")
        os.system(f"git reset --hard {branch_tmp}")
        os.system(f"git branch -d {branch_tmp}")
        info(f"Recommit on target branch {gc.branch} in dir {gc.work_dir} done!")


def append_all(branch=None, work_dir="."):
    """Append all the current changes to the latest commit."""
    with GitContext(branch, work_dir) as gc:
        os.system(f"git add --all")
        os.system(f"git commit --amend --no-edit")
        info(f"Append_all on target branch {gc.branch} in dir {gc.work_dir} done!")


def delete_branch(branch=None, work_dir="."):
    """Delete branch from local and remote origin."""
    with GitContext(branch, work_dir) as gc:
        os.system(f"git branch -D {gc.branch}")
        info(
            f"Delete_branch on local target branch {gc.branch} in dir {gc.work_dir} done!"
        )
        os.system(f"git push -d origin {gc.branch}")
        info(
            f"Delete_branch on remote target branch {gc.branch} in dir {gc.work_dir} done!"
        )


# ----------------------------------------------------------------------------------------------------
# Main entry.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Handy utilities for Git.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(required=True, dest="subparser_name")

    # recommit
    parser_recommit = subparsers.add_parser(
        "recommit",
        aliases=["rc"],
        description=recommit.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_recommit.add_argument(
        "hash",
        # metavar="hash",
        type=str,
        help="hash of the commit after which all the commits are recommitted",
    )
    parser_recommit.add_argument(
        "--branch",
        "-b",
        type=str,
        default=None,
        help="working branch (default: current branch)",
    )
    parser_recommit.add_argument(
        "--work_dir",
        "-d",
        type=str,
        default=".",
        help="working directory (default: current working directory)",
    )
    parser_recommit.set_defaults(
        func=lambda args: recommit(args.hash, args.branch, args.work_dir)
    )

    # append_all
    parser_append_all = subparsers.add_parser(
        "append_all",
        aliases=["aa"],
        description=append_all.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_append_all.add_argument(
        "--branch",
        "-b",
        type=str,
        default=None,
        help="working branch (default: current branch)",
    )
    parser_append_all.add_argument(
        "--work_dir",
        "-d",
        type=str,
        default=".",
        help="working directory (default: current working directory)",
    )
    parser_append_all.set_defaults(
        func=lambda args: append_all(args.branch, args.work_dir)
    )

    # delete_branch
    parser_delete_branch = subparsers.add_parser(
        "delete_branch",
        aliases=["db"],
        description=delete_branch.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_delete_branch.add_argument(
        "--branch",
        "-b",
        type=str,
        default=None,
        help="working branch (default: current branch)",
    )
    parser_delete_branch.add_argument(
        "--work_dir",
        "-d",
        type=str,
        default=".",
        help="working directory (default: current working directory)",
    )
    parser_delete_branch.set_defaults(
        func=lambda args: delete_branch(args.branch, args.work_dir)
    )

    args = parser.parse_args()
    args.func(args)
