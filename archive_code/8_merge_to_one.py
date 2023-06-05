import os
import json
import subprocess

data_list = []
for root, dirs, files in os.walk("C:\@code\APIMISUSE\data\misuse_jsons"):
    for file in files:
        # exclude merged.json
        if file == "merged.json":
            continue
        if not file.endswith(".json"):
            continue
        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
            data = json.load(f)
            for d in data:
                d["file"] = os.path.join(root, file)
                d["label"]="no"
                d["comments"]=""
            data_list+= data
#dump data_list to json
with open("C:\@code\APIMISUSE\data\misuse_jsons\merged.json", "w", encoding="utf-8") as f:
    json.dump(data_list, f, indent=4)
total_length = 0

# load merged.json
with open("C:\@code\APIMISUSE\data\misuse_jsons\merged.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    total_length += len(data)

print(total_length)

