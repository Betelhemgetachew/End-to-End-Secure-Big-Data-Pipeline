from database import get_connection
import bcrypt
from getpass import getpass


def hash_password(password):
    """
    Hash a plaintext password using bcrypt.
    """
    password_bytes = password.encode("utf-8")

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(password, password_hash):
    """
    Verify a plaintext password against a stored bcrypt hash.
    """
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )

def create_user(username, password, role):
    """
    Create a new user with a hashed password.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Check if user already exists
    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE username = %s
        """,
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        print(f"User '{username}' already exists.")

        cursor.close()
        connection.close()
        return

    # Hash the password
    password_hash = hash_password(password)

    # Insert the new user
    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            password_hash,
            role
        )
        VALUES (%s, %s, %s)
        """,
        (
            username,
            password_hash,
            role
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print(f"User '{username}' created successfully.")

def login():
    """
    Authenticate a user.
    """

    username = input("Username: ")
    password = getpass("Password: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT password_hash, role
        FROM users
        WHERE username = %s
        """,
        (username,)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user is None:
        print("\nInvalid username or password.")
        return None

    stored_hash, role = user

    if verify_password(password, stored_hash):

        print("\nLogin successful.")
        print(f"Welcome {username}.")
        print(f"Role: {role}")

        return username, role

    print("\nInvalid username or password.")
    return None

if __name__ == "__main__":
    login()