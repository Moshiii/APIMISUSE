import os
import json
import re

def execute_six_extract_try_catch(match_word,data):
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

        neg_merge = "\n".join(neg_core_change)
        # print(neg_merge)
        if "try" in neg_merge and "except" in neg_merge:
            neg_pattern=1
        pos_merge = "\n".join(pos_core_change)
        # print(pos_merge)
        if "try" in pos_merge and "except" in pos_merge:
            pos_pattern=1
        
        if neg_pattern==0 and pos_pattern==1:
            res.append(item)

    return res
