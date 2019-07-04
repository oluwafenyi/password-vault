import pyperclip
from management import (
    save_password,
    query_db,
    update_password,
    delete_account,
    get_all_accounts,
    delete_all_accounts
)
from generate import generate_password


def generate(command):
    if len(command) > 1:
        account = command[1]
        password = generate_password()
        if not query_db(account):
            save_password(account, password)
            pyperclip.copy(password)
            print(f"Password generated for new account: {account}"
                  "\nCopied to clipboard!")
        else:
            update_password(account, password)
            print(f"Password regenerated for account: {account}"
                  "\nCopied to clipboard!")
    else:
        pyperclip.copy(generate_password())
        print("Random password copied to clipboard!")


def get(command):
    if len(command) > 1:
        account = command[1]
        password = query_db(account)[2]
        pyperclip.copy(password)
        print(f"Password copied to clipboard for account: {account}")

    elif len(command) == 1:
        print("Accounts with passwords saved are:" +
              "\n".join(get_all_accounts()))


def delete(command):
    if len(command) > 1:
        account = command[1]
        response = input(f"Are you sure you want to delete {account} (y/n): ")
        if response.lower() == "y":
            delete_account(account)
            print(f"{account} deleted.")

    elif len(command) == 1:
        response = input("Are you sure you want to delete all saved passwords"
                         "(y/n): ")
        if response.lower() == "y":
            delete_all_accounts()
