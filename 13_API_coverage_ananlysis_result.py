import collections
from sklearn.metrics import confusion_matrix
from collections import Counter
import json

base_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\\data_all\\"
output_path = base_path + 'misuse_v3_classification_stage_3_result.json'
# output_path = base_path + 'data_all.json'
# read the file

with open(output_path, encoding="utf-8") as f:
    data = json.load(f)
print(len(data))
# get all APIs
API_method_torch_list = []
API_method_tf_list = []

with open('C:\@code\APIMISUSE\data\API_method_list_torch.txt', encoding="utf-8") as f:
    API_data = f.readlines()
    for x in API_data:
        if x != "\n":
            API_method_torch_list.append(x.strip().lower())
with open('C:\@code\APIMISUSE\data\API_method_list_tf.txt', encoding="utf-8") as f:
    API_data = f.readlines()
    for x in API_data:
        if x != "\n":
            API_method_tf_list.append(x.strip().lower())

print(len(API_method_torch_list))
API_method_torch_list_filter=[x for x in API_method_torch_list if not x.startswith("._") and not x.endswith("_(")]

print(len(API_method_tf_list))
API_method_tf_list_filter=[x for x in API_method_tf_list if not x.startswith("._") and not x.endswith("_(")]
print(len(API_method_tf_list_filter)+len(API_method_torch_list_filter))

counter=0
hit_list_1=[]
for x in data:
    for y in API_method_torch_list_filter:
        if y in "\n".join(x["change"]).lower():
            counter+=1
            hit_list_1.append(y)
print(len(list(set(hit_list_1))))


counter=0
hit_list_2=[]
for x in data:
    for y in API_method_tf_list_filter:
        if y in "\n".join(x["change"]).lower():
            counter+=1
            hit_list_2.append(y)
print(len(list(set(hit_list_2))))
print(len(list(set(hit_list_1+hit_list_2))))


# write the hit_list_1+hit_list_2 to file
with open(base_path + 'API_hit_list.txt', 'w', encoding="utf-8") as f:
    for item in list(set(hit_list_1+hit_list_2)):
        f.write("%s\n" % item)
        

added_line_list = []
removed_line_list = []
total_line_list = []

for x in data:
    added_counter = 0
    removed_counter = 0
    total_counter = 0
    for line in x["change"]:
        if line.startswith("+"):
            added_counter += 1
        if line.startswith("-"):
            removed_counter -= 1
    total_counter = added_counter + removed_counter

    added_line_list.append(added_counter)
    removed_line_list.append(removed_counter)
    total_line_list.append(total_counter)

print(Counter(added_line_list))
print(Counter(removed_line_list))
print(Counter(total_line_list))


