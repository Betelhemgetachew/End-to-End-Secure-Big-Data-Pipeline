from pathlib import Path

import pandas as pd

from authorization import has_permission
from database import get_connection
from logger import log_event

EXPORT_FOLDER = "exports"
EXPORT_THRESHOLD = 50000


def export_data(username, role):
    """
    Export customer records to a CSV file.
    Large exports are logged as security events.
    """

    # -------------------------------------
    # RBAC
    # -------------------------------------

    if not has_permission(role, "export"):

        log_event(
            username=username,
            action="Permission Denied: Export Data",
            status="FAILED"
        )

        print("\nYou are not authorized to export data.")
        return

    # -------------------------------------
    # Number of records
    # -------------------------------------

    try:
        rows = int(input("\nEnter number of records to export: "))

        if rows <= 0:
            print("Please enter a positive number.")
            return

    except ValueError:
        print("Invalid number.")
        return

    # -------------------------------------
    # Read from PostgreSQL
    # -------------------------------------

    connection = get_connection()

    query = """
        SELECT *
        FROM customers
        LIMIT %s;
    """

    df = pd.read_sql(query, connection, params=(rows,))

    connection.close()

    # -------------------------------------
    # Create export folder
    # -------------------------------------

    Path(EXPORT_FOLDER).mkdir(exist_ok=True)

    file_name = f"{EXPORT_FOLDER}/customers_export.csv"

    df.to_csv(
        file_name,
        index=False
    )

    # -------------------------------------
    # Log export
    # -------------------------------------

    log_event(
        username=username,
        action="Data Export",
        status="SUCCESS"
    )

    # -------------------------------------
    # Detect bulk export
    # -------------------------------------

    if len(df) >= EXPORT_THRESHOLD:

        log_event(
            username=username,
            action="Bulk Data Export Detected",
            status="WARNING"
        )

        print("\nWARNING: Large data export detected.")

    # -------------------------------------
    # Finish
    # -------------------------------------

    print("\nExport completed successfully.")
    print(f"Records exported: {len(df):,}")
    print(f"File saved to: {file_name}")