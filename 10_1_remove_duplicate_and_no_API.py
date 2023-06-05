import json
import re

# path ="C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual.json"
path ="C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual_deduplica.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

for idx, item in enumerate(data):
    #get line in change
    neg_line = []
    pos_line = []
    core_change = []
    for line in item["change"]:
        if line.startswith("-"):
            line = "-" +line[1:].strip()
            neg_line.append(line)
            core_change.append(line)
        if line.startswith("+"):
            line = "+" +line[1:].strip()

            pos_line.append(line)
            core_change.append(line)
    core_change = " ".join(core_change)
        
    item["neg_line"] = neg_line
    item["pos_line"] = pos_line
    item["core_change"] = core_change
    item["core_API"] = ""

    pattern = re.compile(r"(\w+\.)(\w+)(\()")
    if pattern.findall(" ".join(item["change"])):
        API_used = pattern.findall(" ".join(item["change"]))[0][1]
        item["core_API"] = API_used

# remove item["core_API"] = ""
data = [x for x in data if x["core_API"] != ""]
# sort data by core_change
data = sorted(data, key=lambda k: k['core_change'])
# keep the first item of each duplicated core_change
unique_date = []
for x in data:
    if x["core_change"] not in [y["core_change"] for y in unique_date]:
        unique_date.append(x)
# data = unique_date
# sort by number
unique_date = sorted(unique_date, key=lambda k: k['number'])

# write unique_date to json file
path = "C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual_deduplica.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(unique_date, f, indent=4, ensure_ascii=False)


# #pretty print the data
# for idx, item in enumerate(data):
#     print(item["number"], "\t", item["label"], "\t", item["comments"], "\t", item["core_change"][:50])



#get number of accepted and rejected
accepted = 0
rejected = 0
for x in unique_date:
    if x["label"] == "yes":
        accepted += 1
    if x["label"] == "no":
        rejected += 1

print("accepted/rejected/processed/total", accepted, "/",  rejected, "/",accepted+rejected,"/", len(data))


