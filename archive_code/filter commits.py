import requests
import time


# Replace ACCESS_TOKEN with your actual access token
headers = {'Authorization': 'token <API_TOKEN>'}
lines=[]
#read txt file
with open('data\\repo\\repo_name_response_json_1.txt', 'r') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

for x in lines[1:]:                 
    OWNER_REPO=x

    url = f"https://api.github.com/repos/{OWNER_REPO}/commits"

    # Retrieve the first page of commits (up to 100)
    response = requests.get(url, headers=headers)

    # Process the first page of commits
    if response.status_code == 200:
        response_json = response.json()
        for commit in response_json:
            for template in ['Bug fix', 'BUGFIX', 'BUG FIX', 'bugfix', 'bug-fix', 'bug fix', 'Bug-fix', 'Bug Fix']:
                if template in commit['commit']['message']:
                    OWNER_REPO_path = OWNER_REPO.replace("/","_")
                    # if  file not exist then create
                    with open(f'data\\commit\\{OWNER_REPO_path}.txt', 'w',  encoding='utf-8') as f:
                        f.write(f"{commit['sha']}\n")
                    # if file exist then append
                    with open(f'data\\commit\\{OWNER_REPO_path}.txt', 'a',  encoding='utf-8') as f:
                        f.write(f"{commit['sha']}\n")

        while "next" in response.links.keys():
            # time.sleep(1)
            # Retrieve the next page of commits
            url = response.links["next"]["url"]
            response = requests.get(url, headers=headers)
            # Process the next page of commits
            if response.status_code == 200:
                response_json = response.json()
                for commit in response_json:
                    for template in ['Bug fix', 'BUGFIX', 'BUG FIX', 'bugfix', 'bug-fix', 'bug fix', 'Bug-fix', 'Bug Fix']:
                        if template in commit['commit']['message']:
                            OWNER_REPO_path = OWNER_REPO.replace("/","_")
                            with open(f'data\\commit\\{OWNER_REPO_path}.txt', 'a', encoding='utf-8') as f:
                                f.write(f"{commit['sha']}\n")
    else:
        print(f"Error: {response.status_code}")

