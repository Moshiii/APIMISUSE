import os
import json
import re

def execute_six_extract_device_misuse(match_word,data):
    res=[]

    for item in data:
        neg_divce=0
        pos_device=0
        if len(item["method_neg_name"]) == 0 or len(item["method_pos_name"]) == 0:
            continue
        for method in item["method_neg_name"] :
            if "device" in method:
                neg_divce=1
                break
        for method in item["method_pos_name"] :
            if "device" in method:
                pos_device=1
                break
        
        if neg_divce==0 and pos_device==1:
            res.append(item)

    return res
