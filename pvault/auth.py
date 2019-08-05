from getpass import getpass

from .db import PVaultDB


def auth(db: PVaultDB):
    if not db.exists():
        db.create_database()

        master = getpass("Set master password: ")
        master_conf = getpass("Confirm master password: ")

        while master != master_conf and master != "":
            print("Passwords don't match.")
            master = getpass("Set master password: ")
            master_conf = getpass("Confirm master password: ")

        db.encrypt(master_conf)
        db.decrypt(master_conf)
        return master

    else:
        master = getpass("Enter master password: ")
        db.decrypt(master)
        return master
