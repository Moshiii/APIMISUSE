import requests
import time

# # Replace ACCESS_TOKEN with your actual access token
# headers = {'Authorization': 'token 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'}
headers = {'Authorization': 'token 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'}



def get_response(url):
    response = requests.get(url, headers=headers)
    response_json = response.json()
    counter=0
    print(response_json)
    for item in response_json['items']:
        print(item['repository']['full_name'])
        print(item['path'])
        print(item['html_url'])
        counter+=1
        print(counter)

for x in range(0, 1000):
    time.sleep(1)
    idx=x
    # url = f'https://api.github.com/search/repositories?q=pytorch+language:python&sort=stars&page={idx}&per_page=100'
    url = f'https://api.github.com/search/repositories?q=tensorflow+language:python&sort=stars&page={idx}&per_page=100'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        repo_names = [item["full_name"] for item in response_json["items"]]
        name = f"data\\repo_tensorflow\\repo_name_response_tf_json_{idx}.txt"
        with open(name, "w") as f:
            for item in repo_names:
                f.write("%s\n" % item)
        print(f"Page {idx} saved to {name}")
        
    else:
        print(f"Error: {response.status_code}")