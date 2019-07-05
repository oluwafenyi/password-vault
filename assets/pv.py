#!/usr/bin/env python
import sys
import pv_password as password
from pv_management import create_database, query_db
from sqlite3 import Error
from getpass import getpass


def auth():
    p = getpass("Enter master password: ")
    if p == query_db("master")[2]:
        return True
    else:
        print("Invalid password")

# generate account
# account
# delete
# password

# todo: implement help system


if __name__ == "__main__":
    try:
        query_db("master")
    except Error:
        create_database()
        password.set_master_password()

    if auth():
        command = sys.argv[1:]
        if not command:
            raise Exception("pv.py help for available commands")

        switcher = {
            "generate": password.generate,
            "account": password.get,
            "accounts": password.get,
            "delete": password.delete,
            "save": password.save
        }

        event = switcher.get(command[0], "error")

        if not isinstance(event, str):
            event(command)
        else:
            raise Exception("Invalid argument")
