#!/usr/bin/python3
from sys import argv
from command import Command
from connection import Connection


def main():
    cmd = argv[1:]

    if cmd[0] == "help":
        Command().help_menu()

    session = Connection("<IP>", "INT PORT")
    session.connect()

    session.send_data(cmd)
    response = Command(session.recv_data())
    session.close_con()
    print(response.prettify_response())


if __name__ == '__main__':
    main()
