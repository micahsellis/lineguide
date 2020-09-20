import os
import requests
import json

def get_yelp():
    url = "https://api.yelp.com/v3/businesses/search?term=chinese&location=Denver"
    req = requests.get(
        url, headers={'Authorization': 'Bearer %s' % os.environ['API_KEY']})
    response = req.json()
    yelps_list = []
    for bus in response['businesses']:
        yelps_list.append(bus['id'])
    return yelps_list
