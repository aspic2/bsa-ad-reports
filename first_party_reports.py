from app.bsa_api_connections import LineItems
import random

def first_party_reports():
    advertiser = random.choice(bsa_api_keys.keys())
    data = LineItems(advertiser).get_json_response()
