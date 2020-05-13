
import requests

from app.credentials import Credentials
from app.gmail import GmailApi
from app.sheets import SheetsApi, SpreadsheetMetadata
from app.reader import Reader, FileManager, ZipFileManager


def main():
    credentials = Credentials().get()
    email_body = GmailApi(credentials).build_service().get_latest_message_body()
    download_link = Reader(email_body).get_download_link()

    # download the zip file
    download_response = requests.get(download_link)
    zip_file = ZipFileManager("downloaded.zip").write_content(download_response.content)
    report_csv = zip_file.read_first_file().return_content_as_stripped_string()
    report_csv_file = FileManager("report.csv").write_content(report_csv)

    formatted_reporting_data = [data.split(',') for data in Reader(report_csv).return_content_as_list()]

    updated_spreadsheet = SheetsApi(credentials, SpreadsheetMetadata()).build_service().write_to_spreadsheet(formatted_reporting_data)

    print("main.py successfully completed")

if __name__ == '__main__':
    main()
