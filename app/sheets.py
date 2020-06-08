from googleapiclient.discovery import build

class SheetsApi(object):

    def __init__(self, credentials, metadata):
        self.credentials =  credentials
        self.service = None
        self.sheet = None
        self.metadata = metadata

    def build_service(self):
        self.service = build('sheets', 'v4', credentials=self.credentials)
        return self

    def get_spreadsheet(self):
        # This is currently unused
        self.sheet = self.service.spreadsheets().get(spreadsheetId=self.metadata.get_id()).execute()
        return self

    def clear_spreadsheet(self):
        self.service.spreadsheets().values().clear(spreadsheetId=self.metadata.get_id(), range=self.metadata.get_range()).execute()
        return self

    def write_to_spreadsheet(self, data):
        self.clear_spreadsheet()
        value_range_body = {
            "range": self.metadata.get_range(),
            "majorDimension": "ROWS",
            "values": data
        }
        self.service.spreadsheets().values().update(spreadsheetId=self.metadata.get_id(), range=self.metadata.get_range(), valueInputOption='USER_ENTERED', body=value_range_body).execute()
        return self


class SpreadsheetMetadata(object):

    def __init__(self, md={"id": "1HCuPDapimvZNf3W9uBQOJJuHGQ_xLxFwakBlDvYv6bc", "range": "import_flashtalking!A1:Z"}):
        self.id = md.get("id")
        self.range = md.get("range")

    def get_id(self):
        return self.id

    def get_range(self):
        return self.range


if __name__ == '__main__':
    main()
