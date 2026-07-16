from cryptography.fernet import Fernet

KEY_FILE = "keys/secret.key"


def generate_key():
    """
    Generate and save a new encryption key.
    """

    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as file:
        file.write(key)

    print("Encryption key generated successfully.")

def load_key():
    """
    Load the encryption key from disk.
    """

    with open(KEY_FILE, "rb") as file:
        return file.read()

def encrypt_data(data):
    """
    Encrypt a value using Fernet.
    """

    key = load_key()

    cipher = Fernet(key)

    encrypted = cipher.encrypt(
        str(data).encode()
    )

    return encrypted.decode()

def decrypt_data(data):
    """
    Decrypt a value using Fernet.
    """

    key = load_key()

    cipher = Fernet(key)

    decrypted = cipher.decrypt(
        data.encode()
    )

    return decrypted.decode()

