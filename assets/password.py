import pyperclip
from getpass import getpass
from .management import (
    save_password,
    query_db,
    update_password,
    delete_account,
    get_all_accounts,
    delete_all_accounts
)
from .generate import generate_password


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


def generate(command):
    if len(command) > 1:
        account = command[1]
        password = generate_password()
        if not query_db(account):
            save_password(account, password)
            pyperclip.copy(password)
            confirmation_message(account, "g")
        else:
            if confirmation(account, "r"):
                update_password(account, password)
                pyperclip.copy(password)
                confirmation_message(account, "r")
    else:
        pyperclip.copy(generate_password())
        print("Random password copied to clipboard!")


def get(command):
    if len(command) > 1:
        account = command[1]
        password = query_db(account)[2]
        pyperclip.copy(password)
        print(f"Password copied to clipboard for '{account}'!")

    elif len(command) == 1:
        print("Accounts with passwords saved are:\n" +
              "\n".join(get_all_accounts()))


def delete(command):
    if len(command) > 1:
        account = command[1]
        if confirmation(account, "d"):
            delete_account(account)
            print(f"'{account}' deleted.")

    elif len(command) == 1:
        if confirmation(account, "da"):
            delete_all_accounts()
            print("All accounts deleted.")


def save(command):
    account = command[1]
    password = getpass(f"Enter password for '{account}': ")
    if not query_db(account):
        save_password(account, password)
        pyperclip.copy(password)
        print(f"Password saved for '{account}'!")
    else:
        if confirmation(account, "u"):
            update_password(account, password)
            pyperclip.copy(password)
            print(f"Password updated for '{account}'!")


def set_master_password():
    password = False
    again = True
    while again != password:
        password = getpass("Enter new master password: ")
        again = getpass("Enter new master password again: ")
    update_password("master", password)
    print("Master password set.")
