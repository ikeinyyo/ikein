from .git import (
    clean_and_go_main,
    clean_git_cache,
    configure_user,
    create_new_bug_branch,
    create_new_feature_branch,
    delete_all_local_branches,
    fetch_and_rebase,
    ignore_tracked_file,
    show_git_tree,
    squash,
    undo,
    update_current_branch,
)

methods = {
    "newf": {
        "method": create_new_feature_branch,
        "info": "Creates a new feature branch.",
        "usage": "ikein newf <feature_name>",
    },
    "newb": {
        "method": create_new_bug_branch,
        "info": "Creates a new bug branch.",
        "usage": "ikein newb <bug_name>",
    },
    "clean": {
        "method": clean_and_go_main,
        "info": "Cleans the target branch and updates it from the remote repository.",
        "usage": "ikein clean [remote] [branch]",
    },
    "sync": {
        "method": fetch_and_rebase,
        "info": "Cleans the target branch and updates it from the remote repository.",
        "usage": "ikein sync [remote] [branch]",
    },
    "squash": {
        "method": squash,
        "info": "Performs a Git squash operation to combine multiple commits into one.",
        "usage": "ikein squash [remote] [branch]",
    },
    "undo": {
        "method": undo,
        "info": "Undoes changes made to the specified files in the repository.",
        "usage": "ikein undo [files]",
    },
    "branch-clean": {
        "method": delete_all_local_branches,
        "info": "Delete all local branches except the current one.",
        "usage": "ikein branch-clean",
    },
    "tree": {
        "method": show_git_tree,
        "info": "Display the Git commit tree.",
        "usage": "ikein tree",
    },
    "cache": {
        "method": clean_git_cache,
        "info": "Remove all untracked files and directories from the working directory in Git.",
        "usage": "ikein cache",
    },
    "lock": {
        "method": ignore_tracked_file,
        "info": "Temporarily ignore local changes to a tracked file without modifying .gitignore.",
        "usage": "ikein lock <file>",
    },
    "update": {
        "method": update_current_branch,
        "info": "Update the current branch with the latest changes from the specified remote.",
        "usage": "ikein update [remote]",
    },
    "user": {
        "method": configure_user,
        "info": "Update the Git user configuration (name and email) with the specified profile.",
        "usage": "ikein user [profile]",
    },
}
