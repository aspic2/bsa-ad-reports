from __future__ import print_function
from googleapiclient.discovery import build
import base64
import email
import requests
from zipfile import ZipFile
import csv

from app.credentials import Credentials


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = Credentials().get()

    gmail_service = build('gmail', 'v1', credentials=creds)

    # Retrieve latest Adobe email
    gmail_response = gmail_service.users().threads().list(userId='me', q="label:reports subject:Adobe_BSA ").execute()
    latest_thread = gmail_response.get('threads')[0]
    latest_thread_id = latest_thread.get('id')
    message = gmail_service.users().messages().get(userId='me', id=latest_thread.get('id')).execute()

    # return body of email only
    body = message.get('payload').get('body').get('data')

    # this is a bytes-like object and needs to be a string
    lines = base64.urlsafe_b64decode(body.encode('ASCII'))
    lines = str(lines, 'utf-8').split('\r\n')

    download_link = [line for line in lines if "https://download.flashtalking.com" in line][0]

    # download the zip file
    download_response = requests.get(download_link)
    zip_name = 'downloaded.zip'
    with open(zip_name, 'wb+') as myzip:
        myzip.write(download_response.content)

    # get the csv from the zip
    csv_name = ''
    csv_content = None

    with ZipFile(zip_name) as z_file:
        csv_name = z_file.namelist()[0]
        # not the safest way to format data
        csv_content = str(z_file.read(csv_name), 'utf-8').replace('"', '')

    # this file is currenlty unused
    with open('read_zip_data.csv', 'w') as f:
        csv_writer = csv.writer(f, delimiter=",")
        for row in csv_content:
            csv_writer.writerow(row)


    # write the CSV to the appropriate spreadsheet
    spreadsheet_id = '1HCuPDapimvZNf3W9uBQOJJuHGQ_xLxFwakBlDvYv6bc'
    spreadsheet_range = 'import_flashtalking!A1:Z'
    sheets_service = build('sheets', 'v4', credentials=creds)
    sheets_response = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    # clear current data
    sheets_service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=spreadsheet_range).execute()

    # write new data
    content_as_list = csv_content.split("\n")
    list_of_lists = [x.split(',') for x in content_as_list]

    value_range_body = {
        "range": spreadsheet_range,
        "majorDimension": "ROWS",
        "values": list_of_lists
    }
    sheets_service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=spreadsheet_range, valueInputOption='USER_ENTERED', body=value_range_body).execute()

if __name__ == '__main__':
    main()
