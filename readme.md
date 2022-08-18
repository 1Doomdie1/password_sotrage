## Disclaimer
* This is by no means a secure code or a well written code. If you use this code and you get a data breach I will not be responsible for any stolen/damaged data. Use it at your own risk.

## Password Storage Demo
* This project shows how you could use a VPS to store your passwords and then retrive them when needed.
* This is a command line application.

## Requirements
```bash
pip install prettytable
```

## Setup

### Server
* This script can be run on a local network as well. The down side of this will be the fact that you will need to create a process that runs in the background that keeps the script running. This can be overcome if you have a Raspberry PI or any local server that you keep it on.
* Before you run the script go into Server/DBS/ and create a new folder with either your name or any name you want
```bash
cd Server/DBS/
mkdir john
```
* After that you will need to create a json file inside your new directory. The name of the json file should always be db.json
```bash
cd john
touch db.json
echo '[]' > db.json
```
* To start the application you will need to run the start_sv.py file and pass an IP address, a port and the name of the folder you just created. In this case the IP will be localhost as we are running the script localy.
```bash
cd ../../
python3 start_sv.py localhost 9001 john
[+] Server started on port 9001.
```
* This will start a connection on port 9001 and all the new emails will be saved in /DBS/john/db.json
* If you choose to put this on a remote server, like a VPS, provide the IP address you use to connect via ssh into the command.
```bash
python3 start_sv.py 213.213.213.213 9001 john
[+] Server started on port 9001.
```
* Any new events will be logged here.

### Client
* To add data to your DB you will need to run the db.py file which is located under Client/db.py. But before this you will need to change the IP and port on line 13
```python
session = Connection("localhost", 9001)
```
* After you modified this you can run the this command
```bash
python3 db.py help

+-----------+-------------------------------------------------------------------+
|  Command  |                            Description                            |
+-----------+-------------------------------------------------------------------+
|    help   |                             help menu                             |
|   email   |      returns a list of all emails + passwords based on email      |
|   emails  |                 returns a list of all know emails                 |
|   ch_pas  | changes email password by providing service email oldPass newPass |
|  service  |     returns a list of all emails + passwords based on service     |
|  ch_email |   change an email address by providing service oldEmail newEmail  |
|  services |                returns a list of all know services                |
| add_email |     adds a email to db by providing the service email password    |
| del_email |           delete an email by providing service and email          |
+-----------+-------------------------------------------------------------------+
```
* To add different email and passwords to this DB you have to use the add_email flag and pass a service email and password
```bash
python3 db.py add_email yahoo john.doe@yahoo.com 1234
[+] Email 'john.doe@yahoo.com' has been added!
```
* To get a password for an email you can do this in 2 ways. Either by sorting the emails by service or searching by the email directly. For example.
```bash
python3 db.py services
['yahoo']
```
* This will return a list of all services saved in your DB. With this you can get all the emails that are saved under this service like so.
```bash
python3 db.py service yahoo
+--------------------+---------+------------+
|        Email       | Service |  Password  |
+--------------------+---------+------------+
| john.doe@yahoo.com |  yahoo  |    1234    |
+--------------------+---------+------------+
```
* You can search by email directly like this.
```bash
python3 db.py emails
['john.doe@yahoo.com']
```
* This will return a list of all know email in the DB.
* To get an email password knowing the email only you can use this command.
```bash
python3 db.py email john.doe@yahoo.com
+--------------------+---------+------------+
|        Email       | Service |  Password  |
+--------------------+---------+------------+
| john.doe@yahoo.com |  yahoo  |    1234    |
+--------------------+---------+------------+
```
* This command will return a list of all know emails saved in the db even if they have other services.
* If the DB is situated on a VPS or other network please modify the session line from the first point under the Client section of this readme.md
```python
session = Connection("213.213.213.213", 9001)
```