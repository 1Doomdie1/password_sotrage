#!/usr/bin/python3
import socket
import pickle
from sys import argv
from assets import *

HOST = str(argv[1])
PORT = int(argv[2])       # If there is one then more user using this system you will have to run the script on different ports
ADDRESS = (HOST, PORT)
BUFFER = 1024
PATH_TO_DB = str(argv[3]) # Refers to the json file path where the passwords will be saved.

session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
session.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
session.bind(ADDRESS)
session.listen()

print(f"[+] Server started on port {PORT}.")

try:
    run = True
    while run:
        con, address = session.accept()
        cmd = Command(con.recv(BUFFER), PATH_TO_DB)
        if not cmd:
            break

        if cmd.head == "stop":
            run = False
            print(f"[-] CMD RECEIVED: {cmd.head}. <<SERVER STOPPING>>")
            cmd.close_sv()
            response = cmd.response
            con.sendall(response)
            con.close()
        elif cmd.head == "add_email":
            if len(cmd.flags) == 3:
                print(f"[+] CMD RECEIVED: {cmd.head} { {cmd.flags[1]} } for [SERVICE] <{cmd.flags[0]}>")
                cmd.add_new_email_entry()
                response = cmd.response
                con.sendall(response)
            else:
                response = pickle.dumps(["MISSING_ARGS",f"[-] One or more args are missing for [CMD] <'{cmd.head}'>."])
            con.sendall(response)
        elif cmd.head == "service":
            if len(cmd.flags) == 1:
                print(f"[+] CMD RECEIVED: {cmd.head} for [SERVICE] <{cmd.flags[0]}>")
                cmd.sort_entries()
                response = cmd.response
            elif len(cmd.flags) > 1:
                response = pickle.dumps(["TO_MANY_ARGS",f"[-] To many args passed for [CMD] <'{cmd.head}'>."])
            elif len(cmd.flags) < 1:
                response = pickle.dumps(["MISSING_ARGS",f"[-] One or more args are missing for [CMD] <'{cmd.head}'>."])
            con.sendall(response)
        elif cmd.head == "email":
            if len(cmd.flags) == 1:
                print(f"[+] CMD RECEIVED: {cmd.head} <{cmd.flags[0]}>")
                cmd.sort_entries()
                response = cmd.response
            elif len(cmd.flags) > 1:
                response = pickle.dumps(["TO_MANY_ARGS",f"[-] To many args passed for [CMD] <'{cmd.head}'>."])
            elif len(cmd.flags) < 1:
                response = pickle.dumps(["MISSING_ARGS",f"[-] One or more args are missing for [CMD] <'{cmd.head}'>."])
            con.sendall(response)
        elif cmd.head == "services" or cmd.head == "emails":
            if len(cmd.flags) == 0:
                print(f"[+] CMD RECEIVED: {cmd.head} <<SENDING ALL {cmd.head}>>")
                cmd.dump_all()
                response = cmd.response
            else:
                response = pickle.dumps(["TO_MANY_ARGS",f"[-] To many args passed for [CMD] <'{cmd.head}'>."])
            con.sendall(response)
        elif cmd.head == "del_email":
            if len(cmd.flags) == 2:
                print(f"[+] CMD RECEIVED: {cmd.head} <{cmd.flags[1]}>")
                cmd.del_email()
                response = cmd.response
            elif len(cmd.flags) < 2:
                response = pickle.dumps(["MISSING_ARGS",f"[-] One or more args are missing for [CMD] <'{cmd.head}'>."])
            elif len(cmd.flags) > 2:
                response = pickle.dumps(["TO_MANY_ARGS",f"[-] To many args passed for [CMD] <'{cmd.head}'>."])
            con.sendall(response)
        elif cmd.head == "ch_pas":
            if len(cmd.flags) == 4:
                print(f"[+] CMD RECEIVED: {cmd.head} for <'{cmd.flags[1]}'>")
                cmd.ch_pas()
                response = cmd.response
            elif len(cmd.flags) < 4:
                response = pickle.dumps(["MISSING_ARGS",f"[-] One or more args are missing for [CMD] <'{cmd.head}'>."])
            elif len(cmd.flags) > 4:
                response = pickle.dumps(["TO_MANY_ARGS",f"[-] To many args passed for [CMD] <'{cmd.head}'>."])
            con.sendall(response)
        elif cmd.head == "ch_email":
            if len(cmd.flags) == 3:
               print(f"[+] CMD RECEIVED: {cmd.head} for <'{cmd.flags[1]}'>")
               cmd.ch_email()
               response = cmd.response
            elif len(cmd.flags) < 3:
               response = pickle.dumps(["MISSING_ARGS",f"[-] One or more args are missing for [CMD] <'{cmd.head}'>."])
            elif len(cmd.flags) > 3:
               response = pickle.dumps(["TO_MANY_ARGS",f"[-] To many args passed for [CMD] <'{cmd.head}'>."])
            con.sendall(response)
        else:
            response=pickle.dumps(["UNKNOWN_CMD",f"[-] Unknown command <'{cmd.head}'>."])
            con.sendall(response)
except (KeyboardInterrupt, NameError) as e:
    print(e)
    con.close()

