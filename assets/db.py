import sqlite3
import os

from pyAesCrypt import encryptFile, decryptFile

from config import __dbPath__, __dbName__
from crypto import encrypt_password


class EncryptionError(PermissionError):
    pass


class PVaultDB:
    def __init__(self):
        self.name = __dbName__
        self.directory = os.path.dirname(__dbPath__)

    def exists(self):
        return __dbName__ in os.listdir(self.directory) \
            or __dbName__+'.enc' in os.listdir(self.directory)

    def is_decrypted(self):
        if self.exists():
            return __dbName__ in os.listdir(self.directory)

    def encrypt(self, master):
        encryptFile(__dbPath__, __dbPath__ + '.enc', master, 64*1024)
        os.remove(__dbPath__)

    def decrypt(self, master):
        decryptFile(__dbPath__ + '.enc', __dbPath__, master, 64*1024)
        os.remove(__dbPath__ + '.enc')

    def create_database(self):
        """create database upon initialization"""
        with sqlite3.connect(__dbPath__) as conn:
            c = conn.cursor()
            cmd = """CREATE TABLE IF NOT EXISTS passwords (
                        id integer PRIMARY KEY,
                        account text NOT NULL,
                        password text NOT NULL
                    );
                """
            c.execute(cmd)

    def query(self, account):
        if not self.is_decrypted():
            raise EncryptionError('DB is encrypted')
        with sqlite3.connect(__dbPath__) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM passwords WHERE account=?", (account,))
            return c.fetchone()

    def get_all_accounts(self):
        if not self.is_decrypted():
            raise EncryptionError('DB is encrypted')
        with sqlite3.connect(__dbPath__) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM passwords")
            return [item[1] for item in c.fetchall()]

    def save_password(self, account, password, auth):
        password = encrypt_password(password, auth)
        if not self.is_decrypted():
            raise EncryptionError('DB is encrypted')
        """save generated password to account in db"""
        with sqlite3.connect(__dbPath__) as conn:
            c = conn.cursor()
            cmd = """INSERT INTO passwords(account, password)
                    VALUES (?, ?)"""
            c.execute(cmd, (account, password))
        return c.lastrowid

    def update_password(self, account, new_password, auth):
        new_password = encrypt_password(new_password, auth)
        if not self.is_decrypted():
            raise EncryptionError('DB is encrypted')
        """updates an account with a new password"""
        with sqlite3.connect(__dbPath__) as conn:
            c = conn.cursor()
            _id = self.query(account)[0]
            cmd = """UPDATE passwords
                    SET password = ?
                    WHERE id = ?"""
            c.execute(cmd, (new_password, _id))

    def delete_account(self, account):
        if not self.is_decrypted():
            raise EncryptionError('DB is encrypted')
        """deletes entries for an account"""
        with sqlite3.connect(__dbPath__) as conn:
            c = conn.cursor()
            _id = self.query(account)[0]
            cmd = "DELETE FROM passwords WHERE id = ?"
            if account == "all":
                cmd = "DELETE FROM passwords"
                c.execute(cmd)
                return
            c.execute(cmd, (_id,))

    def delete_all_accounts(self):
        if not self.is_decrypted():
            raise EncryptionError('DB is encrypted')
        with sqlite3.connect(__dbPath__) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM passwords")
            self.create_database()
