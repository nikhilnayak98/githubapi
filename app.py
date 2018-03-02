import json
import base64
import requests
import string
import random

from flask import Flask, request, render_template, make_response, redirect, url_for
app = Flask(__name__)

@app.route('/')
def my_form():
	token = ""
	filename = ""
	repo = ""
	branch = ""
	push_to_github(filename, repo, branch, token)
	return "working"

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
if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)
