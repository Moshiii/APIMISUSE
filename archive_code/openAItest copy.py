import os
import openai
import json

openai.api_key = "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"


def craft_prompt(code_diff):
    prompt = "please think of yourself as a professional senior programmer."
    # prompt += "I am going to give you a piece of git commit."
    # prompt += "Please reply yes if you understand."

    # prompt += "This is the list of API misuse categories:"
    # prompt += "1. Argument misuse: incorrect or invalid arguments passed to an API function."
    # prompt += "2. Return value misuse: incorrect or invalid return values from an API function."
    # prompt += "3. State misuse: incorrect or invalid state of an object or system when calling an API function."
    # prompt += "4. Control flow misuse: incorrect or invalid control flow in the use of an API function."
    # prompt += "5. Exception handling misuse: incorrect or invalid exception handling in the use of an API function."
    # prompt += "6. Resource management misuse: incorrect or invalid management of resources (e.g., memory, files) used by an API function."
    # prompt += "7. Interface misuse: incorrect or invalid use of the interface provided by an API function."
    # prompt += "8. Type misuse: incorrect or invalid data types used in the parameters, return values, or variables associated with an API function."
    # prompt += "9. Naming and documentation misuse: incorrect or inconsistent naming and documentation of APIs and their components."
    # prompt += "10. Semantic constraint violation: violation of semantic constraints imposed by the design and specification of APIs."
    # prompt += "11. Security constraint violation: violation of security constraints imposed by the design and specification of APIs."
    # prompt += "12. Performance constraint violation: violation of performance constraints imposed by the design and specification of APIs."
    # prompt += "13. Compatibility constraint violation: violation of compatibility constraints imposed by the design and specification of APIs."
    # prompt += "14. Hardware constraint violation: violation of hardware constraints imposed by the design and specification of APIs."
    # prompt += "15. hardware consistency constraint violation: violation of hardware consistency constraints imposed by the design and specification of APIs."
    # prompt += "16. tensor shape constraint violation: violation of tensor shape constraints imposed by the design and specification of APIs."
    # prompt += "17. distributed related misuse: API behavior is not compatible with distributed training."
    # prompt += "18. mathmatical API misuse: API behavior is not compatible with mathmatical operation."

    # prompt += "can you review the following code and tell me if the code diff is related to a fix of API misuse and which category it is in one short sentence?"
    prompt += "please understand the motivation of the following code diff:"
    prompt += code_diff
    prompt += "based on your understanding, can you tell me if the code diff is related to a fix of API misuse?"
    prompt += "Please start the answer with yes or no followed by a short explain."
    return prompt


def call_api_with_code_diff(prompt):

    completions = openai.Completion.create(
        engine="text-davinci-002",
        # engine="text-ada-001",
        prompt=prompt,
        max_tokens=50,
        n=1
    )
    message = completions.choices[0].text.strip()
    # print(message)
    return message


def dummpy_test_with_code_diff(prompt):
    message = ""

    return message


# ==================main=======================
state = None

# load the data C:\@code\APIMISUSE\filter_by_fix.json
with open("C:\@code\APIMISUSE\\filter_by_fix.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    data = data[:4]
    print(len(data))
    for item in data:
        # print(item["commit_message"])
        # print core change
        # print(item["core_change"])
        code_diff = "\n".join(item["core_change"])
        print("=====================================")
        # print(code_diff)
        prompt = craft_prompt(code_diff)
        message = call_api_with_code_diff(prompt)
        if message == "":
            print("empty message")
        print(message)
        pass
