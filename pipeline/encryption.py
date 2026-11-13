from pathlib import Path

from cryptography.fernet import Fernet

KEY_FILE = "keys/secret.key"


def generate_key():
    """
    Generate and save a new encryption key.
    """

    key = Fernet.generate_key()

    Path(KEY_FILE).parent.mkdir(parents=True, exist_ok=True)

    with open(KEY_FILE, "wb") as file:
        file.write(key)

    print("Encryption key generated successfully.")

def load_key():
    """
    Load the encryption key from disk.
    """

    if not Path(KEY_FILE).exists():
        raise FileNotFoundError(
            f"No encryption key at {KEY_FILE}. Run: python -c \"import sys; sys.path.insert(0, 'pipeline'); "
            f"from encryption import generate_key; generate_key()\""
        )

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

