from googleapiclient.discovery import build

class GmailApi(object):

    def __init__(self, credentials):
        self.credentials = credentials
        self.service = None

    def build_service(self):
        self.service = build('gmail', 'v1', credentials=self.credentials)
        return self

    def get_lastest_thread(self):
        gmail_response = self.service.users().threads().list(userId='me', q="label:reports subject:Adobe_BSA ").execute()
        latest_thread = gmail_response.get('threads')[0]
        return latest_thread

    def get_latest_message_body(self):
        latest_thread = self.get_lastest_thread()
        message = self.service.users().messages().get(userId='me', id=latest_thread.get('id')).execute()
        # return body of email only
        body = message.get('payload').get('body').get('data')
        return body
