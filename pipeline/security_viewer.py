from authorization import has_permission
from database import get_connection
from logger import log_event


def view_security_events(username, role):
    """
    Display security-related events.
    """

    if not has_permission(role, "view_security_events"):

        log_event(
            username=username,
            action="Permission Denied: View Security Events",
            status="FAILED"
        )

        print("\nYou are not authorized to view security events.")
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
        WHERE
            action ILIKE '%Failed%'
            OR action ILIKE '%Permission Denied%'
            OR action ILIKE '%Integrity%'
            OR action ILIKE '%Encrypted%'
        ORDER BY log_time DESC
        LIMIT 20;
        """
    )

    events = cursor.fetchall()

    cursor.close()
    connection.close()

    print("\n" + "=" * 95)
    print("LATEST SECURITY EVENTS")
    print("=" * 95)

    print(
        f"{'ID':<5}"
        f"{'USERNAME':<15}"
        f"{'ACTION':<40}"
        f"{'STATUS':<10}"
        f"{'TIME'}"
    )

    print("-" * 95)

    for event in events:

        print(
            f"{event[0]:<5}"
            f"{event[1]:<15}"
            f"{event[2]:<40}"
            f"{event[3]:<10}"
            f"{event[4]}"
        )

    print("=" * 95)

    print("Security events displayed successfully.")

    log_event(
        username=username,
        action="Viewed Security Events",
        status="SUCCESS"
    )