import requests


class API(object):
    def __init__(self, advertiser):
        self.advertiser_name = advertiser.get_name()
        self.credentials = advertiser.get_api_key()
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

    def set_dates(self, dates):
        self.startDate = dates.get_start_date()
        self.endDate = dates.get_end_date()
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



class LineItemsApi(API):
    def __init__(self, advertiser):
        API.__init__(self, advertiser)
        self.url_appendix = "lineitems"


class DailyStatsApi(API):
    def __init__(self, advertiser):
        API.__init__(self, advertiser)
        self.url_appendix = "daily-stats"


if __name__ == '__main__':
    main()
