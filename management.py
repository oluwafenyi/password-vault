import sqlite3


conn = sqlite3.connect("./password.db")


def create_database():
    """create database upon initialization"""
    with conn:
        c = conn.cursor()
        cmd = """CREATE TABLE IF NOT EXISTS passwords (
                    id integer PRIMARY KEY,
                    account text NOT NULL,
                    password text NOT NULL
                );
            """
        c.execute(cmd)
        save_password("first", "hash")


def query_db(account):
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM passwords WHERE account=?", (account,))
        return c.fetchone()


def get_all_accounts():
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM passwords")
        return [item[1] for item in c.fetchall()][1:]


def save_password(account, password):
    """save generated password to account in db"""
    with conn:
        c = conn.cursor()
        cmd = """INSERT INTO passwords(account, password)
                VALUES (?, ?)"""
        c.execute(cmd, (account, password))
    return c.lastrowid


def update_password(account, new_password):
    """updates an account with a new password"""
    with conn:
        c = conn.cursor()
        _id = query_db(account)[0]
        cmd = """UPDATE passwords
                 SET password = ?
                 WHERE id = ?"""
        c.execute(cmd, (new_password, _id))


def delete_account(account):
    """deletes entries for an account"""
    with conn:
        c = conn.cursor()
        _id = query_db(account)[0]
        cmd = "DELETE FROM passwords WHERE id = ?"
        if account == "all":
            cmd = "DELETE FROM passwords"
            c.execute(cmd)
            return
        c.execute(cmd, (_id,))


def delete_all_accounts():
    with conn:
        c = conn.cursor()
        c.execute("DELETE FROM passwords")
