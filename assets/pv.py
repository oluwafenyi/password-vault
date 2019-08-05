#!/usr/bin/env python
import sys

import handler
from db import PVaultDB
from auth import auth


db = PVaultDB()


if __name__ == "__main__":

    try:
        if sys.argv[1] == "help":
            handler.help_me(sys.argv[1], db)
            sys.exit()

        elif sys.argv[1] == "generate" and len(sys.argv) == 2:
            handler.generate(sys.argv[1:], db)
            sys.exit()

        authenticated = None

        try:
            authenticated = auth(db)
        except ValueError:
            print("Wrong Password")  # or db is corrupt

        if authenticated:
            command = sys.argv[1:]
            if not command:
                print("Invalid Argument\n\n\n")
                handler.help_me(None, db)

            switcher = {
                "generate": handler.generate,
                "account": handler.get,
                "accounts": handler.get,
                "delete": handler.delete,
                "save": handler.save,
            }

            event = switcher.get(command[0], "error")

            if not isinstance(event, str):
                event(command, db, authenticated)
            else:
                print("Invalid Argument\n\n\n")
                handler.help_me(None, db)

        db.encrypt(authenticated)

    except:
        print("An error has occurred.")
        db.encrypt(authenticated)
