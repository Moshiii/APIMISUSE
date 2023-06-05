# read manual.json 
import json
with open("C:\@code\APIMISUSE\manual.json", "r", encoding="utf-8") as f:
    data=json.load(f)
# print(data)
print(len(data))
keywords={"device":["GPU", "CUDA", "CPU", "TPU", "device", "device_type"]}
keywords={"misuse":["incorrect usage", "misuse", "wrong usage","API usage"]}

counter=0
for d in data:
    for kw in keywords["misuse"]:
        if kw in d["commit_message"]:
            counter+=1
print(counter)