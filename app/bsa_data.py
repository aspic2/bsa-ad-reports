from app.line_item import LineItem

class BsaData(object):

    def __init__(self, json):
        self.line_items = []
        self.line_item_names = None
        self.data = json
        self.formatted_data = []


    def add_line_item_names(self):
        # sorting makes things easier to read in the spreadsheet
        self.line_item_names = sorted(set(x.get("lineitem_name") for x in self.data))
        return self

    def add_line_items(self):
        for li in self.line_item_names:
            relevant_stats = list(x for x in self.data if x.get("lineitem_name") == li)
            self.line_items.append(LineItem(relevant_stats).build())
        return self

    def format_data(self):
        self.formatted_data = list([li.get_name(), li.get_impressions(), li.get_clicks()] for li in self.line_items)
        return self

    def add_header_to_formatted_data(self):
        self.formatted_data[0] = ["name", "impressions", "clicks"]
        return self

    def format_and_return_data(self):
        self.add_line_item_names()
        self.add_line_items()
        self.format_data()
        self.add_header_to_formatted_data()
        return self.formatted_data

if __name__ == '__main__':
    main()
