import requests

# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
#===============================================================================
#update this API every time
#===============================================================================
with open('C:\@code\\text-generation-webui\API\HOST.txt', 'r') as f:
    HOST = f.read().strip().split('/')[2]
    
URI = f'http://{HOST}/api/v1/generate'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'


def run(prompt):
    request = {
        'prompt': prompt,
        'max_new_tokens': 250,
        'do_sample': True,
        'temperature': 0.01,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'repetition_penalty': 1.18,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        print(prompt + result)


if __name__ == '__main__':
    prompt = "In order to make homemade bread, follow these steps:\n1)"


    text_1 = f"""
    Making a cup of tea is easy! First, you need to get some \ 
    water boiling. While that's happening, \ 
    grab a cup and put a tea bag in it. Once the water is \ 
    hot enough, just pour it over the tea bag. \ 
    Let it sit for a bit so the tea can steep. After a \ 
    few minutes, take out the tea bag. If you \ 
    like, you can add some sugar or milk to taste. \ 
    And that's it! You've got yourself a delicious \ 
    cup of tea to enjoy.
    """
    prompt = f"""
    You will be provided with text delimited by triple quotes. 
    If it contains a sequence of instructions, \ 
    re-write those instructions in the following format:

    Step 1 - ...
    Step 2 - …
    …
    Step N - …
    \"\"\"{text_1}\"\"\"
    """

    run(prompt)
