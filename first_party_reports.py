from resources.confidential import campaigns_list_hash

from app.bsa_api_connections import DailyStatsApi
from app.dates import Dates
from app.advertiser import Advertiser
from app.sheets import SheetsApi, SpreadsheetMetadata
from app.credentials import Credentials
from app.bsa_data import BsaData
from app.helper import Helper

def main():
    google_credentials = Credentials().get()
    advertisers_info_list = create_advertisers_info_list()
    advertisers = [Advertiser(a) for a in advertisers_info_list if a.get("api_key")]
    for advertiser in advertisers:
        formatted_data = get_first_party_reports_for(advertiser)
        if not formatted_data:
            continue
        metadata = {"id": advertiser.get_spreadsheet_id(), "range": advertiser.get_range()}

        updated_spreadsheet = SheetsApi(google_credentials, SpreadsheetMetadata(metadata)).build_service().write_to_spreadsheet(formatted_data)
    return None


def get_first_party_reports_for(advertiser):
    print("Advertiser = {}".format(advertiser.get_name()))
    dates = Dates().set()

    #for shutterstock
    if advertiser.get_name().lower() == "shutterstock":
        dates = Dates().set_dates_to_current_year()

    data = DailyStatsApi(advertiser).set_dates(dates).get_json_response()

    if data:
        print("data found")
        formatted_data = BsaData(data).format_and_return_data()
        return formatted_data
    else:
        print("no data found for {} in dates {} to {}".format(
                advertiser, dates.get_start_date(), dates.get_end_date()
                ))
        return None


def create_advertisers_info_list():
    metadata = SpreadsheetMetadata(campaigns_list_hash)
    sheets_api = SheetsApi(Credentials().get(), metadata).build_service()
    sheet_values = sheets_api.get_data()
    return Helper.create_advertisers_info_list(sheet_values)



if __name__ == '__main__':
    main()
