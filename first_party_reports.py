from resources.advertisers_info import advertisers_info

from app.bsa_api_connections import LineItemsApi, DailyStatsApi
from app.dates import Dates
from app.line_item import LineItem
from app.advertiser import Advertiser
from app.sheets import SheetsApi, SpreadsheetMetadata
from app.credentials import Credentials
import random
from os import getcwd
import csv

def first_party_reports():
    # TODO: Create an Advertiser object to store advertiser name, google sheet urls
    # TODO: retrieved data, and other resources
    advertiser = Advertiser(advertisers_info[0])
    dates = Dates().set()
    data = DailyStatsApi(advertiser).set_dates(dates).get_json_response()
    print("Advertiser = {}".format(advertiser.get_name()))
    formatted_data = None
    if data:
        line_items = []
        line_item_names = set(x.get("lineitem_name") for x in data)
        formatted_data = list({"lineitem_name": d.get("lineitem_name"),
                                "date": d.get("date"),
                                "impressions": d.get("impressions"),
                                "clicks": d.get("clicks")
                                } for d in data)

        for l in line_item_names:
            relevant_stats = [x for x in formatted_data if x.get("lineitem_name") == l]
            line_items.append(LineItem(relevant_stats).build())
        # TODO: Now what do you want to do with the relevant data?
        spreadsheet_formatted_data = [[l.get_name(), l.get_impressions(), l.get_clicks()] for l in line_items]
        spreadsheet_formatted_data[0] = ["name", "impressions", "clicks"]
        print(spreadsheet_formatted_data)

        metadata = {"id": advertiser.get_spreadsheet_id(), "range": advertiser.get_range()}
        google_credentials = Credentials().get()
        updated_spreadsheet = SheetsApi(google_credentials, SpreadsheetMetadata(metadata)).build_service().write_to_spreadsheet(spreadsheet_formatted_data)

        # with open(getcwd() + "/reports/month_to_date_data.csv", "w") as f:
        #     writer = csv.DictWriter(f, fieldnames=list(formatted_data[0].keys()), extrasaction='ignore')
        #     writer.writeheader()
        #     for row in formatted_data:
        #         writer.writerow(row)
    else:
        print("no data found for {} in dates {} to {}".format(
                advertiser, dates.get_start_date(), dates.get_end_date()
                ))
    print("finished")


if __name__ == '__main__':
    first_party_reports()
