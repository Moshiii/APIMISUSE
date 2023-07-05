import os
import json


# read
data_dict={}
with open("C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual_deduplica_reduced_category_strict_general_case_Moshi.json", encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        data_dict[line["number"]] = line

data_stage_2_dict={}
with open('C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v2_stage_2_classification_template_2_5.json', encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        data_stage_2_dict[line["number"]] = line

#reset file 'C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v2_compare.json'
with open('C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v2_compare.json', 'w', encoding="utf-8") as f:
    f.write("")
    

# merge data_stage_1_dict into data_dict by key
for key in data_dict.keys():
    if key in data_stage_2_dict.keys():
        data_dict[key]["code_change_explaination"] = data_stage_2_dict[key]["code_change_explaination"]
        data_dict[key]["misuse_classification"] = data_stage_2_dict[key]["misuse_classification"]

# convert data_dict to list
data = []
for key in data_dict.keys():
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

counter=0
y_test = []
y_pred = []
no_API_counter = 0
wrong_manual_counter = 0
wrong_auto_counter = 0
for idx in range(len(data[:100])):

    manual_label = data[idx]["label"]
    manual_label = manual_label.strip().lower()
    if manual_label == "":
        break
    if not "misuse_classification" in data[idx].keys():
        break

    auto_label = list(data[idx]["misuse_classification"].values())[0]
    auto_label = auto_label.strip().lower().replace(" ","").replace("\n","").replace("na","no")
    reason_of_fix = list(data[idx]["misuse_classification"].values())[1]

    manual_comments = data[idx]["comments"]
    change = data[idx]["change"]
    number = data[idx]["number"]

    if auto_label!=manual_label:
        # print()
        print("number: ",number)
        # print("manual_comments: ",manual_comments)
        print("change: ")
        for x in change:
            print(x)
        code_change_explaination = data[idx]["code_change_explaination"]
        code_change_explaination = code_change_explaination.split(".")[0]
        print(code_change_explaination)
        print(reason_of_fix)
        print("auto_label: ", auto_label)
        print("manual_label: ", manual_label)
        print()

    changed = ""
    removed = ""
    added = ""

    for j in range(0, len(change)):
        line = change[j]
        changed += "{}\n".format(change[j])
        if line.startswith("-"):
            removed += "{}\n".format(change[j])
        if line.startswith("+"):
            added += "{}\n".format(change[j])
    
    output = {
        "number": number,
        "manual_comments": manual_comments,
        "change": changed,
        "removed": removed,
        "added": added,
        "manual_label": manual_label,
        "auto_label": auto_label,
        "code_change_explaination": data[idx]["code_change_explaination"]
    }
    check_API ="False"
    for API_name in API_method_list:

        if API_name in added:
            check_API="True"
        if API_name in removed:
            check_API="True"
        # if API_name in changed:
        #     check_API="True"
    if check_API == "False":
        no_API_counter += 1
        if manual_label == "yes":
            wrong_manual_counter += 1
        if auto_label == "yes":
            wrong_auto_counter += 1
            # auto_label = "no"

    y_test.append(manual_label)
    y_pred.append(auto_label)

    with open('C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v2_compare.json', 'a') as f:
        json.dump(output, f)
        f.write(os.linesep)

# #frequency counter
from collections import Counter
print("total: ",len(y_test))
print(Counter(y_test))
print(Counter(y_pred))

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
conf_mat = confusion_matrix(y_test, y_pred)
print(conf_mat)
# sns.heatmap(conf_mat, square=True, annot=True, cmap='Blues', fmt='d', cbar=False)
# plt.show()
