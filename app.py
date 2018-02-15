import json
import base64
import requests
import string
import random
import schedule
import time

def job():
    token = "b7885278fa80397a101f61daae366584aed3e3a4"
    filename = "README.md"
    repo = "nikhilnayak98/gitcommitter"
    branch = "master"
    push_to_github(filename, repo, branch, token)
    print("I'm working...")

schedule.every().day.at("21:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)

def generate_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def push_to_github(filename, repo, branch, token):
    url = "https://api.github.com/repos/" + repo + "/contents/" + filename

    filecontents = generate_string()

    with open(filename, "w") as f:
        f.write(filecontents)

    base64content = base64.b64encode(open(filename,"rb").read())

    data = requests.get(url+'?ref='+branch, headers = {"Authorization": "token "+token}).json()
    print(data)
    sha = data['sha']

    if base64content.decode('utf-8')+"\n" != data['content']:
        message = json.dumps({"message": generate_string(3, filecontents),
                            "branch": branch,
                            "content": base64content.decode("utf-8") ,
                            "sha": sha
                            })

        resp=requests.put(url, data = message, headers = {"Content-Type": "application/json", "Authorization": "token "+token})

        print(resp)
    else:
        print("nothing to update")
    
