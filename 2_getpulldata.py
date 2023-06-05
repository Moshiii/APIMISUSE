import os

with open('data\\repo_tensorflow_list\\repo_name_response_tf_json_0.txt', 'r') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

repo_list=lines
for repo in repo_list:
    print(repo)
    if  os.path.exists(f"data\\repo_tensorflow\\{repo.split('/')[1]}"):
        continue
    os.system(f"git clone https://github.com/{repo}.git")