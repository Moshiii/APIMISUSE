import re
import json
import os

data_path = "C:\@code\APIMISUSE\data\misuse_jsons\auto_langchain\data_all\misuse_v3_classification_stage_3_result.json"

data_dict = {}
with open(data_path, encoding="utf-8") as f:
    data = json.load(f)
    for line in data:
        item = {
            "number": line["number"],
            "Symptom": line["Symptom"],
            "Root_Cause": line["Root_Cause"],
            "Action": line["Action"],
            "Element": line["Element"],
        }
        data_dict[line["number"]] = item
