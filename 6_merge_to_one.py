import os
import json
import subprocess

parameter_dict = {}
parameter_dict["pytorch"] = ["torch", "nn", "autograd", "optim", "functional", "dataloader", "datasets", "cuda"]
parameter_dict["tensorflow"] = ["tf", "tensorflow", "keras", "layers", "models"]

data_list = []
for frame_work in parameter_dict.keys():
    for match_word in parameter_dict[frame_work]:
        path = f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\contain_{match_word}_dot_core_change\\"
        files = os.listdir(path)
        for file in files:
            if not file.endswith(".json"):
                continue
            with open(path+file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for d in data:
                    d["file"] = file
                    d["label"]="no"
                    d["comments"]=""
                    d["framework"]=frame_work
                    d["match_word"]=match_word
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

