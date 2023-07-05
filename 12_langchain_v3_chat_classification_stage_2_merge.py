from sklearn.metrics import confusion_matrix
from collections import Counter
import json
import Levenshtein


manual_path = "C:\@code\APIMISUSE\data\misuse_jsons\manual\merged_split_hunk_AST_filter_manual_deduplica_reduced_category_strict_general_case_Moshi.json"
predict_path = 'C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v3_classification_stage_2_if_api_fix.json'
predict_path_minor_change = 'C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v3_classification_stage_2_minor_change.json'

output_path = 'C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\misuse_v3_classification_stage_2.json'


def check_API(data_list, API_method_list):
    data_list = " ".join(data_list)
    for x in API_method_list:
        if x in data_list:
            return True
    return False

def check_distance(added,removed):
    # remove initial +
    added = [x[1:] for x in added]
    removed = [x[1:] for x in removed]
    # strip
    added = [x.strip() for x in added]
    removed = [x.strip() for x in removed]

    added = " ".join(added)
    removed = " ".join(removed)
    # remove space
    added = added.replace(" ", "")
    removed = removed.replace(" ", "")
    distance = Levenshtein.distance(added,removed)
    return added,removed,distance

    



# read
data_dict = {}
with open(manual_path, encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        data_dict[line["number"]] = line

data_stage_minor_change = {}
with open(predict_path_minor_change, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        data_stage_minor_change[line["number"]] = line


data_stage_3_dict = {}
with open(predict_path, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        data_stage_3_dict[line["number"]] = line

with open(output_path, 'w', encoding="utf-8") as f:
    f.write("")

# merge data_stage_1_dict into data_dict by key
for key in data_dict.keys():
    if key in data_stage_minor_change.keys():
        if key in data_stage_3_dict.keys():
            data_dict[key]["minor_change"] = data_stage_minor_change[key]["answer"]
            data_dict[key]["if_API_fix"] = data_stage_3_dict[key]["answer"]
print(len(data_dict))
# convert data_dict to list
data = []
for key in data_dict.keys():
    if "minor_change" in data_dict[key].keys():
        if "if_API_fix" in data_dict[key].keys():
            data.append(data_dict[key])
print(len(data))
print(data[0].keys())

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


y_test = []
y_pred = []
data_filtered=[]
distance_list = []
comment_list= []
# keep only number, label, answer, change
for idx in range(len(data)):
    answer = ""
    label = data[idx]["label"]
    # if label == "":
    #     continue

    minor_change = data[idx]["minor_change"]
    minor_change = minor_change.lower().replace(" ", "").replace(".", "")
    if minor_change == "maybe":
        answer="no"

    if_API_fix = data[idx]["if_API_fix"]
    if_API_fix = if_API_fix.lower().replace(" ", "").replace(".", "")
    if if_API_fix == "maybe":
        answer="no"


    if_contains_API = False
    change = data[idx]["change"]
    added = data[idx]["pos_line"]
    removed = data[idx]["neg_line"]
    if_contains_API = check_API(added, API_method_list) and check_API(removed, API_method_list)

    # added, removed, distance = check_distance(added, removed)
    _, _, distance = check_distance(added, removed)
    # if data[idx]["number"] ==37:
        # print(data[idx]["number"], distance, added, removed)
    # if distance == 4 and minor_change == "no":
    #     print(data[idx]["number"], distance, added, removed)
    # if minor_change == "no" :
    #     distance_list.append(distance)
    distance_list.append(distance)
    data[idx]["distance"] = distance
        # if_contains_API = check_API(added, API_method_list)
    # if_contains_API = check_API(removed, API_method_list)

    
    # if minor_change == "no" and if_API_fix == "yes" and if_contains_API == True:
    if minor_change == "no" and if_API_fix == "yes" and distance>3:
    # if minor_change == "no" and if_API_fix == "yes" :
    # if minor_change == "no" and if_API_fix == "yes" :
    # if minor_change == "no":
        # if if_API_fix == "yes":
        answer = "yes"
    else:
        answer = "no"

    y_test.append(label)
    y_pred.append(answer)

    data[idx]["answer"] = answer
    data[idx] = {key: data[idx][key] for key in [
        "number", "comments", "commit_message", "label", "answer", "change",]}
    data_filtered.append(data[idx])

print("total: ", len(data_filtered))
data_filtered = [line for line in data_filtered if line["answer"] =="yes" or line["label"] =="yes"]
print(len(data_filtered))
# for x in data_filtered:
#     # print(x["number"],x["distance"],x["comments"])
#     comment_list.append(x["comments"])

print("total: ", len(y_test))
print("label:", Counter(y_test))
print("answer:", Counter(y_pred))
# print("distance:", Counter(distance_list))
print("comment:", Counter(comment_list))

conf_mat = confusion_matrix(y_test, y_pred)
print(conf_mat)
with open(output_path, 'w', encoding="utf-8") as f:
    json.dump(data_filtered, f, indent=4)
