import os

import pandas as pd
from psycopg2.extras import execute_values

from database import get_connection
from encryption import encrypt_data
from logger import log_event

def read_dataset(file_path):
    """
    Read the CSV dataset into a pandas DataFrame.
    """
    return pd.read_csv(file_path)


def batch_exists(connection, batch_id):
    """
    Check whether a batch has already been imported.
    """
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM uploads
        WHERE batch_id = %s;
        """,
        (batch_id,)
    )

    exists = cursor.fetchone()[0] > 0

    cursor.close()

    return exists


def insert_upload(
    connection,
    batch_id,
    filename,
    uploaded_by,
    file_hash,
):
    """
    Insert upload metadata and return the generated upload_id.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO uploads
        (
            batch_id,
            filename,
            uploaded_by,
            file_hash,
            upload_status
        )
        VALUES
        (%s, %s, %s, %s, %s)
        RETURNING upload_id;
        """,
        (
            batch_id,
            filename,
            uploaded_by,
            file_hash,
            "SUCCESS",
        ),
    )

    upload_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()

    return upload_id


def insert_customers(connection, dataframe, upload_id):
    """
    Bulk insert customer records.
    """

    cursor = connection.cursor()

    records = [
    (
        upload_id,
        encrypt_data(row.first_name),
        encrypt_data(row.last_name),
        encrypt_data(row.email),
        encrypt_data(row.phone),
        encrypt_data(row.national_id),
        row.city,
        row.account_number,
        row.account_type,
        row.account_balance,
    )
    for row in dataframe.itertuples(index=False)
]
    execute_values(
        cursor,
        """
        INSERT INTO customers
        (
            upload_id,
            first_name,
            last_name,
            email,
            phone,
            national_id,
            city,
            account_number,
            account_type,
            account_balance
        )
        VALUES %s;
        """,
        records,
    )

    connection.commit()

    cursor.close()


def import_dataset(
    file_path,
    batch_id,
    file_hash,
    uploaded_by="System",
):
    """
    Complete import workflow.
    """

    dataframe = read_dataset(file_path)

    connection = get_connection()

    try:

        if batch_exists(connection, batch_id):
            print(f"Batch '{batch_id}' has already been imported.")
            return

        upload_id = insert_upload(
            connection=connection,
            batch_id=batch_id,
            filename=os.path.basename(file_path),
            uploaded_by=uploaded_by,
            file_hash=file_hash,
        )

        log_event(
            username=uploaded_by,
            action="Sensitive Data Encrypted",
            status="SUCCESS"
        )

        insert_customers(
            connection=connection,
            dataframe=dataframe,
            upload_id=upload_id,
        )

        log_event(
            username=uploaded_by,
            action="Dataset Imported",
            status="SUCCESS"
)

        print(f"Successfully imported {len(dataframe)} customer records.")
        print(f"Upload ID : {upload_id}")
        print(f"Batch ID  : {batch_id}")
        return upload_id, batch_id

    except Exception as e:

        connection.rollback()

        log_event(
            username=uploaded_by,
            action="Dataset Imported",
            status="FAILED"
        )

        print(f"Import failed: {e}")

        raise
    finally:

        connection.close()