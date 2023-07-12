import collections
from sklearn.metrics import confusion_matrix
from collections import Counter
import json
# manual
# calib
# test_1
# test_2
base_path_1 = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\\manual\\manual_data_1k.json"
base_path_2 = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\\calib\\calib_data_1k.json"
base_path_3 = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\\test_1\\test_1_data_1k.json"
base_path_4 = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\\test_2\\test_2_data_1k.json"
base_path_5 = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\\extra\\extra_data_223.json"

# file_path  = 'misuse_v3_classification_stage_3_result.json'
# file_path = 'misuse_v3_classification_stage_2.json'
# file_path = 'misuse_v2_stage_1_code_explain.json'
file_path = 'data_all.json'
output_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\\data_all\\data_all.json"


path_list = [base_path_1, base_path_2, base_path_3, base_path_4, base_path_5]

data_all = []
for x in path_list:

    input_path = x
    # read file
    with open(input_path, 'r', encoding="utf-8") as f:
        data = json.load(f)
        print(len(data))
    data_all.extend(data)


with open(output_path, 'w', encoding="utf-8") as f:
    json.dump(data_all, f, indent=4, ensure_ascii=False)
