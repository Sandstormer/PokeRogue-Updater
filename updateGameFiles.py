
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

# Get the main files
repo_url = "https://github.com/pagefaultgames/pokerogue.git"  # Replace with the actual repo URL
repo_dest = "./game_files/live"  # Where to save the entire cloned repo
branch_name = "main"  # Replace with the desired branch name
if os.path.exists(os.path.join(repo_dest, ".git")):
    print("\nUpdating main repository...")
    subprocess.run(["git", "-C", repo_dest, "checkout", branch_name], check=True)
    subprocess.run(["git", "-C", repo_dest, "pull"], check=True)
else:
    print("\nCloning main repository...")
    subprocess.run(["git", "clone", "-b", branch_name, repo_url, repo_dest], check=True)

# Get the localization files
repo_url_loc = "https://github.com/pagefaultgames/pokerogue-locales.git"  # Replace with the actual repo URL
repo_dest_loc = "./game_files/locales"  # Where to save the entire cloned repo
if os.path.exists(os.path.join(repo_dest_loc, ".git")):
    print("\nUpdating localization repository...")
    subprocess.run(["git", "-C", repo_dest_loc, "pull"], check=True)
else:
    print("\nCloning localization repository...")
    subprocess.run(["git", "clone", repo_url_loc, repo_dest_loc], check=True)

# Get the beta files
repo_url = "https://github.com/pagefaultgames/pokerogue.git"  # Replace with the actual repo URL
repo_dest = "./game_files/beta"  # Where to save the entire cloned repo
branch_name = "beta"  # Replace with the desired branch name
if os.path.exists(os.path.join(repo_dest, ".git")):
    print("\nUpdating beta repository...")
    subprocess.run(["git", "-C", repo_dest, "checkout", branch_name], check=True)
    subprocess.run(["git", "-C", repo_dest, "pull"], check=True)
else:
    print("\nCloning beta repository...")
    subprocess.run(["git", "clone", "-b", branch_name, repo_url, repo_dest], check=True)

print('\n======= ALL DONE =======\n')