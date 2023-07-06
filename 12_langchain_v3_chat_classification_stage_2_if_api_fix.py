from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
from dotenv import load_dotenv
import os
import json
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


base_path = "C:\@code\APIMISUSE\data\misuse_jsons\\auto_langchain\\test_1\\"
input_path = base_path + "test_1_data_1k.json"
stage_1_path = base_path + "misuse_v2_stage_1_code_explain.json"
output_path = base_path + "misuse_v2_stage_1_code_explain.json"

data_dict = {}
with open(input_path, encoding="utf-8") as f:
    data_manual = json.load(f)
    for line in data_manual:
        data_dict[line["number"]] = line

data_stage_2_dict = {}
with open(stage_1_path, encoding="utf-8") as f:
    data = f.readlines()
    data = [line for line in data if line != "\n"]
    data = [json.loads(line) for line in data]
    # data = data[:1000]
    print(len(data))
    for line in data:
        data_stage_2_dict[line["number"]] = line


# merge data_stage_1_dict into data_dict by key
for key in data_dict.keys():
    if key in data_stage_2_dict.keys():
        data_dict[key]["code_change_explaination"] = data_stage_2_dict[key]["code_change_explaination"]

# convert data_dict to list
data = []
for key in data_dict.keys():
    if "code_change_explaination" in data_dict[key].keys():
        data.append(data_dict[key])

print(len(data))

template_1 = """
You are an experienced software developer.
You are great at explain code changes in a concise and easy to understand manner.
When you don't know the answer to a question you admit that you don't know.

Please read the definition of API misuse, code change explaination, removed code, and added code and Answer the question at the end:
first read the definition of API misuse, these are rules that you must follow to answer the question correctly.
then read the context, code change explaination, 
then you need to compare the removed code and added code to what has been changed.
if the code change is spacing ,formatting, or comment, answer no.
if added and remove code are almost the same, answer no.
if added and remove code are not related to API call, answer no.
if added and remove code are not using Machine learning related API, answer no.
rename variable are not API misuse fix, answer no.
change code formatting, code style are not API misuse fix, answer no.
change type annotation in def <function>(var: type annotation) is not API misuse fix, answer no.
arr, remove, change string value or comment are not API misuse fix, answer no.
arr, remove, change import are not API misuse fix, answer no.
arr, remove, change method defination are not API misuse fix, answer no.


positive sign of API misuse:
API misuse is when a developer uses an API in a way that is not intended by the API designer.
API misuse fix include Deprecation API fix, shape,type, dtype fix, null reference check fix.
API misuse fix include GPU, CPU, parallelization, or distributed fix, 
API misuse fix include no_grad(), is_training, or eval() fix, missing epsilon or atol, incorrect loss function, or incorrect gradient calculation fix
API misuse fix include fix the if statement or with statement right before calling API. 
API misuse fix must have code change related to API call in the context section.
API misuse fix highly likely to have API call in the added code section.


context: 
{change_code}

code change explaination:
{code_change_explaination}

removed code: 
{removed_code}

added code: 
{added_code}

<answer start>

Questions:    
is this a API misuse fix?

Answer: (Yes, No, Maybe)
"""


@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(4))
def completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)
#1604
for i in range(0, len(data)):
    print("current_index:", i, "/", len(data))

    # commit_message = "{}\n".format(data[i]["commit_message"])
    change = ""
    removed = ""
    added = ""

    for j in range(0, len(data[i]["change"])):
        line = data[i]["change"][j]
        change += "{}\n".format(data[i]["change"][j])
        if line.startswith("-"):
            removed += "{}\n".format(data[i]["change"][j])
        if line.startswith("+"):
            added += "{}\n".format(data[i]["change"][j])
    number = data[i]["number"]
    print("number", number)
    # continue
    # print("commit_message", len(commit_message))
    print("change", len(change))
    print("removed", len(removed))
    print("added", len(added))

    code_change_explaination = data[i]["code_change_explaination"]
    print("code_change_explaination", len(code_change_explaination))
    prompt_1 = template_1.format(
        change_code=change, removed_code=removed, added_code=added, code_change_explaination=code_change_explaination)
    print("prompt_1", len(prompt_1))

    code_change_explaination = completion_with_backoff(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt_1}
        ]
    )
    # code_change_explaination = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "user", "content": prompt_1}
    #     ]
    # )
    code_change_explaination = code_change_explaination["choices"][0]["message"]["content"]

    output = {
        "number": number,
        "answer": code_change_explaination,
    }

    with open(output_path, 'a') as f:
        json.dump(output, f)
        f.write(os.linesep)
