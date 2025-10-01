
# Run this file first
# It grabs the entire official repo of Pokerogue
# including the beta and localization repos

# After this is done:
# Step 1 is to run this script
# Step 2 is to run updateImages.py
# Step 3 is to run updateDatabase.py
# Step 4 is to run updateMoves.py
# Step 5 is to run updateLangs.py
# Step 6 is to push the changes to my github

import subprocess, os

def clone_or_update(repo_url, repo_dest, branch_name=None):
    # If folder exists but isn't a git repo, delete it
    if os.path.exists(repo_dest) and not os.path.exists(os.path.join(repo_dest, ".git")):
        print(f"Folder exists at {repo_dest}...")
        input("Can't continue without deleting that folder")

    # Reset everything in the folder, or clone it from scratch
    if os.path.exists(os.path.join(repo_dest, ".git")):
        print(f"\nResetting repository at {repo_dest}...")
        subprocess.run(["git", "-C", repo_dest, "fetch", "--depth", "1", "origin"], check=True)
        if branch_name:
            subprocess.run(["git", "-C", repo_dest, "checkout", branch_name], check=True)
            subprocess.run(["git", "-C", repo_dest, "reset", "--hard", f"origin/{branch_name}"], check=True)
        else:
            subprocess.run(["git", "-C", repo_dest, "reset", "--hard", "origin/HEAD"], check=True)
    else:
        print(f"\nCloning repository into {repo_dest}...")
        if branch_name:
            cmd = ["git", "clone", "--depth", "1", "-b", branch_name, repo_url, repo_dest]
        else:
            cmd = ["git", "clone", "--depth", "1", repo_url, repo_dest]
        subprocess.run(cmd, check=True)

    # Clean any untracked files/directories
    subprocess.run(["git", "-C", repo_dest, "clean", "-fdx"], check=True)

    # Initialize and update submodules recursively, force any local changes to be discarded
    subprocess.run(["git", "-C", repo_dest, "submodule", "update", "--init", "--recursive", "--force", "--depth", "1"], check=True)

# Main files
clone_or_update(
    repo_url="https://github.com/pagefaultgames/pokerogue.git",
    repo_dest="./game_files/live",
    branch_name="main"
)

# Localization files
clone_or_update(
    repo_url="https://github.com/pagefaultgames/pokerogue-locales.git",
    repo_dest="./game_files/locales"
)

# Beta files
clone_or_update(
    repo_url="https://github.com/pagefaultgames/pokerogue.git",
    repo_dest="./game_files/beta",
    branch_name="beta"
)

print('\n======= ALL DONE =======\n')