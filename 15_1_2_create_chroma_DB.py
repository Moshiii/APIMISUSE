import json
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import chromadb
import os
from dotenv import load_dotenv
load_dotenv()
base_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\manual\\"
input_path = base_path + "manual_invest_data_1k.json"
# rule_path = base_path + "misuse_report.json"
rule_path = base_path + "fix_rules.json"


client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                  persist_directory="C:\@code\APIMISUSE\chroma_db"
                                  ))

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"],
    model_name="text-embedding-ada-002"
)
# API_misuse_fix_pattern_rules
collection = client.get_or_create_collection(
    "fix_rules", embedding_function=openai_ef)
collection_list = client.list_collections()
print(collection_list)

data_dict = {}
with open(input_path, encoding="utf-8") as f:
    data = json.load(f)
    for line in data:
        item = {
            "number": line["number"],
            "change": line["change"],
        }
        data_dict[line["number"]] = item

print(data_dict[4].keys())

# read input_path
rule_dict = {}
with open(rule_path, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        item = {
            "number": line["number"],
            "change": line["change"],
            "fix_pattern": line["fix_pattern"],
        }
        rule_dict[line["number"]] = item

print(rule_dict[4].keys())

data_list = []
for key in data_dict.keys():
    if key in rule_dict.keys():
        data_dict[key]["fix_pattern"] = rule_dict[key]["fix_pattern"]
        data_dict[key]['change'] = "\n".join(data_dict[key]['change'])
        data_list.append(data_dict[key])

print(len(data_list))
print(data_list[0])

documents = []
ids = []
for x in data_list:
    documents.append(x["change"])
    ids.append(str(x["number"]))
print("start db injection")

collection.add(
    documents=documents,
    ids=ids,
)
print("finished")
