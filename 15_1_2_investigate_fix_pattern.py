from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from collections import Counter
from dotenv import load_dotenv
import os
import json
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import chromadb
import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

example_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\manual\\fix_rules.json"

example_dict = {}
with open(example_path, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        item = {
            "number": line["number"],
            "change": line["change"].split("\n"),
            "fix_pattern": line["fix_pattern"].split("\n"),
        }
        example_dict[line["number"]] = item
# write to json

with open("C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\manual\\fix_rules_dict.json", "w", encoding="utf-8") as f:
    json.dump(example_dict, f, indent=4, ensure_ascii=False)