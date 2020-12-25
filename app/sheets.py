from googleapiclient.discovery import build

from resources.confidential import campaigns_list_hash


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

    def get_data(self):
        # TODO: Get this code working
        response = self.service.spreadsheets().values().get(spreadsheetId=self.metadata.id, range=self.metadata.range).execute()
        return response.get('values', [])


class SpreadsheetMetadata(object):

    def __init__(self, metadata):
        self.id = metadata.get("id")
        self.range = metadata.get("range")

    def get_id(self):
        return self.id

    def get_range(self):
        return self.range


if __name__ == '__main__':
    main()
