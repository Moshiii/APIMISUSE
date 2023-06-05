import json
import collections


# path ="C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual.json"
path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/merged_split_hunk_AST_filter_manual_deduplica_reduced_category.json"

bug_fix_path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/API_misuse_bug_fix.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

accepted = 0
rejected = 0
for x in data:
    if x["label"] == "yes":
        accepted += 1
    if x["label"] == "no":
        rejected += 1
print("accepted/rejected/processed/total", accepted, "/",
      rejected, "/", accepted+rejected, "/", len(data))

bug_fix=[]

for idx, x in enumerate(data):
    if x["label"] == "yes":
        if x["core_API"] != "":
            if len(x["neg_line"]) == 1 and len(x["pos_line"]) == 1:
                bug = x["neg_line"][0][1:]
                fix = x["pos_line"][0][1:]
                bug_fix.append({"bug":bug,"fix":fix})

# write bug_fix to file
with open(bug_fix_path, "w", encoding="utf-8") as f:
    f.write(json.dumps(bug_fix, indent=4))