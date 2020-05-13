import base64
from os import getcwd
from zipfile import ZipFile

class Reader(object):

    def __init__(self, content):
        self.clean_data = None
        self.content = content


    def decode_content(self):
        # this is a bytes-like object and needs to be a string
        self.content = base64.urlsafe_b64decode(self.content.encode('ASCII'))
        self.clean_data = str(self.content, 'utf-8')
        return self

    def return_content_as_list(self, split_by='\n'):
        # is there a more robust way to handle new lines?
        lines = self.clean_data.split(split_by)
        return lines

    def get_download_link(self):
        self.decode_content()
        content_list = self.return_content_as_list('\r\n')
        return [line for line in content_list if "https://download.flashtalking.com" in line][0]

    def return_content_as_stripped_string(self, stripped_character='"'):
        self.content = str(self.content, 'utf-8').replace(stripped_character, '')
        return self.content


class FileManager(object):

    def __init__(self, filename=None, write_mode='w'):
        self.file = file
        self.filename = filename
        self.filepath = getcwd() + '/resources/' + self.filename
        self.write_mode = write_mode

    def write_content(self, content):
        # make sure write mode is 'wb+' for zip files
        with open(self.filepath, self.write_mode) as f:
            f.write(content)
        return self



class ZipFileManager(FileManager):

    def __init__(self):
        FileManager.__init__(self, filename=None, write_mode='wb+')

    def read_first_file(self):
        first_file = None
        with ZipFile(self.filepath) as zip:
            file_name = zip.namelist()[0]
            first_file = Reader(zip.read(file_name))
        return first_file
