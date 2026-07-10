from database import get_connection

try:
    connection = get_connection()

    print("Connected successfully!")

    connection.close()

except Exception as e:
    print(e)