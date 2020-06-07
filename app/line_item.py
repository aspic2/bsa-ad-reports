

class LineItem(object):

    def __init__(self, daily_stats):
        self.name = None
        self.id = None
        self.impressions = None
        self.clicks = None
        self.daily_stats = daily_stats

    def total_impressions(self):
        pass

    def total_clicks(self):
        pass

    def set_name(self):
        pass



if __name__ == '__main__':
    main()
