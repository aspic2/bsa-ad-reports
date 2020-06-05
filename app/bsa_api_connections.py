import requests
from resources.bsa_api_keys import bsa_api_keys

class API(object):
    def __init__(self, advertiser):
        self.advertiser = advertiser
        self.credentials = bsa_api_keys.get(self.advertiser)
        self.base_url = "https://papi.buysellads.com/"
        self.url = self.base_url
        self.url_appendix = ""
        self.type = "csv"
        self.query = {"key": self.credentials}
        self.startDate = ""
        self.endDate = ""
        self.lineitemId = ""

    def build_url(self):
        self.url += self.url_appendix
        return self

    def build_query(self):
        if self.startDate:
            self.query["startDate"] = self.startDate
        if self.endDate:
            self.query["endDate"] = self.endDate
        if self.lineitemId:
            self.query["lineitemId"] = self.lineitemId
        return self

    def prep_url(self):
        self.build_query().build_url()
        return self

    def get(self):
        return requests.get(self.url, params = self.query)

    def get_json_response(self):
        return self.prep_url().get().json()



class LineItems(API):
    def __init__(self, advertiser):
        API.__init__(self, advertiser)
        self.url_appendix = "lineitems"


class DailyStats(API):
    def __init__(self, advertiser, dates):
        API.__init__(self, advertiser)
        self.url_appendix = "daily-stats"
        self.startDate = dates.get_start_date()
        self.endDate = dates.get_end_date()


if __name__ == '__main__':
    main()
