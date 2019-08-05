import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def gen_key(master):
    password = master.encode()
    salt = master.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt_password(password, master):
    f = Fernet(gen_key(master))
    return f.encrypt(password.encode())


def decrypt_password(password, master):
    f = Fernet(gen_key(master))
    return f.decrypt(password).decode()
