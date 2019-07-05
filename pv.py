import sys
import assets.password as password
from assets.management import create_database, query_db
from sqlite3 import Error


# generate account
# account
# delete
# password

# todo: master password system
# todo: hide passwords entered on the command line
# todo: implement help system

if __name__ == "__main__":
    try:
        query_db("first")
    except Error:
        create_database()

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
