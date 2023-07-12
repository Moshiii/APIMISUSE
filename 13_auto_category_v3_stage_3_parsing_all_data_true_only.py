import collections
from sklearn.metrics import confusion_matrix
from collections import Counter
import json


base_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\\data_all\\"

input_path = base_path + 'data_all.json'
stage_2_path = base_path + 'misuse_v3_classification_stage_2.json'
stage_1_path = base_path + 'misuse_v2_stage_1_code_explain.json'
stage_3_path = base_path + 'misuse_v3_classification_stage_3.json'
output_path = base_path + 'misuse_v3_classification_stage_3_result.json'


def parse_symptom(Symptom):

    if "no" in Symptom:
        Symptom = "none"
    elif "program crash" in Symptom:
        Symptom = "program crash"
    elif "unexpected output" in Symptom:
        Symptom = "unexpected output"
    elif "return warning" in Symptom:
        Symptom = "return warning"
    elif "low efficiency" in Symptom:
        Symptom = "low efficiency"
    else:
        Symptom = "none"
    return Symptom


def parse_Root_Cause(Root_Cause):

    if "no" in Root_Cause:
        Root_Cause = "none"
    elif "deprecat" in Root_Cause:
        Root_Cause = "deprecation management error"
    elif "deprecation management error" in Root_Cause:
        Root_Cause = "deprecation management error"
    elif "management error" in Root_Cause:
        Root_Cause = "deprecation management error"
    elif "data conversion error" in Root_Cause:
        Root_Cause = "data conversion error"
    elif "device management error" in Root_Cause:
        Root_Cause = "device management error"
    elif "state handling error" in Root_Cause:
        Root_Cause = "state handling error"
    elif "algorithm error" in Root_Cause:
        Root_Cause = "algorithm error"
    elif "null reference error" in Root_Cause:
        Root_Cause = "null reference error"
    elif "argument error" in Root_Cause:
        Root_Cause = "argument error"
    else:
        Root_Cause = "none"
    return Root_Cause


def parse_Action(Action):
    Action = Action.replace(" ", "").lower()

    if "removal" in Action:
        Action = "removal"
    elif "addition" in Action:
        Action = "addition"
    elif "change" in Action:
        Action = "change"
    elif "replace" in Action:
        Action = "change"
    elif "update" in Action:
        Action = "update"
    else:
        Action = "none"

    return Action


def parse_Element(Element):
    Element = Element.lower()

    if "call" in Element:
        Element = "api call"
    elif "parameter" in Element:
        Element = "api parameter"
    elif "condition check" in Element:
        Element = "api condition check"
    else:
        Element = "none"
    return Element


def answer_parser(stage_3_answer):

    answer_list = stage_3_answer.lower().split("\n")
    Symptom = ""
    Root_Cause = ""
    Action = ""
    Element = ""

    for y in answer_list:
        if "symptom: " in y:
            Symptom = y.replace("symptom: ", "")
        if "motivation: " in y:
            Root_Cause = y.replace("motivation: ", "")
        if "action: " in y:
            Action = y.replace("action: ", "")
        if "element: " in y:
            Element = y.replace("element: ", "")

    Symptom = parse_symptom(Symptom)
    Root_Cause = parse_Root_Cause(Root_Cause)
    Action = parse_Action(Action)
    Element = parse_Element(Element)

    return Symptom, Root_Cause, Action, Element


data_dict = {}
with open(input_path, encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        data_dict[line["number"]] = line
print(len(data_dict.keys()))
# print(data_dict[0].keys())

stage_2_dict = {}
with open(stage_2_path, encoding="utf-8") as f:
    data = json.load(f)
    for line in data:
        stage_2_dict[line["number"]] = line
print(len(stage_2_dict.keys()))

stage_3_dict = {}
with open(stage_3_path, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        stage_3_dict[line["number"]] = line
# print(stage_3_dict[4].keys())
print(len(stage_3_dict.keys()))


data = []

for key in data_dict.keys():
    if key in stage_3_dict.keys():
        item = data_dict[key]
        stage_3_answer = stage_3_dict[key]["stage_3_answer"]
        Symptom, Root_Cause, Action, Element = answer_parser(stage_3_answer)
        if Symptom == "none" or Root_Cause == "none" or Action == "none" or Element == "none":
            continue
        item["Symptom"] = Symptom
        item["Root_Cause"] = Root_Cause
        item["Action"] = Action
        item["Element"] = Element
        item = {"number": item["number"],
                "change": item["change"],
                "comments": item['comments'],
                "Symptom": item["Symptom"],
                "Root_Cause": item["Root_Cause"],
                "Action": item["Action"],
                "Element": item["Element"],
                "Action_Element": item["Action"] + " " + item["Element"]}

        data.append(item)

print(data[0].keys())
print(len(data))

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)


Symptom_list = []
Root_Cause_list = []
Action_list = []
Element_list = []
Action_Element_list = []

for x in data:
    Symptom = x["Symptom"]
    Root_Cause = x["Root_Cause"]
    Action = x["Action"]
    Element = x["Element"]
    Action_Element = x["Action_Element"]

    Symptom_list.append(Symptom)
    Root_Cause_list.append(Root_Cause)
    Action_list.append(Action)
    Element_list.append(Element)
    Action_Element_list.append(Action_Element)

Symptom_counter = collections.Counter(Symptom_list)
Root_Cause_counter = collections.Counter(Root_Cause_list)
Action_counter = collections.Counter(Action_list)
Element_counter = collections.Counter(Element_list)
Action_Element_counter = collections.Counter(Action_Element_list)

print(Symptom_counter)
print("")
print(Root_Cause_counter)
print("")
print(Action_counter)
print("")
print(Element_counter)
print("")
print(Action_Element_counter)
