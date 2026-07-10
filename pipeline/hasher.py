

import hashlib
from pathlib import Path


def generate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def save_hash(hash_value, hash_file):

    Path(hash_file).parent.mkdir(parents=True, exist_ok=True)

    with open(hash_file, "w") as file:
        file.write(hash_value)


def load_hash(hash_file):

    with open(hash_file, "r") as file:
        return file.read().strip()


def verify_hash(file_path, hash_file):

    current_hash = generate_hash(file_path)
    stored_hash = load_hash(hash_file)

    return current_hash == stored_hash


