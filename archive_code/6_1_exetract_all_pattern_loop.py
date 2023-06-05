from six_extract_add_Error import execute_six_extract_add_Error
from six_extract_add_none import execute_six_extract_add_none
from six_extract_add_not_none import execute_six_extract_add_not_none
from six_extract_argument_replace import execute_six_extract_argument_replace
from six_extract_device_misuse import execute_six_extract_device_misuse
from six_extract_if_condition import execute_six_extract_if_condition

import json

#pytorch
match_word = "nn"
match_word = "torch"
match_word = "autograd"
match_word="optim"
match_word="functional"
match_word="dataloader"
match_word="datasets"
match_word="cuda"

#tensorflow
match_word="tf"
match_word="tensorflow"
match_word="keras"
match_word="layers"
match_word="models"



with open(f"C:\@code\APIMISUSE\\filter_by_fix_{match_word}.json", "r", encoding="utf-8") as f:
    data = json.load(f)

res = execute_six_extract_add_Error(match_word, data)
with open(f"C:\@code\APIMISUSE\\data\\misuse_jsons\\filter_by_fix_{match_word}_add_Error.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=4)
res = execute_six_extract_add_none(match_word, data)
with open(f"C:\@code\APIMISUSE\\data\\misuse_jsons\\filter_by_fix_{match_word}_add_none.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=4)
res = execute_six_extract_add_not_none(match_word, data)
with open(f"C:\@code\APIMISUSE\\data\\misuse_jsons\\filter_by_fix_{match_word}_add_not_none.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=4)
res = execute_six_extract_argument_replace(match_word, data)
with open(f"C:\@code\APIMISUSE\\data\\misuse_jsons\\filter_by_fix_{match_word}_argument_replace.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=4)
res = execute_six_extract_device_misuse(match_word, data)
with open(f"C:\@code\APIMISUSE\\data\\misuse_jsons\\filter_by_fix_{match_word}_device_misuse.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=4)
res = execute_six_extract_if_condition(match_word, data)
with open(f"C:\@code\APIMISUSE\\data\\misuse_jsons\\filter_by_fix_{match_word}_if_condition.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=4)
