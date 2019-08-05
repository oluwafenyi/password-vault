import string
import random


def generate_password():
    buffer = list(string.ascii_letters + string.digits + string.punctuation)
    length = random.randint(12, 20)
    password = "".join(random.sample(buffer, length))
    return password
