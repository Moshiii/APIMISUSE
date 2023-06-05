import requests
import os
with open('..\\..\\data\\repo\\repo_name_response_json_2.txt', 'r') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
headers = {'Authorization': 'token  <API_TOKEN>'}

counter = 0
for line in lines:
    repo_url = f'https://github.com/{line}'
    zip_url = repo_url + '/archive/master.zip'


    response = requests.head(zip_url, allow_redirects=True)
    repo_size = int(response.headers.get('Content-Length', 0))
    print("repo_size",repo_size,"line",line)
    if repo_size < 20000000:  # 20 MB
        response = requests.get(zip_url,headers=headers)
    else:
        continue

    counter+=1
    print(counter)
    line = line.replace("/", "_")
    #if exist then skip
    if os.path.exists(f'{line}.zip'):
        print(line,"exist")
        continue

    with open(f'{line}.zip', 'wb') as f:
        f.write(response.content)
