import MaxPlus

class OpenFile(object):
    def __init__(self, file_path):
        self.file_path = file_path
        fm = MaxPlus.FileManager
        fm.Open(file_path)