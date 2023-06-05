import os
import json
import subprocess

total_length = 0

for root, dirs, files in os.walk("C:\@code\APIMISUSE\data\misuse_jsons"):
    for file in files:
        if not file.endswith(".json"):
            continue
        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
            print(os.path.join(root, file))
            data = json.load(f)
            length = len(data)
            print(length)
            total_length += length

print(total_length)