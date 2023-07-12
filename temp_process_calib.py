from collections import Counter
from sklearn.metrics import confusion_matrix, accuracy_score
import json

old_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\calib\calib_data_1k.json"
predict_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\calib\misuse_v3_classification_stage_2.json"
output_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\calib\calib_invest_data_1k.json"
# read old

data_old = {}
with open(old_path, encoding="utf-8") as f:
    data = json.load(f)
    for line in data:
        data_old[line["number"]] = line
print(len(data_old))

data_predict = {}
with open(predict_path, encoding="utf-8") as f:
    data = json.load(f)
    for line in data:
        data_predict[line["number"]] = line
print(len(data_predict))

data_output = []
for key, value in data_old.items():
    if key in data_predict:
        item = data_old[key]
        item["label"] = data_predict[key]["answer"]
        data_output.append(item)
    else:
        print(key)
print(len(data_output))

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data_output, f, indent=4)