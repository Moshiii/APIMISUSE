from collections import Counter
from sklearn.metrics import confusion_matrix, accuracy_score
import json

old_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\manual\misuse_v3_classification_stage_2_minor_change_old_2.json"
new_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\manual\misuse_v3_classification_stage_2_minor_change.json"

# old_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\manual\misuse_v3_classification_stage_2_if_api_fix_old_2.json"
# new_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\manual\misuse_v3_classification_stage_2_if_api_fix.json"

# read old
data_stage_3_dict_old = {}
with open(old_path, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        data_stage_3_dict_old[line["number"]] = line
old_list = []
for values in data_stage_3_dict_old.values():
    answer = values["answer"]
    answer = answer.lower().replace(".", "")
    if "yes" in answer:
        answer = "yes"
    elif "no" in answer:
        answer = "no"
    old_list.append(answer)


data_stage_3_dict = {}
with open(new_path, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        data_stage_3_dict[line["number"]] = line

new_list = []
for values in data_stage_3_dict.values():
    answer = values["answer"]
    answer = answer.lower().replace(".", "")
    if "yes" in answer:
        answer = "yes"
    elif "no" in answer:
        answer = "no"
    new_list.append(answer)

print(len(data_stage_3_dict_old))
print(len(data_stage_3_dict))
# get confusion matrix

print(Counter(old_list))
print(Counter(new_list))
print(confusion_matrix(old_list, new_list))
print(accuracy_score(old_list, new_list))
