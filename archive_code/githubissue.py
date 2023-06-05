from github import Github
import os

# Create a Github instance using your personal access token
g = Github(" <API_TOKEN>")

# Get the repository object
repo_name="huggingface/transformers"
repo = g.get_repo(repo_name)

# Get all the issues in the repository
issues = repo.get_issues(state="closed")

# Loop through the issues and extract relevant information
for issue in issues:
    # get issue number
    issue_number = issue.number
    thread_ourput=[]    
    print("Issue Title:", issue.title)
    print("Issue State:", issue.state)
    print("Issue Author:", issue.user.login)
    print("Issue Created At:", issue.created_at)
    print("Issue Body:", issue.body)
    print("="*50)
    thread_ourput.append(issue.title)
    thread_ourput.append(issue.state)
    thread_ourput.append(issue.user.login)
    thread_ourput.append(issue.created_at)
    thread_ourput.append(issue.body)
    thread_ourput.append("="*50)
    
    # Get the comments for the issue
    comments = issue.get_comments()
    
    # Loop through the comments and extract relevant information
    for comment in comments:
        print("Comment Author:", comment.user.login)
        print("Comment Created At:", comment.created_at)
        print("Comment Body:", comment.body)
        print("-"*50)
        thread_ourput.append(comment.user.login)
        thread_ourput.append(comment.created_at)
        thread_ourput.append(comment.body)
        thread_ourput.append("-"*50)
    #write thread_ourput to file
    repo_name = repo_name.replace("/", "_")
    # if exist then skip
    if os.path.exists(f'data\\issue\\{repo_name}_issue_{issue_number}.txt'):
        print(f'data\\issue\\{repo_name}_issue_{issue_number}.txt',"exist")
        continue
    with open(f'data\\issue\\{repo_name}_issue_{issue_number}.txt', 'w', encoding="utf-8") as f:
        for item in thread_ourput:
            f.write("%s\n" % item)
