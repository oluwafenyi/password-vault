import pyperclip
from getpass import getpass

from .generator import generate_password
from .crypto import decrypt_password


def confirmation(account, action):
    if action == "r":
        response = input("Are you sure you want to regenerate password for"
                         " '{}' (y/n): ".format(account))
    elif action == "d":
        response = input("Are you sure you want to delete password for"
                         " '{}' (y/n): ".format(account))
    elif action == "u":
        response = input("Are you sure you want to update password for"
                         " '{}' (y/n): ".format(account))
    elif action == "da":
        response = input("Are you sure you want to delete all saved passwords "
                         "(y/n): ")
    return response.lower() == "y"


def confirmation_message(account, action):
    if action == "g":
        print("Password generated for account: '{}'".format(account) +
              "\nCopied to clipboard!")

    if action == "r":
        print("Password regenerated for account: '{}''".format(account) +
              "\nCopied to clipboard!")


def generate(command, db, auth):
    if len(command) > 1:
        account = command[1]
        password = generate_password()
        if not db.query(account):
            db.save_password(account, password, auth)
            pyperclip.copy(password)
            confirmation_message(account, "g")
        else:
            if confirmation(account, "r"):
                db.update_password(account, password, auth)
                pyperclip.copy(password)
                confirmation_message(account, "r")
    else:
        pyperclip.copy(generate_password())
        print("Random password copied to clipboard!")


def get(command, db, auth):
    if len(command) > 1:
        account = command[1]
        password = db.query(account)[2]
        password = decrypt_password(password, auth)
        pyperclip.copy(password)
        print("Password copied to clipboard for '{}'!".format(account))

    elif len(command) == 1:
        accounts = db.get_all_accounts()
        if len(accounts) > 0:
            print("Accounts with passwords saved are:\n" +
                  "\n".join(accounts))
        else:
            print("No accounts saved.")


def delete(command, db, auth):
    if len(command) > 1:
        account = command[1]
        if confirmation(account, "d"):
            db.delete_account(account)
            print("'{}' deleted.".format(account))

    elif len(command) == 1:
        if confirmation("all", "da"):
            db.delete_all_accounts()
            print("All accounts deleted.")


def save(command, db, auth):
    if len(command) > 1:
        account = command[1]
        password = getpass("Enter password for '{}': ".format(account))
        if not db.query(account):
            db.save_password(account, password, auth)
            pyperclip.copy(password)
            print("Password saved for '{}'!".format(account))
        else:
            if confirmation(account, "u"):
                db.update_password(account, password, auth)
                pyperclip.copy(password)
                print("Password updated for '{}'!".format(account))
    else:
        print("Account name required.")


def help_me(command, db):
    messages = [
        "usage: pv [command]",
        "A python CLI based password manager",
        "generate  generates a random password to your clipboard",
        "          [accountname] sets a unique identifier for your password and save; overwrites if exists",
        "accounts  shows all saved passwords",
        "account   [accountname] shows the password of a particular user only",
        "save      [accountname] awaits password input and binds to accountname",
        "delete    delete all passwords in the database",
        "          [accountname] delete only this user in the database"
    ]
    for message in messages: print(message)
