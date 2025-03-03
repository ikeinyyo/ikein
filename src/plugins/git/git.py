import random
import string
import subprocess
from typing import List, Optional

from utils.bash import confirm, echo
from utils.config import get_config


def _generate_tmp(length: int = 5) -> str:
    """
    Generates a temporary string of a specified length using random letters and digits.

    Parameters:
        length (int): The length of the temporary string to generate. Default is 5.

    Returns:
        str: A temporary string of random letters and digits.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def _get_current_branch() -> Optional[str]:
    """
    Retrieves the current git branch.

    Returns:
        str: The name of the current branch, or None if there is an error retrieving the branch.
    """
    try:
        return (
            subprocess.check_output(
                ["git", "symbolic-ref", "--short", "-q", "HEAD"],
            )
            .strip()
            .decode("utf-8")
        )
    except Exception:
        return None


def _get_all_branches(exclude_current: bool = True) -> Optional[List[str]]:
    """
    Retrieves a list of all git branches.

    Parameters:
        exclude_current (bool): If True, the current branch will be excluded from the list. Default is True.

    Returns:
        List[str]: A list of branch names, or None if there was an error retrieving the branches.
    """
    try:
        return (
            subprocess.check_output(
                "git branch | grep -v \* | xargs" if exclude_current else "git branch",
                shell=True,
            )
            .decode("utf-8")
            .strip()
            .replace("*", "")
            .split()
        )
    except Exception:
        return None


def create_new_feature_branch(*args: str) -> str:
    """
    Creates a new git feature branch.

    Parameters:
        args (str): The name of the feature branch to create.

    Returns:
        str: The git command to create the feature branch, or an error message if no branch name is provided.
    """
    if len(args) == 1:
        return f"git checkout -b feature/{args[0]}"
    return echo("A feature branch name is required.")


def create_new_bug_branch(*args: str) -> str:
    """
    Creates a new git bug branch.

    Parameters:
        args (str): The name of the bug branch to create.

    Returns:
        str: The git command to create the bug branch, or an error message if no branch name is provided.
    """
    if len(args) == 1:
        return f"git checkout -b bug/{args[0]}"
    return echo("A bug branch name is required.")


def clean_and_go_main(*args: str) -> str:
    """
    Cleans up and switches to the main branch.

    Parameters:
        args (str): The remote or branch name to use when switching to the main branch.

    Returns:
        str: A series of git commands to clean up and switch to the main branch, with the provided options.
    """
    tmp = _generate_tmp()
    if len(args) == 1:
        return f"""
            git fetch origin
            git branch -D {tmp} || true
            git checkout -b {tmp}
            git branch -D "{args[0]}" || true
            git checkout --track origin/{args[0]}
            git branch -D {tmp} || true
        """
    elif len(args) == 2:
        return f"""
            git fetch {args[0]}
            git branch -D {tmp} || true
            git checkout -b {tmp}
            git branch -D "{args[1]}" || true
            git checkout --track {args[0]}/{args[1]}
            git branch -D {tmp} || true
        """
    return f"""
        git fetch origin
        git branch -D {tmp} || true
        git checkout -b {tmp}
        git branch -D "main"
        git checkout --track origin/main
        git branch -D {tmp} || true
    """


def squash(*args: str) -> str:
    """
    Squashes git commits into a single commit.

    Parameters:
        args (str): The branch or remote to rebase onto.

    Returns:
        str: The git command to squash commits, or an error message if no valid arguments are provided.
    """
    if len(args) == 1:
        return f"""
            git fetch origin
            git rebase -i origin/{args[0]}
        """
    elif len(args) == 2:
        return f"""
            git fetch origin
            git rebase -i {args[0]}/{args[1]}
        """
    return f"""
        git fetch origin
        git rebase -i origin/main
    """


def undo(*args: str) -> str:
    """
    Undoes changes in the working directory.

    Parameters:
        args (str): A list of specific files to revert, or none to revert all changes.

    Returns:
        str: The git command to undo changes, or a command to undo specific files.
    """
    if len(args) == 0:
        return "git checkout ."
    return f"git checkout {' '.join(args)}"


def delete_all_local_branches() -> str:
    """
    Deletes all local git branches except for the current branch.

    Returns:
        str: The git command to delete all local branches.
    """
    branches = _get_all_branches(exclude_current=True)
    return f"git branch -D {' '.join(branches)}" if branches else ""


def show_git_tree() -> str:
    """
    Shows the git commit tree with detailed information.

    Returns:
        str: The git command to display the commit tree.
    """
    return "git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative --branches"


def clean_git_cache() -> str:
    """
    Cleans the git cache by removing untracked files and directories.

    Returns:
        str: The git command to clean the cache, or a message if the operation is canceled.
    """
    if confirm(
        "Warning: This action will permanently delete all untracked files and directories. This cannot be undone. Do you want to proceed?"
    ):
        return "git clean -dfx"
    return echo("Operation canceled: No changes were made.")


def ignore_tracked_file(*args: str) -> str:
    """
    Marks a file as assumed unchanged in git.

    Parameters:
        args (str): The file to mark as unchanged.

    Returns:
        str: The git command to ignore the tracked file.
    """
    return f"git update-index --assume-unchanged {args[0]}"


def update_current_branch(*args: str) -> str:
    """
    Updates the current branch by switching to the specified branch in a remote.

    Parameters:
        args (str): The remote or branch name to fetch and switch to.

    Returns:
        str: The git command to update the current branch.
    """
    current_branch = _get_current_branch()
    tmp = _generate_tmp()

    if len(args) == 1:
        return f"""
            git fetch {args[0]}
            git checkout -b {tmp}
            git branch -D {current_branch}
            git checkout --track {args[0]}/{current_branch}
            git branch -D {tmp}
        """
    return f"""
        git fetch origin
        git checkout -b {tmp}
        git branch -D {current_branch}
        git checkout --track origin/{current_branch}
        git branch -D {tmp}
    """


def configure_user(*args: str) -> str:
    """
    Configures the git user profile based on the given profile name.

    Parameters:
        args (str): The profile name to use for configuring the git user.

    Returns:
        str: The git commands to configure the user, or an error message if the profile is not found.
    """
    profiles = get_config().get("git", {}).get("profiles", {})

    if len(args) == 1 and args[0] in profiles.keys():
        user = profiles[args[0]]
        return f"""
            git config user.email "{user['email']}"
            git config user.name "{user['name']}"
            {echo(f'New user: {user["name"]} ({user["email"]})')}
        """
    return echo(f"Profile not found. Available profiles: {', '.join(profiles.keys())}")
