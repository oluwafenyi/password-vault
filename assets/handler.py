import pyperclip
from getpass import getpass

from generator import generate_password
from crypto import decrypt_password


def confirmation(account, action):
    if action == "r":
        response = input("Are you sure you want to regenerate password for"
                         f" '{account}' (y/n): ")
    elif action == "d":
        response = input("Are you sure you want to delete password for"
                         f" '{account}' (y/n): ")
    elif action == "u":
        response = input("Are you sure you want to update password for"
                         f" '{account}' (y/n): ")
    elif action == "da":
        response = input("Are you sure you want to delete all saved passwords "
                         "(y/n): ")
    return response.lower() == "y"


def confirmation_message(account, action):
    if action == "g":
        print(f"Password generated for account: '{account}'"
              "\nCopied to clipboard!")

    if action == "r":
        print(f"Password regenerated for account: '{account}''"
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
        print(f"Password copied to clipboard for '{account}'!")

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
            print(f"'{account}' deleted.")

    elif len(command) == 1:
        if confirmation("all", "da"):
            db.delete_all_accounts()
            print("All accounts deleted.")


def save(command, db, auth):
    if len(command) > 1:
        account = command[1]
        password = getpass(f"Enter password for '{account}': ")
        if not db.query(account):
            db.save_password(account, password, auth)
            pyperclip.copy(password)
            print(f"Password saved for '{account}'!")
        else:
            if confirmation(account, "u"):
                db.update_password(account, password, auth)
                pyperclip.copy(password)
                print(f"Password updated for '{account}'!")
    else:
        print("Account name required.")


def help_me(command, db):
    import os
    base = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    with open(os.path.join(base, 'README.md')) as readme:
        lines = readme.readlines()
        title = list(filter(lambda line: 'basic usage' in line.lower(), lines))
        title_index = lines.index(title[0])
        for line in lines[title_index::]:
            if not line.isspace():
                print(line)
