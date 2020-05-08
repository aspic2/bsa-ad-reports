from __future__ import print_function
from googleapiclient.discovery import build
import base64
import email

from app.credentials import Credentials


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = Credentials().get()

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])
    #
    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])

    response = service.users().threads().list(userId='me', q="label:reports subject:Adobe_BSA ").execute()
    latest_thread = response.get('threads')[0]
    latest_thread_id = latest_thread.get('id')

    message = service.users().messages().get(userId='me', id=latest_thread.get('id')).execute()
    body = message.get('payload').get('body').get('data')

    # this is a bytes-like object and needs to be a string
    lines = base64.urlsafe_b64decode(body.encode('ASCII')).split('\r\n')
    download_links = [line for line in lines if "https://download.flashtalking.com" in line]
    print(download_links)


if __name__ == '__main__':
    main()
