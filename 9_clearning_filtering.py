import json
processed_path = "C:\@code\APIMISUSE\data\misuse_jsons\merged_split_hunk_AST.json"
match_word_list =["fix","solve","repair","bug","failure","issue","error","fault","defect","flaw","glitch"]
#shuffle the list 
import random

# print(random.shuffle(match_word_list))
# print(match_word_list)
# exit()

data = []
with open(processed_path, "r", encoding="utf-8") as f:
    for line in f:
        data.append(json.loads(line))


print(len(data))

data = list(set([json.dumps(x) for x in data]))
data = [json.loads(x) for x in data]
print(len(data))
match_freq_list=[]

data_filtered = []
for idx, x in enumerate(data[:]):


    #get the number of + line
    plus_line = 0
    for line in x["change"]:
        if line.startswith("+ "):
            plus_line += 1
    #get the number of - line
    minus_line = 0
    for line in x["change"]:
        if line.startswith("- "):
            minus_line += 1
    #get the number of AST_diff
    AST_diff_line = 0
    for line in x["AST_diff"]:
        AST_diff_line += 1

    commit_message = x["commit_message"]
    # if fix not in commit message, skip

    # if "fix" not in commit_message.lower():
    #     continue

    if plus_line + minus_line > 10:
        continue
    
    if AST_diff_line > 25:
        continue

    #if any of the match word in commit message, keep else, skip
    if not any(word in commit_message.lower() for word in match_word_list):
        continue
    else:
        # print the match word
        for word in match_word_list:
            if word in commit_message.lower():
                # print(word)
                match_freq_list.append(word)
                break



    x["label"] = ""
    x["comments"] = ""
    x["number"] = idx
    x["plus_line"] = plus_line
    x["minus_line"] = minus_line
    x["AST_diff_line"] = AST_diff_line
    data_filtered.append(x)

# get counter of the match_freq_list
from collections import Counter
print(len(match_freq_list))
match_freq_list = Counter(match_freq_list)
print(match_freq_list)


with open( "C:\@code\APIMISUSE\data\misuse_jsons\merged_split_hunk_AST_filter.json", "w", encoding="utf-8") as f:
    json.dump(data_filtered, f)
print(len(data_filtered))
