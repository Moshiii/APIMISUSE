import collections
from sklearn.metrics import confusion_matrix
from collections import Counter
import json


base_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\\calib\\"
input_path = base_path + "calib_data_1k.json"
# stage_3_fix_pattern_path = base_path + "misuse_v3_classification_stage_3_fix_pattern.json"
stage_3_path = base_path + "misuse_v3_classification_stage_3.json"
stage_2_path = base_path + "misuse_v3_classification_stage_2.json"
output_path = base_path + "misuse_v3_classification_stage_3_result.json"


def parse_symptom(Symptom):

    if "no" in Symptom or "No" in Symptom:
        Symptom = "None"
    elif "Program Crash" in Symptom:
        Symptom = "Program Crash"
    elif "Unexpected Output" in Symptom:
        Symptom = "Unexpected Output"
    elif "Return Warning" in Symptom:
        Symptom = "Return Warning"
    elif "Low Efficiency" in Symptom:
        Symptom = "Low Efficiency"
    else:
        Symptom = "None"
    return Symptom


def parse_Root_Cause(Root_Cause):
    if "no" in Root_Cause or "No" in Root_Cause:
        Root_Cause = "None"
    elif "Deprecation Management Error" in Root_Cause:
        Root_Cause = "Deprecation Management Error"
    elif "Management Error" in Root_Cause:
        Root_Cause = "Deprecation Management Error"
    elif "Data Conversion Error" in Root_Cause:
        Root_Cause = "Data Conversion Error"
    elif "Device Management Error" in Root_Cause:
        Root_Cause = "Device Management Error"
    elif "State Handling Error" in Root_Cause:
        Root_Cause = "State Handling Error"
    elif "Algorithm Error" in Root_Cause:
        Root_Cause = "Algorithm Error"
    elif "Null Reference Error" in Root_Cause:
        Root_Cause = "Null Reference Error"
    elif "Argument error" in Root_Cause:
        Root_Cause = "Argument Error"
    elif "Argument Error" in Root_Cause:
        Root_Cause = "Argument Error"
    else:
        Root_Cause = "None"
    return Root_Cause


def parse_symptom_Root_Cause(stage_3_answer):

    answer_list = stage_3_answer.split("\n")
    Symptom = ""
    Root_Cause = ""

    for y in answer_list:
        if "Symptom: " in y:
            Symptom = y.replace("Symptom: ", "")
        if "Motivation: " in y:
            Root_Cause = y.replace("Motivation: ", "")

    Symptom = parse_symptom(Symptom)
    Root_Cause = parse_Root_Cause(Root_Cause)

    return Symptom, Root_Cause


def parse_Action(Action):
    Action = Action.replace(" ", "").lower()

    if "removal" in Action:
        Action = "Removal"
    elif "addition" in Action:
        Action = "Addition"
    elif "change" in Action:
        Action = "Change"
    elif "replacement" in Action:
        Action = "Change"
    elif "update" in Action:
        Action = "update"
    else:
        Action = "None"

    return Action


def parse_Element(Element):
    Element = Element.lower()

    if "api call" in Element:
        Element = "API Call"
    elif "api parameter" in Element:
        Element = "API Parameter"
    elif "api condition check" in Element:
        Element = "API Condition Check"
    else:
        Element = "None"
    return Element


def parse_Action_Element(stage_3_answer):

    answer_list = stage_3_answer.split("\n")
    Action = ""
    Element = ""

    for y in answer_list:
        if "action_of_fix: " in y:
            Action = y.replace("action_of_fix: ", "")
        if "API_element_of_fix: " in y:
            Element = y.replace("API_element_of_fix: ", "")

    Action = parse_Action(Action)
    Element = parse_Element(Element)

    return Action, Element


data_dict = {}
with open(input_path, encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        data_dict[line["number"]] = line


stage_2_dict = {}
with open(stage_2_path, encoding="utf-8") as f:
    data = json.load(f)
    for line in data:
        stage_2_dict[line["number"]] = line


# stage_3_fix_pattern_dict = {}
# with open(stage_3_fix_pattern_path, encoding="utf-8") as f:
#     data = f.readlines()
#     data = [line for line in data if line != "\n"]
#     data = [json.loads(line) for line in data]
#     for line in data:
#         stage_3_fix_pattern_dict[line["number"]] = line


stage_3_dict = {}
with open(stage_3_path, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        stage_3_dict[line["number"]] = line
# print(stage_3_dict[4].keys())


data = []
for key in data_dict.keys():
    if key in stage_2_dict.keys():
        if key in stage_3_dict.keys():
            item = data_dict[key]
            # stage_3_answer_fix_pattern = stage_3_fix_pattern_dict[key]["stage_3_answer"]
            stage_3_answer = stage_3_dict[key]["stage_3_answer"]
            print(stage_2_dict[key])
            answer = stage_2_dict[key]["answer"]

            # Action, Element = parse_Action_Element(stage_3_answer_fix_pattern)
            Symptom, Root_Cause = parse_symptom_Root_Cause(stage_3_answer)
            # item["Action"] = Action
            # item["Element"] = Element
            if answer == "no":
                Symptom=""
                Root_Cause=""
            item = {"number": item["number"],
                    # "label": item["label"],
                    "label": answer,
                    "change": item["change"],
                    "comments": item['comments'],
                    # "Action": item["Action"],
                    # "Element": item["Element"],
                    "Symptom": Symptom,\
                    "Root_Cause": Root_Cause}
            data.append(item)

print(data[0].keys())
print(len(data))


with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
