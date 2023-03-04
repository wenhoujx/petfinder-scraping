import os
import requests
import json
import re 
import time 

PETFINDER_API = "PETFINDER_API"
PETFINDER_SECRET = "PETFINDER_API_SECRET"

api_value = os.getenv(PETFINDER_API)
secret_value = os.getenv(PETFINDER_SECRET)

def to_json(res) : 
    return json.loads(res.text)

# get auth 
auth_res = requests.post("https://api.petfinder.com/v2/oauth2/token", data=f"grant_type=client_credentials&client_id={api_value}&client_secret={secret_value}", headers={
    'Content-Type':  "application/x-www-form-urlencoded"
})
access_token = to_json(auth_res)['access_token']

animal_types = ['dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard']


counts = []
for type_ in animal_types: 
    get_animals_res = requests.get(f"https://api.petfinder.com/v2/animals?type={type_}&limit=1", headers={
        "Authorization": f"Bearer {access_token}"
    })
    count = to_json(get_animals_res)['pagination']['total_count']
    counts.append({"type": type_, "count": count})

with open('counts.json', 'w+') as ff: 
    json.dump(
        { "time_ms": round(time.time() * 1000) , 
         "counts": counts } , ff )
