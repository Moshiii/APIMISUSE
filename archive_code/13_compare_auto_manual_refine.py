import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from collections import Counter
import os
import json
# load C:\@code\APIMISUSE\data\misuse_jsons\auto_langchain\misuse_classification.json
with open('C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_classification_v2_VSDB_diff_only_refine.json', encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    for idx in range(len(data)):
        data[idx] = json.loads(data[idx])
    # data = [json.loads(line) for line in data]

# load C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual_deduplica_reduced_category.json
with open('C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v2_compare.json', encoding="utf-8") as f:
    data_manual = f.readlines()
    data_manual = [line for line in data_manual if line != "\n"]
    data_manual = [json.loads(line) for line in data_manual]
    data_manual = [line for line in data_manual if line["manual_label"] != line["auto_label"]]

# load torch list C:\@code\APIMISUSE\data\API_method_list_torch.txt
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

no_API_counter = 0
wrong_manual_counter = 0
wrong_auto_counter = 0
y_test = []
y_pred = []
for idx in range(len(data)):
    number = data[idx]["number"]
    for data_manual_idx in data_manual:
        if data_manual_idx["number"] == number:
            break


    print(idx)
    if "if_API_misuse_fix" in data[idx]["misuse_classification"]:
        auto_label = data[idx]["misuse_classification"]['if_API_misuse_fix']
    if "If_API_misuse_fix" in data[idx]["misuse_classification"]:
        auto_label = data[idx]["misuse_classification"]['If_API_misuse_fix']
    auto_label = auto_label.strip().lower().replace(
        " ", "").replace("\n", "").replace("na", "no")

    manual_label = data_manual_idx["manual_label"]
    change = data_manual_idx["change"]
    added = data_manual_idx["added"]
    removed = data_manual_idx["removed"]
    number = data_manual_idx["number"]
    check_API ="False"
    for API_name in API_method_list:

        if API_name in added:
            check_API="True"
        if API_name in removed:
            check_API="True"
    if check_API == "False":
        no_API_counter += 1
        if manual_label == "yes":
            wrong_manual_counter += 1
        if auto_label == "yes":
            wrong_auto_counter += 1
            auto_label = "no"

    y_test.append(manual_label)
    y_pred.append(auto_label)

    if manual_label == "no" and auto_label == "yes":
        print("number: ")
        print(number)
        print("change: ")
        print(change)
        print("code explain: ")
        print(list(data_manual_idx.values())[-1])
        print("reason of fix: ")
        print(list(data[idx]["misuse_classification"].values())[-1])

# frequency counter
print(Counter(y_test))
print(Counter(y_pred))
print("no_API_counter", no_API_counter)
print("wrong_manual_counter", wrong_manual_counter)
print("wrong_auto_counter", wrong_auto_counter)

conf_mat = confusion_matrix(y_test, y_pred)
print(conf_mat)
