import os

with open('data\\repo_tensorflow_list\\repo_name_response_tf_json_2.txt', 'r') as f:
# with open('data\\repo_pytorch_list\\repo_name_response_json_2.txt', 'r') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

os.chdir("data\\repo_tensorflow_test")
# os.chdir("data\\repo_pytorch_test")
repo_list=lines[:50]
for repo in repo_list:
    print(repo)
    if  os.path.exists(f"data\\repo_tensorflow_test\\{repo.split('/')[1]}"):
    # if  os.path.exists(f"data\\repo_pytorch_test\\{repo.split('/')[1]}"):
        continue
    os.system(f"git clone https://github.com/{repo}.git")