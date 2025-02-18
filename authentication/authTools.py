from hashlib import sha512
from database.db import Database
import os

def hash_password(password: str, salt: str = None) -> tuple:
    """
    Hashes a password using SHA-512.

    args:
        - password: A string of the password to hash.

    returns:
        - A tuple of the salt and the hashed password, both as strings.
    """
    encoded_password = password.encode()
    if salt is None:
        salt = os.urandom(16).hex()
    key = sha512(encoded_password + salt.encode()).hexdigest()
    return (salt, key)


def username_exists(username: str, data: Database) -> bool:
    """
    Checks if a username exists in the passwords.txt file.

    args:
        - username: A string of the username to check.

    returns:
        - True if the username exists, False if not.
    """

    return data.does_user_exist(username)


def update_passwords(username: str, key: str, salt: str, data: Database):
    """
    Updates the passwords.txt file with a new username and password combination.
    If the username is already in the file, the password will be updated.

    args:
        - username: A string of the username to store.
        - key: A string of the hashed password to store.
        - salt: A string of the salt to store.

    returns:
        - None

    modifies:
        - passwords.txt: Updates an existing or adds a new username and password combination to the file.
    """
    data.set_password_hash(username, key)
    data.set_password_salt(username, salt)


def check_password(password: str, salt: str, key: str) -> bool:
    """
    Checks if a password is correct by hashing it and comparing it to the given hash key.

    args:
        - password: A string of the password to check.
        - salt: A string of the salt to use.
        - key: A string of the hash to check against.

    returns:
        - True if the password is correct, False if not.
    """
    salt, new_key = hash_password(password, salt)
    key, new_key = key.strip(), new_key.strip()

    return key == new_key


def login_pipeline(username: str, password: str, data: Database) -> bool:
    """
    Checks if a username and password combination is correct.

    args:
        - username: A string of the username to check.
        - password: A string of the password to check.

    returns:
        - True if the username and password combination is correct, False if not.
    """
    if not username_exists(username, data):
        return False

    p_hash = data.get_password_hash_by_username(username)
    p_salt = data.get_salt_by_username(username)

    return check_password(password, p_salt, p_hash)


def main():
    password = input("enter password: ")
    salt, key = hash_password(password)
    print(f"Salt: {salt}")
    print(f"Key: {key}")


if __name__ == "__main__":
    main()
