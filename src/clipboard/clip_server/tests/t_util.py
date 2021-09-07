import requests

def wipe():
    requests.delete('http://localhost:5000/clips')