import os
import json

output_path='C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v2_compare_auto_category.json'

# read
data_dict = {}
with open("C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual_deduplica_reduced_category_strict_general_case_Moshi.json", encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        data_dict[line["number"]] = line

data_stage_2_dict = {}
with open('C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v2_auto_category_2.json', encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    print(len(data))
    for line in data:
        data_stage_2_dict[line["number"]] = line

with open(output_path, 'w', encoding="utf-8") as f:
    f.write("")


# merge data_stage_1_dict into data_dict by key
for key in data_dict.keys():
    if key in data_stage_2_dict.keys():
        data_dict[key]["code_change_explaination"] = data_stage_2_dict[key]["code_change_explaination"]

# convert data_dict to list
data = []
for key in data_dict.keys():
    if "code_change_explaination" in data_dict[key].keys():
        data.append(data_dict[key])

print(len(data))
print(data[0].keys())

API_method_list = []
with open('C:\@code\APIMISUSE\data\API_method_list_torch.txt', encoding="utf-8") as f:
    API_data = f.readlines()
    for x in API_data:
        if x != "\n":
            API_method_list.append(x.strip().lower())
with open('C:\@code\APIMISUSE\data\API_method_list_tf.txt', encoding="utf-8") as f:
    API_data = f.readlines()
    for x in API_data:
        if x != "\n":
            API_method_list.append(x.strip().lower())

counter = 0
y_test = []
y_pred = []
category_list = []
no_API_counter = 0
wrong_manual_counter = 0
wrong_auto_counter = 0
for idx in range(len(data[:])):
    if "code_change_explaination" not in data[idx].keys():
        break

    manual_comments = data[idx]["comments"]
    change = data[idx]["change"]
    number = data[idx]["number"]

    # print("number: ", number)
    # print("manual_comments: ",manual_comments)
    # print("change: ")
    # for x in change:
    #     print(x)
    code_change_explaination = data[idx]["code_change_explaination"]
    res_list = code_change_explaination.split("\n")
    Symptom = ""
    Motivation = ""
    for x in res_list:
        if x.startswith("Symptom"):
            Symptom = x
            Symptom = Symptom.split(": ")[1].replace("\"", "").replace(",", "")
        if x.startswith("Motivation"):
            Motivation = x
            Motivation = Motivation.split(": ")[1].replace("\"", "").replace(",", "")
    if Symptom ==""or Motivation == "":
        continue
    else:
        data[idx]["Symptom"] = Symptom
        data[idx]["Motivation"] = Motivation
    # keep keys number label change Symptom Motivation
    data[idx] = {key: data[idx][key] for key in ["number","comments","commit_message", "label", "change", "Symptom", "Motivation"]}

#write data to output_path 

# get Motivation as a list
Motivation_list = []
Symptom_list = []
for idx in range(len(data[:])):
    if "Motivation" in data[idx].keys():
        Motivation_list.append(data[idx]["Motivation"])
    if "Symptom" in data[idx].keys():
        Symptom_list.append(data[idx]["Symptom"])
print(len(Motivation_list))
print(len(Symptom_list))
#get frequency counter in Motivation_list
from collections import Counter
Motivation_counter = Counter(Motivation_list)
Symptom_counter = Counter(Symptom_list)
print(Motivation_counter)
print("=====================================")

print(Symptom_counter)


with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)