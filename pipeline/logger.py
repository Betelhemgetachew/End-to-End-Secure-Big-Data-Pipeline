from database import get_connection


def log_event(username, action, status, ip_address="127.0.0.1"):
    """
    Save an audit log entry.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO audit_logs
        (
            username,
            action,
            status,
            ip_address
        )
        VALUES
        (%s, %s, %s, %s)
        """,
        (
            username,
            action,
            status,
            ip_address,
        ),
    )

    connection.commit()

    cursor.close()
    connection.close()