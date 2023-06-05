import json
import re

total_length = 0
with open("C:\@code\APIMISUSE\data\misuse_jsons\merged.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    total_length += len(data)

print(total_length)
data_list = []

# for commit in the list:
for counter, x in enumerate(data[:]):
    print(counter,"/", len(data))
    change = x["change"]
    # regex of "@@ -1,8 +1,7 @@"
    pattern = r"@@ -\d+,\d+ \+\d+,\d+ @@"

    for idx, line in enumerate(change):
        if line.startswith("@@"):
            line = re.sub(pattern, "<<spliter>>", line)
            change[idx] = line

    change_string = "\n".join(change)
    change_string = change_string.split("<<spliter>>")
    change_string = [x.strip() for x in change_string]
    change_string = change_string[1:]
    del x["change"]
    del x["core_change"]
    for index, hunk in enumerate(change_string):
        hunk= hunk.split("\n")
        x["change"] = hunk
        x["hunk_index"] = index
        data_list.append(x)



with open("C:\@code\APIMISUSE\data\misuse_jsons\merged_split_hunk.json", "w", encoding="utf-8") as f:
    json.dump(data_list, f, indent=4)

total_length = 0
with open("C:\@code\APIMISUSE\data\misuse_jsons\merged_split_hunk.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    total_length += len(data)

print(total_length)
