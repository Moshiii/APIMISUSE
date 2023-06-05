import os
import json
import re
pattern_0 = r"\.[a-zA-Z0-9_]+\("
pattern_1 = r"\.[a-zA-Z0-9_]+\["
pattern_2 = r"[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+"


parameter_dict = {}
parameter_dict["pytorch"] = ["torch", "nn", "autograd", "optim", "functional", "dataloader", "datasets", "cuda"]
parameter_dict["tensorflow"] = ["tf", "tensorflow", "keras", "layers", "models"]

# for each framework for each parameter
for frame_work in parameter_dict.keys:
    for match_word in parameter_dict[frame_work]:
        
        match_counter=0
        summary_file = f"C:\@code\APIMISUSE\\filter_by_fix_{match_word}.json" 
        sumamry=[]
        files = os.listdir(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\contain_{match_word}_dot_core_change")
        for file in files:
            with open(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\contain_{match_word}_dot_core_change\{file}", "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                pos_lines=0
                neg_lines=0
                #=================if no core chage then skip===================================
                if len(item["core_change"]) == 0:
                    continue
                for line in item["core_change"]:
                    if line.startswith("+"):
                        pos_lines+=1
                    if line.startswith("-"):
                        neg_lines+=1
                #=================if only add or remove then skip===================================
                if pos_lines == 0 or neg_lines == 0:
                    continue
                
                item["repo_name"] = file.replace(".txt.json", "")
                #=================if about doc then skip===================================
                if "doc" in item["commit_message"].lower():
                    continue

                if "fix" in item["commit_message"].lower():
                    core_change_length = len(item["core_change"])
                    # if core_change_length > 4:
                        # continue
                    core_change_neg_string = " ".join([x for x in item["core_change"] if x.startswith("-")])
                    core_change_pos_string = " ".join([x for x in item["core_change"] if x.startswith("+")])
                    
                    method_neg_name = re.findall(pattern_0, core_change_neg_string)
                    method_neg_name += re.findall(pattern_1, core_change_neg_string)
                    method_neg_name += re.findall(pattern_2, core_change_neg_string)

                    api_neg_name = re.findall(pattern_0, core_change_neg_string)

                    method_pos_name = re.findall(pattern_0, core_change_pos_string)
                    method_pos_name += re.findall(pattern_1, core_change_pos_string)
                    method_pos_name += re.findall(pattern_2, core_change_pos_string)

                    api_pos_name = re.findall(pattern_0, core_change_pos_string)
                    

                    item["method_neg_name"] = method_neg_name
                    item["method_pos_name"] = method_pos_name

                    item["api_neg_name"] = api_neg_name
                    item["api_pos_name"] = api_pos_name

                    match_counter+=1

                    sumamry.append(item)
        print(match_counter)

with open(summary_file, "w", encoding="utf-8") as f:
    json.dump(sumamry, f, indent=4)