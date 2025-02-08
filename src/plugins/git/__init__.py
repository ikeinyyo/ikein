from .git import (
    clean_and_go_main,
    clean_git_cache,
    configure_user,
    create_new_bug_branch,
    create_new_feature_branch,
    delete_all_local_branches,
    ignore_tracked_file,
    show_git_tree,
    squash,
    undo,
    update_current_branch,
)

methods = {
    "gnewf": {
        "method": create_new_feature_branch,
        "info": "Creates a new feature branch.",
        "usage": "ikein gnewf <feature_name>",
    },
    "gnewb": {
        "method": create_new_bug_branch,
        "info": "Creates a new bug branch.",
        "usage": "ikein gnewb <bug_name>",
    },
    "gclean": {
        "method": clean_and_go_main,
        "info": "Cleans the target branch and updates it from the remote repository.",
        "usage": "ikein gclean [remote] [branch]",
    },
    "gsquash": {
        "method": squash,
        "info": "Performs a Git squash operation to combine multiple commits into one.",
        "usage": "ikein gsquash [remote] [branch]",
    },
    "gundo": {
        "method": undo,
        "info": "Undoes changes made to the specified files in the repository.",
        "usage": "ikein gundo [files]",
    },
    "gbclean": {
        "method": delete_all_local_branches,
        "info": "Delete all local branches except the current one.",
        "usage": "ikein gbclean",
    },
    "gtree": {
        "method": show_git_tree,
        "info": "Display the Git commit tree.",
        "usage": "ikein gtree",
    },
    "gcache": {
        "method": clean_git_cache,
        "info": "Remove all untracked files and directories from the working directory in Git.",
        "usage": "ikein gcache",
    },
    "glock": {
        "method": ignore_tracked_file,
        "info": "Temporarily ignore local changes to a tracked file without modifying .gitignore.",
        "usage": "ikein glock <file>",
    },
    "gupdate": {
        "method": update_current_branch,
        "info": "Update the current branch with the latest changes from the specified remote.",
        "usage": "ikein gupdate [remote]",
    },
    "guser": {
        "method": configure_user,
        "info": "Update the Git user configuration (name and email) with the specified profile.",
        "usage": "ikein guser [profile]",
    },
}
