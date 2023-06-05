import json
import code_diff as cd
data_list = []
total_length = 0
with open("C:\@code\APIMISUSE\data\misuse_jsons\merged_split_hunk.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    total_length += len(data)
print(total_length)

for idx, x in enumerate(data[:]):
    print(idx, "/", total_length)
    # print(x["change"])
    change_before = []
    change_after = []

    for line in x["change"]:
        if line.startswith("-"):
            change_before.append(line[1:])
        elif line.startswith("+"):
            change_after.append(line[1:])
        else:
            change_before.append(line)
            change_after.append(line)
    change_before = "\n".join(change_before)
    change_after = "\n".join(change_after)
    result = ""

    try:
        output = cd.difference(change_before, change_after, lang="python")
        result = output.edit_script()
    except:
        result = ["AST parser failed"]
    result = [str(x) for x in result]
    x["AST_diff"] = result

    with open("C:\@code\APIMISUSE\data\misuse_jsons\merged_split_hunk_AST.json", "a", encoding="utf-8") as f:
        json.dump(x, f)
        f.write("\n")

    # total_length = 0
    # data = []
    # with open("C:\@code\APIMISUSE\data\misuse_jsons\merged_split_hunk_across_change.json", "r", encoding="utf-8") as f:
    #     for line in f:
    #         data.append(json.loads(line))
    
    # total_length = len(data)
    # print(total_length)
