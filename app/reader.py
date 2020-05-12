import base64

class Reader(object):

    def __init__(self, content):
        self.clean_data = None
        self.content = content


    def decode_content(self):
        # this is a bytes-like object and needs to be a string
        self.content = base64.urlsafe_b64decode(self.content.encode('ASCII'))
        return self

    def return_content_as_list(self):
        lines = str(self.content, 'utf-8').split('\r\n')
        return lines

    def get_download_link(self, content_list):
        return [line for line in content_list if "https://download.flashtalking.com" in line][0]
