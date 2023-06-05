import os
import json
import re

def execute_six_extract_argument_replace(match_word,data):
    res=[]

    for item in data:
        neg_line=0
        pos_line=0
        if len(item["method_neg_name"]) == 0 or len(item["method_pos_name"]) == 0:
            continue
        if item["api_neg_name"] != item["api_pos_name"]:
            continue
        for line in item["core_change"]:
            if line.startswith("-"):
                neg_line+=1
            elif line.startswith("+"):
                pos_line+=1
        if neg_line>1 and pos_line>1:
            continue
        res.append(item)

    return res
