from datetime import date, timedelta


class Dates(object):

    def __init__(self):
        self.today = date.today()
        self.end_date = self.today
        self.start_date = self.today -timedelta(6)

    def set_end_date_to_last_wednesday(self):
        dates = list((self.today-timedelta(x)) for x in range(14))
        last_wednesday = max(filter(lambda x : x.weekday() == 2, dates))
        self.end_date = last_wednesday
        return self

    def set_end_date(self):
        # set to last full day of data
        self.end_date = self.today - timedelta(1)
        return self

    def set_dates_to_current_month(self):
        self.set_end_date()
        self.set_start_date()
        return self

    def set_start_date(self):
        # default to first of month
        self.start_date = self.end_date.replace(day=1)
        return self

    def set_start_date_to_one_week_prior(self):
        self.start_date = self.end_date-timedelta(6)
        return self

    def set(self, slack_weekly=False):
        # TODO: Is there a better way to handle this?
        if slack_weekly:
            self.set_end_date_to_last_wednesday()
            self.set_start_date_to_one_week_prior()
        else:
            self.set_dates_to_current_month()
        return self

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date


if __name__ == '__main__':
    main()
