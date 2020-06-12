from resources.advertisers_info import advertisers_info

class Advertiser(object):

    def __init__(self, info):
        self.name = info.get("name")
        # TODO: Plenty of unused attributes here. Maybe subclass them?
        self.bsa_api_key = info.get("api_key")
        self.spreadsheet_id = info.get("spreadsheet_id")
        self.tab_name = info.get("tab_name")
        self.third_party_tab_name = info.get("third_party_tab_name")
        self.email_subject = info.get("email_subject")
        self.email_attachment_name = info.get("email_attachment_name")
        self.stats = None

    def set_stats(self):
        self.stats = gather_and_calculate_stats()
        return self

    def get_stats(self):
        return self.stats

    def get_api_key(self):
        return self.bsa_api_key

    def get_name(self):
        return self.name

    def get_spreadsheet_id(self):
        return self.spreadsheet_id

    def get_range(self, range="!B1:Z"):
        # default to leaving column A open
        return self.tab_name + range



if __name__ == '__main__':
    main()
