class Helper:

    def list_get(a_list, index, default=""):
        a = None
        try:
            a = a_list[index]
        except IndexError:
            a = default
        return a

    def build_advertiser_info_dict(a_list):
        d = {}
        d["name"] = Helper.list_get(a_list, 0)
        d["spreadsheet_id"] = Helper.list_get(a_list, 1)
        d["tab_name"] = Helper.list_get(a_list, 2)
        d["api_key"] = Helper.list_get(a_list, 3)
        d["third_party_tab_name"] = Helper.list_get(a_list, 4)
        d["email_subject"] = Helper.list_get(a_list, 5)
        d["email_attachment_name"] = Helper.list_get(a_list, 6)
        d["download_link"] = Helper.list_get(a_list, 7)
        return d

    def create_advertisers_info_list(data):
        advertisers_info_list = []
        for row in data:
            advertiser_dict = Helper.build_advertiser_info_dict(row)
            advertisers_info_list.append(advertiser_dict)
        return advertisers_info_list


if __name__ == '__main__':
    main()
