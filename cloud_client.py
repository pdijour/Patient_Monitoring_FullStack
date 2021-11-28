# cloud_client.py

import requests

server = "http://127.0.0.1:5000"

def main():
    # Check if server running
    r = requests.get(server + "/")
    print(r.status_code)
    print(r.text)
