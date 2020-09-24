from .models import Yelp
import os
import requests
import json

def get_yelp(query, locale):
    url = f"https://api.yelp.com/v3/businesses/search?term={query}&location={locale}"
    req = requests.get(
        url, headers={'Authorization': 'Bearer %s' % os.environ['API_KEY']})
    response = req.json()
    yelps_list = []
    for bus in response['businesses']:
        yelps_list.append(bus)

    return yelps_list

def get_details(yelp_id):
    url = f"https://api.yelp.com/v3/businesses/{yelp_id}"
    # new_yelp = 
    # new_yelp.business_id = yelp_id
    # new_yelp.save()
    req = requests.get(
        url, headers={'Authorization': 'Bearer %s' % os.environ['API_KEY']})
    response = req.json()
    return response