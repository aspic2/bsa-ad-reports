from resources.bsa_api_keys import bsa_api_keys

from app.bsa_api_connections import LineItems
import random

def first_party_reports():
    advertiser = random.choice(list(bsa_api_keys.keys()))
    data = LineItems(advertiser).get_json_response()
    print("Advertiser = {}".format(advertiser))
    print(data)

if __name__ == '__main__':
    first_party_reports()
