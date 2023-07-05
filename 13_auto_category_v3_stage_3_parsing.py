from sklearn.metrics import confusion_matrix
from collections import Counter
import json

input_path = "C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual_deduplica_reduced_category_strict_general_case_Moshi.json"
stage_3_path = 'C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v3_classification_stage_3.json'
output_path = 'C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\merged_split_hunk_AST_filter_manual_Moshi_auto.json'


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
        if "Root_Cause: " in y:
            Root_Cause = y.replace("Motivation: ", "")

    Symptom = parse_symptom(Symptom)
    Root_Cause = parse_Root_Cause(Root_Cause)

        
    return Symptom, Root_Cause



data_dict = {}
with open(input_path, encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        data_dict[line["number"]] = line
# print(data_dict[0].keys())

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
    if key in stage_3_dict.keys():
        item = data_dict[key]
        stage_3_answer = stage_3_dict[key]["stage_3_answer"]
        Symptom, Root_Cause = parse_symptom_Root_Cause(stage_3_answer)

        item["Symptom"] = Symptom
        item["Root_Cause"] = Root_Cause
        item={"number":item["number"], \
              "label":item["label"],\
              "change":item["change"],\
              "comments":item['comments'], \
              "Symptom":item["Symptom"],\
              "Root_Cause":item["Root_Cause"]}
        data.append(item)

print(data[0].keys())
print(len(data))


with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)


# exit()
Symptom_list = []
Root_Cause_list = []
for x in data:
    Symptom = x["Symptom"]
    Root_Cause = x["Root_Cause"]

    Symptom_list.append(Symptom)
    Root_Cause_list.append(Root_Cause)
import collections
Symptom_counter = collections.Counter(Symptom_list)
Root_Cause_counter = collections.Counter(Root_Cause_list)
print(Symptom_counter)
print("")
print(Root_Cause_counter)





