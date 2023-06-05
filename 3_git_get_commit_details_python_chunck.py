import os
import re
import subprocess

# Output all commit hashes to a file
os.chdir("data/repo_tensorflow/")
# get all the repo names in the repo folder
repo_names = os.listdir()
for repo_name in repo_names:
    git_repo_path = repo_name
    os.chdir(git_repo_path)
    print(repo_name)
    if os.path.exists(f"C:\@code\APIMISUSE\data\commit\python_chunks\\tensorflow\\all_commit\{repo_name}.txt"):
        print("repo_name exists: ",repo_name)
        os.chdir("..")
        continue
    os.system("git log --format='%H' > commit_hashes.txt")
    result=[]
    # Loop through each commit hash in the file
    with open("commit_hashes.txt", "r",encoding="utf-8") as f:
        for commit_hash in f.readlines():
            commit_hash = str(commit_hash.strip())
            commit_hash = commit_hash[1:-1]
            command = ["git", "show", commit_hash]
            try:
                output = subprocess.check_output(command, universal_newlines=True, encoding="utf-8")
            except:
                continue
            commit_details = output
            diff_files = commit_details.split("diff --git ")
            for diff_file in diff_files:
                if len(diff_file) > 2000:
                    continue
                lines = diff_file.split("\n")
                line = lines[0].split()[-1]
                if not line.endswith(".py") and not line.endswith(".ipynb"):
                    continue
                result.append("=====================================")
                result.append("commit_hash is : "+commit_hash)
                result.append(diff_file)
    name=git_repo_path
    with open(f"C:\\@code\\APIMISUSE\\data\\commit\\python_chunks\\tensorflow\\all_commit\\{name}.txt", "w", encoding="utf-8") as result_file:
        result_file.write("\n".join(result))
    os.chdir("..")