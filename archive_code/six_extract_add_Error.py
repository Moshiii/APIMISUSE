import os
import json
import re


def execute_six_extract_add_Error(match_word,data):
    res=[]

    for item in data:
        neg_pattern=0
        pos_pattern=0
        if len(item["method_neg_name"]) == 0 or len(item["method_pos_name"]) == 0:
            continue
        neg_core_change = []
        pos_core_change = []
        for line in item["core_change"]:
            if line.startswith("-"):
                neg_core_change.append(line)
            elif line.startswith("+"):
                pos_core_change.append(line)

        for line in neg_core_change:
            if "Error" in line:
                neg_pattern=1
                break
        for line in pos_core_change:
            if "Error" in line:
                pos_pattern=1
                break
        
        if neg_pattern==0 and pos_pattern==1:
            res.append(item)

    return res
