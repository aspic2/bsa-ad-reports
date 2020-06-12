from googleapiclient.discovery import build

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
        return message

    def get_latest_message_body(self):
        message = self.get_latest_message()
        # return body of email only
        body = message.get('payload').get('body').get('data')
        return body

    def get_latest_message_attachment(self):
        message = self.get_latest_message()
        attachment_id = message.get('payload').get('body').get('attachmentId')
        if attachment_id:
            attachment = message.attachments.get(attachment_id)
            return attachment


class GmailApiService(object):
    """Create as many API objects as you wish without rebuilding the service"""

    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def get(self):
        return self.service



if __name__ == '__main__':
    main()
