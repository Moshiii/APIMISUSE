import json
import collections

API_method_list = []
with open('C:\@code\APIMISUSE\data\API_method_list_torch.txt', encoding="utf-8") as f:
    API_data = f.readlines()
    for x in API_data:
        if x != "\n":
            API_method_list.append(x.strip().lower())
with open('C:\@code\APIMISUSE\data\API_method_list_tf.txt', encoding="utf-8") as f:
    API_data = f.readlines()
    for x in API_data:
        if x != "\n":
            API_method_list.append(x.strip().lower())

# path ="C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual.json"
path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/merged_split_hunk_AST_filter_manual_deduplica_reduced_category_strict_general_case_Moshi.json"
# path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/merged_split_hunk_AST_filter_manual_deduplica_reduced_category.json"



with open(path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

no_API_counter=0
wrong_manual_counter=0
wrong_auto_counter=0

filtered_data = []
for idx, x in enumerate(data):
    check_API ="False"
    added = " ".join(x["pos_line"])
    removed = " ".join(x["neg_line"])
    changed = " ".join(x["change"])
    for API_name in API_method_list:
        
        if API_name in added:
            check_API="True"
        if API_name in removed:
            check_API="True"
        if API_name in changed:
            check_API="True"
    if check_API == "False":
        no_API_counter += 1
    else:
        filtered_data.append(x)
data=filtered_data
print("no_API_counter: ",no_API_counter)



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

for idx, x in enumerate(data):
    if x["label"] == "yes":
        if x["core_API"] != "":
            accepted_comments[idx] = x["comments"]
            unique_comments.append(x["comments"])

# unique_comments = sorted(list(set(unique_comments)))
unique_comments = sorted(list(unique_comments))

hit = 0
unique_action = []
unique_object = []
unique_action_object = []
unique_motivation = []
for idx, comment in enumerate(unique_comments):

    # if "to" in comment:
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

# print("comments")
# for x in collections.Counter(unique_comments):
#     print(collections.Counter(unique_comments)[x], "\t", x)

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




Counter({'Change': 270, 'Addition': 88, 'update': 41, 'Removal': 24})

Counter({'API Call': 232, 'API Parameter': 125, 'API Condition Check': 62, 'None': 4})