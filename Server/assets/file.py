#!/usr/bin/python3
import json

class File():
    def __init__(self, path, mode):
        self.file = open(path, mode)

    def output_format(self, format):
        if format == "json":
            self.data = json.load(self.file)

    def save(self, data):
        self.data.append(data)
        self.file.seek(0)
        json.dump(self.data, self.file, indent=2)
        self.close()

    def write(self, data):
        json.dump(data, self.file, indent=2)
        self.close()

    def close(self):
        self.file.close()
