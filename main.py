import requests

from resources.advertisers_info import advertisers_info

from app.credentials import Credentials
from app.gmail import GmailApi, GmailApiService
from app.sheets import SheetsApi, SpreadsheetMetadata
from app.reader import Reader, FileManager, ZipFileManager
from app.advertiser import Advertiser


def main():
    credentials = Credentials().get()
    gmail_service = GmailApiService(credentials).get()
    advertiser = Advertiser(advertisers_info[3])

    reporting_data = get_reporting_data(gmail_service, advertiser)
    formatted_reporting_data = process_reporting_data(reporting_data)
    updated_spreadsheet = write_data_to_spreadsheet(credentials, advertiser, formatted_reporting_data)
    print("updated reporting for {}".format(advertiser.get_name()))


def get_reporting_data(gmail_service, advertiser):
    email_body = GmailApi(gmail_service, advertiser.get_email_subject()).get_latest_message_body()
    download_link = Reader(email_body).get_download_link()
    download_response = requests.get(download_link).content
    return download_response


def process_reporting_data(data):
    zip_file = ZipFileManager("downloaded.zip").write_content(data)
    report_csv = zip_file.read_first_file().return_content_as_stripped_string()
    report_csv_file = FileManager("report.csv").write_content(report_csv)
    formatted_reporting_data = [data.split(',') for data in Reader(report_csv).return_content_as_list()]
    return formatted_reporting_data


def write_data_to_spreadsheet(credentials, advertiser, formatted_data):
    updated_spreadsheet = SheetsApi(credentials, SpreadsheetMetadata({"id": advertiser.get_spreadsheet_id(), "range": advertiser.get_third_party_range(),  })).build_service().write_to_spreadsheet(formatted_data)
    return updated_spreadsheet


if __name__ == '__main__':
    main()
