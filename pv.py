import sys
import password
from management import create_database, query_db
from sqlite3 import Error


# generate account
# account
# delete
# password

if __name__ == "__main__":
    try:
        query_db("first")
    except Error:
        create_database()

    command = sys.argv[1:]

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
