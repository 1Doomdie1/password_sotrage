#!/usr/bin/python3

import base64

class Encrypt():
    def __init__(self, passwd):
        self.key = '<ENTER YOUR KEY>' # This can be anything that you'd like.
        self.password = passwd

    def encode_paswd(self):
        bytes_paswd = f"{self.password}{self.key}".encode("ascii")
        return base64.b64encode(bytes_paswd).decode("ascii")

    def decode_paswd(self):
        base64_paswd_bytes = self.password.encode("ascii")
        return base64.b64decode(base64_paswd_bytes).decode("ascii").replace(self.key, "")
