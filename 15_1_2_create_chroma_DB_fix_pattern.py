import json
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import chromadb
import os
from dotenv import load_dotenv
load_dotenv()
base_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\manual\\"
input_path = base_path + "manual_invest_data_1k.json"
rule_path = base_path + "fix_rules.json"
rule_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\data_all\\fix_rules.json"

def parse_fix_pattern(input_str):
    input_str = input_str.replace("\n", "").lower().replace("fix pattern:","fix_pattern:")
    if "fix_pattern:" in input_str:
        output_str = input_str.split("fix_pattern:")[1]
    else:
        print("error: fix_pattern: not found")
        output_str = ""
    return output_str

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                  persist_directory="C:\@code\APIMISUSE\chroma_db"
                                  ))

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"],
    model_name="text-embedding-ada-002"
)
# API_misuse_fix_pattern_rules
collection = client.get_or_create_collection(
    "fix_rules_pattern_enbedding_900", embedding_function=openai_ef)
collection_list = client.list_collections()
print(collection_list)

rule_dict = {}
with open(rule_path, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    for line in data:
        item = {
            "number": line["number"],
            "change": line["change"],
            "fix_pattern": parse_fix_pattern(line["fix_pattern"]),
        }
        rule_dict[line["number"]] = item

data_list = []
for key in rule_dict.keys():
    data_list.append(rule_dict[key])

print(len(data_list))
print(data_list[0])

documents = []
ids = []
for x in data_list:
    fix_pattn = x["fix_pattern"]
    if fix_pattn == "":
        continue
    print("=====================================")
    print(fix_pattn)
    documents.append(fix_pattn)
    ids.append(str(x["number"]))
print("start db injection")

# collection.add(
#     documents=documents,
#     ids=ids,
# )
# print("finished")
