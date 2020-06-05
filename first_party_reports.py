from resources.bsa_api_keys import bsa_api_keys

from app.bsa_api_connections import LineItemsApi, DailyStatsApi
from app.dates import Dates
import random
from os import getcwd
import csv

def first_party_reports():
    advertiser = random.choice(list(bsa_api_keys.keys()))
    dates = Dates().set()
    data = DailyStatsApi(advertiser).set_dates(dates).get_json_response()
    print("Advertiser = {}".format(advertiser))
    formatted_data = None
    if data:
        formatted_data = list({"lineitem_name": d.get("lineitem_name"),
                                "date": d.get("date"),
                                "impressions": d.get("impressions"),
                                "clicks": d.get("clicks")
                                } for d in data)
        # TODO: Reduce the daily breakdown into single line items with total clicks and impressions
        with open(getcwd() + "/reports/month_to_date_data.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=list(formatted_data[0].keys()), extrasaction='ignore')
            writer.writeheader()
            for row in formatted_data:
                writer.writerow(row)
    print("finished")
    

if __name__ == '__main__':
    first_party_reports()
