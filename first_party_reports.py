from resources.advertisers_info import advertisers_info

from app.bsa_api_connections import DailyStatsApi
from app.dates import Dates
from app.advertiser import Advertiser
from app.sheets import SheetsApi, SpreadsheetMetadata
from app.credentials import Credentials
from app.bsa_data import BsaData

def main():
    google_credentials = Credentials().get()
    advertisers = [Advertiser(a) for a in advertisers_info if a.get("api_key")]
    for advertiser in advertisers:
        formatted_data = get_first_party_reports_for(advertiser)
        if not formatted_data:
            continue
        metadata = {"id": advertiser.get_spreadsheet_id(), "range": advertiser.get_range()}

        updated_spreadsheet = SheetsApi(google_credentials, SpreadsheetMetadata(metadata)).build_service().write_to_spreadsheet(formatted_data)
    return None


def get_first_party_reports_for(advertiser):
    dates = Dates().set()
    data = DailyStatsApi(advertiser).set_dates(dates).get_json_response()
    print("Advertiser = {}".format(advertiser.get_name()))
    if data:
        print("data found")
        formatted_data = BsaData(data).format_and_return_data()
        return formatted_data
    else:
        print("no data found for {} in dates {} to {}".format(
                advertiser, dates.get_start_date(), dates.get_end_date()
                ))
        return None




if __name__ == '__main__':
    main()
