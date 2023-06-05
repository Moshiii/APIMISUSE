import json

# path ="C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual.json"
path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/merged_split_hunk_AST_filter_manual_deduplica.json"



with open(path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

#get number of accepted and rejected
accepted = 0
rejected = 0
for x in data:
    if x["label"] == "yes":
        accepted += 1
    if x["label"] == "no":
        rejected += 1

print("accepted/rejected/processed/total", accepted, "/",  rejected, "/",accepted+rejected,"/", len(data))

# exit()
# get all the manual label comments for accepted and rejected with its item number
accepted_comments = {}
rejected_comments = {}
rejected_data = []
accepted_data = []
for idx,x in enumerate(data):
    if x["label"] == "yes":

        # if "type" in x["commit_message"]:
        #     accepted_comments[idx] = "##"+ x["comments"]

        accepted_comments[idx] = x["comments"]

    if x["label"] == "no":
        rejected_comments[idx] = x["comments"]
#sort the comments alphabetical
accepted_comments = dict(sorted(accepted_comments.items(), key=lambda item: item[1]))
rejected_comments = dict(sorted(rejected_comments.items(), key=lambda item: item[1]))

for idx,x in enumerate(accepted_comments):
    accepted_data.append(data[x])

for idx,x in enumerate(rejected_comments):
    rejected_data.append(data[x])
# print("accepted comments", accepted_comments)
# print("rejected comments", rejected_comments)

#pretty print the comments
unique_comments = []
for idx, comment in accepted_comments.items():
    # print(idx, "\t",comment)
    unique_comments.append(comment)
unique_comments = list(set(unique_comments))
unique_comments = sorted(unique_comments)
# for idx, comment in enumerate(unique_comments):
#     print(idx, "\t",comment)

# wrtie rejected_comments to json file
path = "C:\@code\APIMISUSE\data\misuse_jsons\\rejected_comments.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(rejected_data, f, indent=4, ensure_ascii=False)

# wrtie rejected_comments to json file
path = "C:\@code\APIMISUSE\data\misuse_jsons\\accepted_comments.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(accepted_data, f, indent=4, ensure_ascii=False)

