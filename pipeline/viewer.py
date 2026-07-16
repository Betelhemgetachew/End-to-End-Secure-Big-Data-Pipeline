from authorization import has_permission
from database import get_connection
from logger import log_event


def view_logs(username, role):
    """
    Display the most recent audit logs.
    """

    if not has_permission(role, "view_logs"):

        log_event(
            username=username,
            action="Permission Denied: View Audit Logs",
            status="FAILED"
        )

        print("\nYou are not authorized to view audit logs.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            log_id,
            username,
            action,
            status,
            log_time
        FROM audit_logs
        ORDER BY log_time DESC
        LIMIT 20;
        """
    )

    logs = cursor.fetchall()

    cursor.close()
    connection.close()

    print("\n" + "=" * 95)
    print("LATEST AUDIT LOGS")
    print("=" * 95)

    print(
        f"{'ID':<5}"
        f"{'USERNAME':<15}"
        f"{'ACTION':<35}"
        f"{'STATUS':<10}"
        f"{'TIME'}"
    )

    print("-" * 95)

    for log in logs:

        print(
            f"{log[0]:<5}"
            f"{log[1]:<15}"
            f"{log[2]:<35}"
            f"{log[3]:<10}"
            f"{log[4]}"
        )

    print("=" * 95)
    print("Audit logs displayed successfully.")

    log_event(
        username=username,
        action="Viewed Audit Logs",
        status="SUCCESS"
    )