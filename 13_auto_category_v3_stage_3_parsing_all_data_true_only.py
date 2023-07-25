import random
import collections
from sklearn.metrics import confusion_matrix
from collections import Counter
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import plotly.graph_objects as go  # Import the graphical object
import re

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
        Symptom = "Program Crash"
    elif "incorrect result" in Symptom:
        Symptom = "Unexpected Output"
    elif "return warning" in Symptom:
        Symptom = "Return Warning"
    elif "low efficiency" in Symptom:
        Symptom = "Low Efficiency"
    else:
        Symptom = "none"
    return Symptom


def parse_Root_Cause(Root_Cause):

    if "no" in Root_Cause:
        Root_Cause = "none"
    elif "deprecat" in Root_Cause:
        Root_Cause = "Deprecation Management Error"
    elif "deprecation management error" in Root_Cause:
        Root_Cause = "Deprecation Management Error"
    elif "data conversion error" in Root_Cause:
        Root_Cause = "Data Conversion Error"
    elif "device management error" in Root_Cause:
        Root_Cause = "Device Management Error"
    elif "state handling error" in Root_Cause:
        Root_Cause = "State Handling Error"
    elif "algorithm error" in Root_Cause:
        Root_Cause = "Algorithm Error"
    elif "null reference error" in Root_Cause:
        Root_Cause = "Null Reference Error"
    elif "argument error" in Root_Cause:
        Root_Cause = "Argument Error"
    else:
        Root_Cause = "none"
    return Root_Cause


def parse_Action(Action):
    Action = Action.replace(" ", "").lower()

    if "removal" in Action:
        Action = "Redundant"          
    elif "addition" in Action:
        Action = "Missing"
    elif "change" in Action:
        Action = "Replace"
    elif "replace" in Action:
        Action = "change"
    elif "update" in Action:
        Action = "Outdated"
    else:
        Action = "none"

    return Action


def parse_Element(Element):
    Element = Element.lower()

    if "call" in Element:
        Element = "API Method"
    elif "parameter" in Element:
        Element = "API Parameter"
    elif "condition check" in Element:
        Element = "API Condition"
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


def change_parser(change):
    added = []
    removed = []
    for line in change:
        if line.startswith("+"):
            added.append(line)
        elif line.startswith("-"):
            removed.append(line)
    # get all APIs in format ".xxx(" using regex
    API_added = []
    API_removed = []
    for line in added:
        API_added += re.findall(r"\.[a-zA-Z0-9_]+\(", line)
    for line in removed:
        API_removed += re.findall(r"\.[a-zA-Z0-9_]+\(", line)
    API_added = list(set(API_added))
    API_removed = list(set(API_removed))
    # print(API_added, API_removed)

    return added, removed, API_added, API_removed


data_dict = {}
with open(input_path, encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        data_dict[line["number"]] = line
# print(len(data_dict.keys()))
# print(data_dict[0].keys())

stage_2_dict = {}
with open(stage_2_path, encoding="utf-8") as f:
    data = json.load(f)
    for line in data:
        stage_2_dict[line["number"]] = line
# print(len(stage_2_dict.keys()))

stage_3_dict = {}
with open(stage_3_path, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        stage_3_dict[line["number"]] = line
# print(stage_3_dict[4].keys())
# print(len(stage_3_dict.keys()))


data = []

for key in data_dict.keys():
    if key in stage_3_dict.keys():
        item = data_dict[key]
        stage_3_answer = stage_3_dict[key]["stage_3_answer"]
        Symptom, Root_Cause, Action, Element = answer_parser(stage_3_answer)
        added, removed, API_added, API_removed = change_parser(item["change"])
        if len(added) == 0:
            Action = "Redundant"
        if len(removed) == 0:
            Action = "Missing"
        if len(API_added) > len(removed):
            Action = "Missing"
        if len(API_removed) > len(added):
            Action = "Redundant"
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
                "Action_Element": item["Action"] + " " + item["Element"],
                "Symptom_Root_Cause": item["Symptom"] + "|" + item["Root_Cause"]}

        data.append(item)

# print(data[0].keys())
# print(len(data))

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)


Symptom_list = []
Root_Cause_list = []
Action_list = []
Element_list = []
Action_Element_list = []
Symptom_Root_Cause_list = []

for x in data:
    Symptom = x["Symptom"]
    Root_Cause = x["Root_Cause"]
    Action = x["Action"]
    Element = x["Element"]
    Action_Element = x["Action_Element"]
    Symptom_Root_Cause = x["Symptom_Root_Cause"]

    Symptom_list.append(Symptom)
    Root_Cause_list.append(Root_Cause)
    Action_list.append(Action)
    Element_list.append(Element)
    Action_Element_list.append(Action_Element)
    Symptom_Root_Cause_list.append(Symptom_Root_Cause)
print(len(Symptom_list))

Symptom_counter = collections.Counter(Symptom_list)
Root_Cause_counter = collections.Counter(Root_Cause_list)
Action_counter = collections.Counter(Action_list)
Element_counter = collections.Counter(Element_list)
Action_Element_counter = collections.Counter(Action_Element_list)
Symptom_Root_Cause_counter = collections.Counter(Symptom_Root_Cause_list)

print(Symptom_counter)
print("")
print(Root_Cause_counter)
print("")
print(Action_counter)
print("")
print(Element_counter)
print("")
print(Action_Element_counter)
print("")
print(Symptom_Root_Cause_counter)



def plot_sanky():
    node_label = list(set(Symptom_list))+list(set(Root_Cause_list))
    node_dict = {y: x for x, y in enumerate(node_label)}
    s_t_list = Symptom_Root_Cause_counter.keys()
    source = [x.split("|")[1] for x in s_t_list]
    target = [x.split("|")[0] for x in s_t_list]
    values = list(Symptom_Root_Cause_counter.values())
    print("")
    print(source)
    print("")
    print(target)
    print("")
    print(values)

    source_node = [node_dict[x] for x in source]
    target_node = [node_dict[x] for x in target]
    # make 4 random colors low opacity
    category_colors = [
        f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.3)" for x in range(4)]
    # for each unique target, assign a color
    unique_targets = list(set(target_node))
    target_node_colors = [
        category_colors[unique_targets.index(x)] for x in target_node]
    # [0, 0, 0, 1, 1, 1, 2, 3, 3, 4, 4]
    # [2, 3, 4, 2, 3, 4, 5, 5, 6, 5, 6]

    fig = go.Figure(
        data=[go.Sankey(
            node=dict(
                label=node_label,
            ),
            # This part is for the link information
            link=dict(
                source=source_node,
                target=target_node,
                value=values,
                color=target_node_colors
            ), textfont=dict(size=25, color='black'),
        )]
    )

    # Add annotations for the labels
    fig.add_annotation(
        x=0,  # X position for the left label
        y=1.1,   # Y position for the left label
        text="API Misuse Root Causes",
        showarrow=False,
        font=dict(
            size=25,
            color="black"
        )
    )

    fig.add_annotation(
        x=1,   # X position for the right label
        y=1.03,   # Y position for the right label
        text="API Misuse Symptoms",
        showarrow=False,
        font=dict(
            size=25,
            color="black"
        )
    )

    # With this save the plots
    plot(fig,
         image_filename='sankey_plot_1',
         image='png',
         image_width=1000,
         image_height=600
         )
    # And shows the plot
    fig.show()


def plot_stack_type(Action_Element_counter):
    data=Action_Element_counter
    operation = (
        "Missing",
        "Redundant",
        "Replace",
        "Outdated",
    )
    API_method = np.array([data["Missing API Method"], data["Redundant API Method"], data["Replace API Method"], data["Outdated API Method"]])
    API_parameter = np.array([data["Missing API Parameter"], data["Redundant API Parameter"], data["Replace API Parameter"], data["Outdated API Parameter"]])
    API_condition = np.array([data["Missing API Condition"], data["Redundant API Condition"], data["Replace API Condition"], data["Outdated API Condition"]])
    elements = {
        "API Method":    API_method,
        "API Parameter": API_parameter,
        "API Condition": API_condition,
    }
    width = 0.5

    fig, ax = plt.subplots()
    bottom = np.zeros(4)

    for boolean, element_count in elements.items():
        p = ax.bar(operation, element_count, width,
                   label=boolean, bottom=bottom)
        bottom += element_count
        # Add number labels to each stack box
        ax.bar_label(p, label_type='center')

    ax.set_ylim(0, 350)
    ax.set_title("Number of API Misuse Elements per API Operation")
    ax.set_ylabel("Count")
    ax.set_xlabel("Operation")
    ax.legend(loc="upper left")
    # save to pdf
    # change font size
    plt.savefig("API_Misuse_Elements_per_API_Operation.pdf",
                bbox_inches='tight')

    plt.show()

# plot_stack_type(Action_Element_counter)

def plot_stack_root_cause_symptom(Symptom_Root_Cause_counter):
    data=Symptom_Root_Cause_counter
    operation = (
        "Program Crash",
        "Low Efficiency",
        "Unexpected Output",
        "Return Warning",
    )
    device_management_error = np.array([data["Program Crash|Device Management Error"], data["Low Efficiency|Device Management Error"], data["Unexpected Output|Device Management Error"], data["Return Warning|Device Management Error"]])
    data_conversion_error = np.array([data["Program Crash|Data Conversion Error"], data["Low Efficiency|Data Conversion Error"], data["Unexpected Output|Data Conversion Error"], data["Return Warning|Data Conversion Error"]])
    deprecation_management_error = np.array([data["Program Crash|Deprecation Management Error"], data["Low Efficiency|Deprecation Management Error"], data["Unexpected Output|Deprecation Management Error"], data["Return Warning|Deprecation Management Error"]])
    algorithm_error = np.array([data["Program Crash|Algorithm Error"], data["Low Efficiency|Algorithm Error"], data["Unexpected Output|Algorithm Error"], data["Return Warning|Algorithm Error"]])
    null_reference_error = np.array([data["Program Crash|Null Reference Error"], data["Low Efficiency|Null Reference Error"], data["Unexpected Output|Null Reference Error"], data["Return Warning|Null Reference Error"]])
    argument_error = np.array([data["Program Crash|Argument Error"], data["Low Efficiency|Argument Error"], data["Unexpected Output|Argument Error"], data["Return Warning|Argument Error"]])
    state_handling_error = np.array([data["Program Crash|State Handling Error"], data["Low Efficiency|State Handling Error"], data["Unexpected Output|State Handling Error"], data["Return Warning|State Handling Error"]])
    elements = {
        "device management error":      device_management_error,
        "data conversion error":        data_conversion_error,
        "deprecation management error": deprecation_management_error,
        "algorithm error":              algorithm_error,
        "null reference error":         null_reference_error,
        "argument error":               argument_error,
        "state handling error":         state_handling_error,
    }
    width = 0.5

    fig, ax = plt.subplots()
    bottom = np.zeros(4)

    for boolean, element_count in elements.items():
        p = ax.bar(operation, element_count, width,
                   label=boolean, bottom=bottom)
        bottom += element_count

        for i, v in enumerate(element_count):
            if v >= 5:  # Only plot numbers if greater than or equal to 10
                plt.text(i,bottom[i]-element_count[i]/2, str(v), ha='center', va='center')


    ax.set_ylim(0, 400)
    ax.set_title("Number of Root Cause per Symptom")
    ax.set_ylabel("Count")
    ax.set_xlabel("Symptom")
    ax.legend(loc="upper right")
    # save to pdf
    plt.rcParams.update({'font.size': 20})

    plt.savefig("API_Misuse_Elements_per_API_Operation.pdf",
                bbox_inches='tight')

    plt.show()


plot_stack_root_cause_symptom(Symptom_Root_Cause_counter)
