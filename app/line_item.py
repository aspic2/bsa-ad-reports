

class LineItem(object):

    def __init__(self, daily_stats):
        self.name = None
        self.id = None
        self.impressions = None
        self.clicks = None
        self.daily_stats = daily_stats
        self.start_of_data = None
        self.end_of_data = None

    def build(self):
        self.set_name().total_impressions().total_clicks().set_dates()
        return self

    def total_impressions(self):
        self.impressions = sum(int(x.get("impressions")) for x in self.daily_stats)
        return self

    def total_clicks(self):
        self.clicks = sum(int(x.get("clicks")) for x in self.daily_stats)
        return self

    def set_name(self):
        self.name = self.daily_stats[0].get("lineitem_name")
        return self

    def get_name(self):
        return self.name

    def get_impressions(self):
        return self.impressions

    def get_clicks(self):
        return self.clicks

    def set_dates(self):
        dates = list(x.get("date") for x in self.daily_stats)
        # Relies on dates arriving in YYYY-MM-DD format and sorting alphabetically
        self.start_of_data = min(dates)
        self.end_of_data = max(dates)
        return self



if __name__ == '__main__':
    main()
