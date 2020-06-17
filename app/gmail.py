from googleapiclient.discovery import build
import base64
from datetime import date

class GmailApi(object):

    def __init__(self, service, query):
        self.service = service
        self.query = query

    def get_lastest_thread(self):
        gmail_response = self.service.users().threads().list(userId='me', q=self.query).execute()
        latest_thread = gmail_response.get('threads')[0]
        return latest_thread

    def get_latest_message(self):
        latest_thread = self.get_lastest_thread()
        message = self.service.users().messages().get(userId='me', id=latest_thread.get('id')).execute()
        # must convert .get("internalDate") from ms to s
        latest_message_date = date.fromtimestamp(int(message.get("internalDate"))/1000)
        print("Latest message from {}".format(latest_message_date))
        return message

    def get_latest_message_body(self):
        message = self.get_latest_message()
        # return body of email only
        body = message.get('payload').get('body').get('data')
        return body

    def get_latest_message_attachment(self):
        message = self.get_latest_message()
        attachments = list(x for x in message.get('payload').get('parts') if x.get('filename'))
        if not attachments:
            return None
        print("Number of attachments = {}".format(len(attachments)))
        #default to first attachment
        attachment_id = attachments[0].get('body').get('attachmentId')
        attachment = self.service.users().messages().attachments().get(userId='me', messageId=message.get('id'), id=attachment_id).execute().get('data')
        # attachemnt needs to be decoded to be written as a useful .zip file
        attachment = base64.urlsafe_b64decode(attachment.encode('UTF-8'))
        return attachment


class GmailApiService(object):
    """Create as many API objects as you wish without rebuilding the service"""

    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def get(self):
        return self.service



if __name__ == '__main__':
    main()
