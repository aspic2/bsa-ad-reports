import base64

class Reader(object):

    def __init__(self, content):
        self.clean_data = None
        self.content = content


    def decode_content(self):
        # this is a bytes-like object and needs to be a string
        self.content = base64.urlsafe_b64decode(self.content.encode('ASCII'))
        self.clean_data = str(self.content, 'utf-8')
        return self

    def return_content_as_list(self):
        # is there a more robust way to handle new lines?
        lines = self.clean_data.split('\r\n')
        return lines

    def get_download_link(self):
        self.decode_content()
        content_list = self.return_content_as_list()
        return [line for line in content_list if "https://download.flashtalking.com" in line][0]
