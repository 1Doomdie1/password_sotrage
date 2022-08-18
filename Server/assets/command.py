#!/usr/bin/python3

import pickle
from .file import File
from .encrypt import Encrypt

class Command():
    def __init__(self, cmd, path):
        self.cmd = pickle.loads(cmd)
        self.head = self.cmd[0]
        self.path = path
        self.flags = self.cmd[1:]
        self.response = ''

    def add_new_email_entry(self):
        db = File(f"DBS/{self.path}/db.json", "r+")
        db.output_format("json")
        service = self.flags[0]
        email = self.flags[1]
        password = Encrypt(self.flags[2]).encode_paswd()
        db.save({"service":service, "email":email, "password":password})
        self.response = pickle.dumps(["EMAIL_ENTRY" ,f"[+] Email '{self.flags[1]}' has been added!"])

    def close_sv(self):
        self.response = pickle.dumps(["SV_SHUTDOWN" ,f"[-] Server shutdown."])

    def sort_entries(self):
        db = File(f"DBS/{self.path}/db.json", "r")
        db.output_format("json")
        data = db.data
        db.close()
        entries = []
        for entry in data:
            try:
                if entry[self.head] == self.flags[0]:
                    paswd = Encrypt(entry["password"]).decode_paswd()
                    entry["password"] = paswd
                    entries.append(entry)
            except KeyError:
                pass
        if not entries:
            cmd_code = "UNKNOWN_CMD"
            entries = f"[-] Unknown {self.head} <'{self.flags[0]}'>"
            print(f"{' '*5}└--->{entries}")
        else:
            cmd_code = f"{self.head.upper()}_ENTRIES"
        self.response = pickle.dumps([cmd_code ,entries])

    def dump_all(self):
        db = File(f"DBS/{self.path}/db.json", "r")
        db.output_format("json")
        data = db.data
        entries = [entry[self.head[:-1]] for entry in data]
        db.close()
        if self.head == "services":
            cmd_code = "ALL_SERVICES"
            entries = list(set(entries))
        else:
            cmd_code = "ALL_EMAILS"
        self.response = pickle.dumps([cmd_code, list(set(entries))])

    def del_email(self):
        db = File(f"DBS/{self.path}/db.json", "r")
        db.output_format("json")
        data = db.data
        db.close()
        email_service = self.flags[0]
        email_to_delete = self.flags[1]
        entry_to_delete = None
        for index in range(len(data)):
            if data[index]["service"] == email_service and data[index]["email"] == email_to_delete:
                entry_to_delete = index
                break
        if entry_to_delete:
            data.pop(entry_to_delete)
            db = File(f"DBS/{self.path}/db.json", "w")
            db.write(data)
            self.response = pickle.dumps(["EMAIL_DELETE", f"[+] Email {self.flags[1]} have been deleted."])
        elif not entry_to_delete:
            self.response = pickle.dumps(["EMAIL_DELETE_ERROR", f"[-] Email {self.flags[1]} not found.."])

    def ch_pas(self):
        db = File(f"DBS/{self.path}/db.json", "r")
        db.output_format("json")
        data = db.data
        db.close()

        service = self.flags[0]
        email = self.flags[1]
        old_pass = Encrypt(self.flags[2]).encode_paswd()
        new_pass = Encrypt(self.flags[3]).encode_paswd()
        password_changed = False

        for entry in data:
            if entry["service"] == service and entry["email"] == email and entry["password"] == old_pass:
                entry["password"] = new_pass
                password_changed = True
                break

        if password_changed:
            db = File(f"DBS/{self.path}/db.json", "w")
            db.write(data)
            self.response = pickle.dumps(["PASWD_CHANGED", f"[+] Password has been changed."])
        elif not password_changed:
            self.response = pickle.dumps(["PASWD_CHANGED_FAILED", f"[-] Failed to change password. Old password or email may be wrong."])

    def ch_email(self):
        db  = File(f"DBS/{self.path}/db.json", "r")
        db.output_format("json")
        data = db.data
        db.close()

        service = self.flags[0]
        old_email = self.flags[1]
        new_email = self.flags[2]
        email_changed = False

        for entry in data:
            if entry["service"] == service and entry["email"] == old_email:
                entry["email"] = new_email
                email_changed = True
                break

        if email_changed:
            db = File(f"DBS/{self.path}/db.json", "w")
            db.write(data)
            self.response = pickle.dumps(["EMAIL_CHANGED", f"[+] Email {self.flags[1]} has been changed."])
        elif not email_changed:
            self.response = pickle.dumps(["EMAIL_CHANGED_FAILED", f"[-] Email {self.flags[1]} not found."])

    def __str__(self):
        return f"{self.cmd}"

