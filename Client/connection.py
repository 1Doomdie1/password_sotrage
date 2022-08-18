import pickle
import socket
from command import Command


class Connection():
    def __init__(self, host, port, buffer=1024):
        self.host = host
        self.port = port
        self.buffer = buffer

    def connect(self):
        ADDRESS = (self.host, self.port)
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.connect(ADDRESS)

    def send_data(self, data):
        msg = Command(data).pickle_cmd()
        self.session.sendall(msg)

    def recv_data(self):
        response = Command(self.session.recv(self.buffer)).unpickle_cmd()
        return response

    def close_con(self):
        self.session.close()


'''
SV reply codes

'SERVICE_ENTRIES'
'EMAIL_ENTRIES'
'ALL_SERVICES'
'ALL_EMAILS'
'SV_SHUTDOWN':
'UNKNOWN_CMD':
'MISSING_ARGS':
'TO_MANY_ARGS':

'''
