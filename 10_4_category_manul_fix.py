import collections
import json

# path ="C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual.json"
path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/merged_split_hunk_AST_filter_manual_deduplica_reduced_category_strict_general_case_Moshi.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

# ===============================================================================
# value replacement for label comment fix
# ===============================================================================

# before ="logic fix"
# after = "argument fix"

# for idx,x in enumerate(data):
#     if before in x["comments"]:
# #         # data[idx]["comments"] = after
#         data[idx]["comments"] = data[idx]["comments"].replace(before, after)
# #         # data[idx]["comments"] = data[idx]["comments"].split(before)[0]+before
# #         # data[idx]["comments"] = data[idx]["comments"].split(before)[0]


# ===============================================================================
# manual investigation
# ===============================================================================

# for idx, x in enumerate(data):
#     if x["comments"].endswith("for"):
#         print(idx, "\t", x["comments"])
#         print(idx, "\t", x["commit_message"])
#         for y in x["change"]:
#             print("\t", y)
#         data[idx]["comments"] = "update_condition_check"

# ===============================================================================
# write to file again
# ===============================================================================

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# exit()

# get number of accepted and rejected
accepted = 0
rejected = 0
for x in data:
    if x["label"] == "yes":
        accepted += 1
    if x["label"] == "no":
        rejected += 1
print("accepted/rejected/processed/total", accepted, "/",
      rejected, "/", accepted+rejected, "/", len(data))

accepted_comments = {}
unique_comments = []

import re

for idx, x in enumerate(data):
    if x["label"] == "yes":
        if x["core_API"] != "":
            accepted_comments[idx] = x["comments"]
            unique_comments.append(x["comments"])
        #===========================================================================
        # check if API used
        #===========================================================================

        # pattern = re.compile(r"(\w+\.)(\w+)(\()")
        # API_used =[]
        # if pattern.findall(" ".join(x["neg_line"])):
        #     API_used += [pattern.findall(" ".join(x["neg_line"]))[0][1]]
        # if pattern.findall(" ".join(x["pos_line"])):
        #     API_used += [pattern.findall(" ".join(x["pos_line"]))[0][1]]
        # x["diff_API"] = API_used
        # if len(x["diff_API"])==0 and x["label"]=="yes":
        #     print(x["number"], "\t", x["label"])
        #===========================================================================

        #===========================================================================
        # check if test case
        #===========================================================================
        # if "test" in x["commit_message"].lower():
        #     print(x["number"], "\t", x["label"])    
        # else:
        # change = " ".join(x["change"])
        # if "test" in change.lower():
        #     print(x["number"], "\t", x["label"])

    

exit()
# unique_comments = sorted(list(set(unique_comments)))
unique_comments = sorted(list(unique_comments))

hit = 0
unique_action = []
unique_object = []
unique_action_object = []
unique_motivation = []
for idx, comment in enumerate(unique_comments):

    if "for" in comment:
        hit += 1
        action = comment.split(" ")[0]
        rest = " ".join(comment.split(" ")[1:])
        object = rest.split("for")[0]
        motivation = rest.split("for")[1]
        unique_action.append(action)
        unique_object.append(object)
        unique_action_object.append(action+" "+object)
        unique_motivation.append(motivation)
    else:
        print(idx, "\t",comment)

print("hit", hit)

print("comments")
for x in collections.Counter(unique_comments):
    print(collections.Counter(unique_comments)[x], "\t", x)

print("action_object")
for x in collections.Counter(unique_action_object):
    print(collections.Counter(unique_action_object)[x], "\t", x)

print("action")
for x in collections.Counter(unique_action):
    print(collections.Counter(unique_action)[x], "\t", x)

print("object")
for x in collections.Counter(unique_object):
    print(collections.Counter(unique_object)[x], "\t", x)

print("motivation")
for x in collections.Counter(unique_motivation):
    print(collections.Counter(unique_motivation)[x], "\t", x)