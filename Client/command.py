import sys
import pickle
from prettytable import PrettyTable


class Command():
    def __init__(self, cmd=None):
        self.cmd = cmd

    def pickle_cmd(self):
        return pickle.dumps(self.cmd)

    def unpickle_cmd(self):
        unpickled_cmd = pickle.loads(self.cmd)
        reply_code = unpickled_cmd[0]
        response = unpickled_cmd[1]
        return reply_code, response

    def prettify_response(self):
        reply_code = self.cmd[0]
        response = self.cmd[1]

        if reply_code == "SERVICE_ENTRIES" or reply_code == "EMAIL_ENTRIES":
            table = PrettyTable()
            table.field_names = ["Email", "Service", "Password"]
            for entry in response:
                table.add_row([entry["email"], entry["service"], entry["password"]])
            return table
        else:
            return response

    def help_menu(self):
        table = PrettyTable()
        table.field_names = ["Command", "Description"]
        cmds_descrition = [
            ["help", "help menu"],
            ["email", "returns a list of all emails + passwords based on email"],
            ["emails", "returns a list of all know emails"],
            ["ch_pas", "changes email password by providing service email oldPass newPass"],
            ["service", "returns a list of all emails + passwords based on service"],
            ["ch_email", "change an email address by providing service oldEmail newEmail"],
            ["services", "returns a list of all know services"],
            ["add_email", "adds a email to db by providing the service email password"],
            ["del_email", "delete an email by providing service and email"],
        ]
        for cmd_descrition in cmds_descrition:
            table.add_row(cmd_descrition)
        print(table)
        sys.exit()
