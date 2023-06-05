import json
import collections
import os


bug_fix_path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/API_misuse_bug_fix.json"
result_path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/API_misuse_bug_detection_result_tensorflow.json"
path = "C:\\@code\\APIMISUSE\\data\\repo_tensorflow"
file_list_log=[]
bug_list = []
fix_list = []
result = []
match_count=0

with open(bug_fix_path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

for x in data:
    bug_list.append(x["bug"])
    fix_list.append(x["fix"])

#get all folder path in C:\@code\APIMISUSE\data\repo_pytorch
folder_list = []
for root, dirs, files in os.walk(path):
    for dir in dirs:
        folder_list.append(os.path.join(root, dir))

print("folder count ",len(folder_list))
for idx,folder_path in enumerate(folder_list): 
        
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_list.append(os.path.join(root, file))
    file_list_log+=file_list
    print("current folder",folder_path)
    print("current progress",idx,"/",len(folder_list),"file count ",len(file_list),"bug count ",match_count)

    for idx,x in enumerate(file_list):
        # print("current progress",idx,"/",len(file_list))
        with open(x, "r", encoding="utf-8") as f:
            file_content = f.read()
            file_content = file_content.split("\n")
        for idx,bug in enumerate(bug_list):
            fix = fix_list[idx]
            if bug in file_content:
                match_count+=1
                result.append({"bug": bug, "fix": fix, "file_path": x})

# write result to json file
with open(result_path, "w", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=4))
with open("file_list_log.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(file_list_log, indent=4))
