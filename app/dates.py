from datetime import date, timedelta


class Dates(object):

    def __init__(self):
        self.start_date = date.today()-timedelta(6)
        self.end_date = date.today()

    def set_end_date(self):
        # week is set to end on a wednesday
        today = date.today()
        dates = list((date.today()-timedelta(x)) for x in range(14))
        last_wednesday = max(filter(lambda x : x.weekday() == 2, dates))
        self.end_date = last_wednesday
        return self

    def set_start_date(self):
        self.start_date = self.end_date-timedelta(6)
        return self

    def set_dates(self):
        self.set_end_date().set_start_date()
        return self

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date


if __name__ == '__main__':
    main()
