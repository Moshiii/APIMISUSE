from sklearn.metrics import confusion_matrix, plot_confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score
from collections import Counter
import json
base_path ="C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\manual\\"
input_path = base_path + "manual_data_1k.json"
manual_path = base_path + "manual_invest_data_1k.json"
prediction_path = base_path + 'merged_split_hunk_AST_filter_manual_Moshi_result.json'


def parse_action(comments):
    if comments.startswith("add"):
        action = "add"
    elif comments.startswith("remove"):
        action = "remove"
    elif comments.startswith("change"):
        action = "change"
    elif comments.startswith("update"):
        action = "update"
    else:
        action = "None"
    return action


def parse_element(comments):
    if "call" in comments:
        api_object = "API call"
    elif "param" in comments:
        api_object = "API Parameter"
    elif "condition" in comments:
        api_object = "API Condition Check"
    else:
        api_object = "None"
    return api_object


data_dict = {}
with open(input_path, encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        data_dict[line["number"]] = line
manual_dict = {}
with open(manual_path, encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        manual_dict[line["number"]] = line

# merge
for key in data_dict.keys():
    if key in manual_dict.keys():
        data_dict[key]["Manual_Symptom"] = manual_dict[key]["Manual_Symptom"]
        data_dict[key]["Manual_Root_Cause"] = manual_dict[key]["Manual_Root_Cause"]
    if not key in manual_dict.keys():
        data_dict[key]["Manual_Symptom"] = "None"
        data_dict[key]["Manual_Root_Cause"] = "None"

stage_3_dict = {}
with open(prediction_path, encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        stage_3_dict[line["number"]] = line

data = []
if_API_misuse_classification_label_list = []
if_API_misuse_classification_pred_list = []

action_classification_label_list = []
element_classification_label_list = []
symptom_classification_label_list = []
root_cause_classification_label_list = []

action_classification_pred_list = []
element_classification_pred_list = []
symptom_classification_pred_list = []
root_cause_classification_pred_list = []

for key in data_dict.keys():
    if_API_misuse_classification_label_list.append(data_dict[key]["label"])
    if not key in stage_3_dict.keys():
        if_API_misuse_classification_pred_list.append("no")
    if key in stage_3_dict.keys():
        if_API_misuse_classification_pred_list.append("yes")

        label_item = data_dict[key]
        comments = label_item["comments"]
        comments = comments.split("for")[0]

        action_label = parse_action(comments).lower().strip()
        element_label = parse_element(comments).lower().strip()
        symptom_label = label_item["Manual_Symptom"].lower().strip()
        root_cause_label = label_item["Manual_Root_Cause"].lower().strip()

        pred_item = stage_3_dict[key]
        action_pred = pred_item["Action"].lower().strip()
        element_pred = pred_item["Element"].lower().strip()
        symptom_pred = pred_item["Symptom"].lower().strip()
        root_cause_pred = pred_item["Root_Cause"].lower().strip()


        if action_label == "none" or element_label == "none" or symptom_label == "none" or root_cause_label == "none":
            continue

        action_classification_label_list.append(action_label)
        element_classification_label_list.append(element_label)
        symptom_classification_label_list.append(symptom_label)
        root_cause_classification_label_list.append(root_cause_label)

        action_classification_pred_list.append(action_pred)
        element_classification_pred_list.append(element_pred)
        symptom_classification_pred_list.append(symptom_pred)
        root_cause_classification_pred_list.append(root_cause_pred)

        

# get confusion matrix of API misuse classification
# print(confusion_matrix(if_API_misuse_classification_label_list, if_API_misuse_classification_pred_list))
print("accuracy: ", accuracy_score(if_API_misuse_classification_label_list,
      if_API_misuse_classification_pred_list))

# get confusion matrix of action classification
print("Action classification")
# print(confusion_matrix(action_classification_label_list, action_classification_pred_list))
print("accuracy: ", accuracy_score(
    action_classification_label_list, action_classification_pred_list))
print(Counter(action_classification_label_list))
print(Counter(action_classification_pred_list))

# get confusion matrix of element classification
print("Element classification")
# print(confusion_matrix(element_classification_label_list, element_classification_pred_list))
print("accuracy: ", accuracy_score(
    element_classification_label_list, element_classification_pred_list))

# get confusion matrix of symptom classification
print("Symptom classification")
# print(confusion_matrix(symptom_classification_label_list, symptom_classification_pred_list))
print("accuracy: ", accuracy_score(
    symptom_classification_label_list, symptom_classification_pred_list))

# get confusion matrix of root cause classification
print("Root cause classification")
# print(confusion_matrix(root_cause_classification_label_list, root_cause_classification_pred_list))
print("accuracy: ", accuracy_score(
    root_cause_classification_label_list, root_cause_classification_pred_list))
