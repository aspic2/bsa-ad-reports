
from __future__ import print_function
import base64
import requests
from zipfile import ZipFile
import csv

from app.credentials import Credentials
from app.gmail import GmailApi
from app.sheets import SheetsApi, SpreadsheetMetadata
from os import getcwd

resources_path = getcwd() + '/resources/'

def main():
    creds = Credentials().get()

    message_body = GmailApi(creds).build_service().get_latest_message_body()

    # this is a bytes-like object and needs to be a string
    lines = base64.urlsafe_b64decode(message_body.encode('ASCII'))
    lines = str(lines, 'utf-8').split('\r\n')

    download_link = [line for line in lines if "https://download.flashtalking.com" in line][0]

    # download the zip file
    download_response = requests.get(download_link)
    zip_path = resources_path + 'downloaded.zip'
    with open(zip_path, 'wb+') as myzip:
        myzip.write(download_response.content)

    # get the csv from the zip
    csv_name = ''
    csv_content = None

    with ZipFile(zip_path) as z_file:
        csv_name = z_file.namelist()[0]
        # not the safest way to format data
        csv_content = str(z_file.read(csv_name), 'utf-8').replace('"', '')

    # this file is currenlty unused
    with open(resources_path + 'read_zip_data.csv', 'w') as f:
        f.write(csv_content)

    content_as_list = csv_content.split("\n")
    formatted_reporting_data = [x.split(',') for x in content_as_list]


    updated_spreadsheet = SheetsApi(creds, SpreadsheetMetadata()).build_service().write_to_spreadsheet(formatted_reporting_data)

    print("main.py successfully completed")

if __name__ == '__main__':
    main()
