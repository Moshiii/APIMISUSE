import os
import openai
import json 

openai.api_key = "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"
# response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)


prompt  = "I need your help to identify if a git commit is about an machine learning API usage change or not. "
prompt += "please response with Yes or No followed by the reason in one sentence. Here are some examples:"
prompt += "Example: -    if isinstance(net, torch.nn.Module): +    if isinstance(net, nn.Module):"
prompt += "Answer: No, because  torch.nn.Module is the same as nn.Module. it is just a shorter way to write it."
prompt += "Example: -if __name__ == \"__main__\": +if __name__ == '__main__':"
prompt += "Answer: No, because the given change is irrelevant to the API usage. it is just a code style change."
prompt += "Example: -        net = torch.nn.DataParallel(net) +        net = torch.nn.DataParallel(net).to(device)"
prompt += "Answer: Yes, because it was not required to specify device but now it is required to specify device."

prompt += "Example: -        net = torch.nn.DataParallel(net) +        net = torch.nn.DataParallel(net).to(device)"
prompt += "Answer: Yes, because it was not required to specify device but now it is required to specify device."


base_prompt = prompt

# prompt += "Example: -    return torch.tensor(betas) +    return torch.tensor(betas, dtype=torch.float32)"

# read all files in the folder data\commit\python_chunks\contain_torch_dot_manual_core_chage
files = os.listdir("C:\@code\APIMISUSE\data\commit\python_chunks\contain_torch_dot_manual_core_chage")
for file in files[:3]:
    #read the file
    with open(f"C:\@code\APIMISUSE\data\commit\python_chunks\contain_torch_dot_manual_core_chage\{file}", "r", encoding="utf-8") as f:
        data = json.load(f)
    # print file path
    print(f"C:\@code\APIMISUSE\data\commit\python_chunks\contain_torch_dot_manual_core_chage\{file}")
    for item in data[:3]:
        #check if the core change is empty
        if len(item["core_change"]) == 0:
            continue
        print(item["commit_hash"])
        print(item["index"])
        print(item["core_change"])
        prompt = base_prompt+ "Example: " + item["core_change"][0] + " " + item["core_change"][1]
        prompt += "Answer: "
        response = openai.Completion.create(model="text-curie-001", prompt=prompt, temperature=0)
        #get the response using the API

        # print(response)
        # get the text from the response
        text = response["choices"][0]["text"]
        print(text)
