import random
import string
import subprocess

from utils.bash import confirm, echo
from utils.config import get_config


def _generate_tmp(length=5):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def _get_current_branch():
    try:
        return (
            subprocess.check_output(
                ["git", "symbolic-ref", "--short", "-q", "HEAD"],
            )
            .strip()
            .decode("utf-8")
        )
    except Exception as e:
        return None


def _get_all_branches(exclude_current=True):
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
    except Exception as e:
        return None


def create_new_feature_branch(*args):
    if len(args) == 1:
        return f"git checkout -b feature/{args[0]}"
    return echo("A feature branch name is required.")


def create_new_bug_branch(*args):
    if len(args) == 1:
        return f"git checkout -b bug/{args[0]}"
    return echo("A bug branch name is required.")


def clean_and_go_main(*args):
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


def squash(*args):
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


def undo(*args):
    if len(args) == 0:
        return "git checkout ."
    return f"git checkout {' '.join(args)}"


def delete_all_local_branches():
    branches = _get_all_branches(exclude_current=True)
    return f"git branch -D {' '.join(branches)}"


def show_git_tree():
    return "git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative --branches"


def clean_git_cache():
    if confirm(
        "Warning: This action will permanently delete all untracked files and directories. This cannot be undone. Do you want to proceed?"
    ):
        return "git clean -dfx"
    return echo("Operation canceled: No changes were made.")


def ignore_tracked_file(*args):
    return f"git update-index --assume-unchanged {args[0]}"


def update_current_branch(*args):
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


def configure_user(*args):
    profiles = get_config().get("git", {}).get("profiles", {})

    if len(args) == 1 and args[0] in profiles.keys():
        user = profiles[args[0]]
        return f"""
            git config user.email "{user['email']}"
            git config user.name "{user['name']}"
            {echo(f'New user: {user["name"]} ({user["email"]})')}
        """
    return echo(f"Profile not found. Available profiles: {', '.join(profiles.keys())}")
