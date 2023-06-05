import json
source_path = "C:\@code\APIMISUSE\data\misuse_jsons\\accepted_comments.json"
# source_path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/merged_split_hunk_AST_filter_manual_deduplica.json"
# target_path ="C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual.json"
# source_path = "C:\@code\APIMISUSE\data\misuse_jsons\\rejected_comments.json"

target_path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/merged_split_hunk_AST_filter_manual_deduplica_reduced_category.json"


#read all the data in raw_path
with open(source_path, "r", encoding="utf-8") as f:
    source_data = json.load(f)
#read all the data in path
with open(target_path, "r", encoding="utf-8") as f:
    target_data = json.load(f)

for idx1,item1 in enumerate(source_data):
    for idx2,item2 in enumerate(target_data):
        if item1["number"] == item2["number"]:
            target_data[idx2]["comments"] = item1["comments"]
            target_data[idx2]["label"] = item1["label"]


# write data to path
with open(target_path, "w", encoding="utf-8") as f:
    json.dump(target_data, f, indent=4, ensure_ascii=False)

