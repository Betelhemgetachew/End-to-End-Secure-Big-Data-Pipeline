"""
gui_adapters.py

Thin bridge between the CustomTkinter GUI and the existing backend
(auth.py, authorization.py, validator.py, hasher.py, importer.py,
exporter.py, logger.py, database.py).

None of the original backend files are modified. The CLI-only bits
(auth.login() uses input()/getpass(), exporter.export_data() uses
input()) are re-implemented here calling the *same* underlying
functions (verify_password, has_permission, get_connection, etc.) so
the business logic and audit trail stay identical -- only the I/O
changes from stdin/stdout to function args/return values.
"""

import os
import uuid
import traceback

from database import get_connection
from auth import verify_password
from authorization import has_permission
from validator import validate_dataset
from hasher import generate_hash, save_hash
from importer import import_dataset
from logger import log_event

HASH_DIR = "hashes"


# ---------------------------------------------------------------------------
# Authentication (mirrors auth.login(), no input()/getpass())
# ---------------------------------------------------------------------------

def authenticate(username: str, password: str):
    """
    Returns (success: bool, role: str | None, message: str)
    """
    try:
        connection = get_connection()
    except Exception as e:
        return False, None, f"Could not connect to database:\n{e}"

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT password_hash, role
        FROM users
        WHERE username = %s
        """,
        (username,),
    )
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user is None:
        log_event(username=username, action="Failed Login", status="FAILED")
        return False, None, "Invalid username or password."

    stored_hash, role = user

    if verify_password(password, stored_hash):
        log_event(username=username, action="User Login", status="SUCCESS")
        return True, role, "Login successful."

    log_event(username=username, action="Failed Login", status="FAILED")
    return False, None, "Invalid username or password."


# ---------------------------------------------------------------------------
# Dataset validation (Phase 6) - GUI wraps validator.validate_dataset directly
# ---------------------------------------------------------------------------

def run_validate(username, role, file_path):
    """
    Returns dict: {success, dataframe_or_none, message}
    """
    if not has_permission(role, "validate"):
        log_event(username=username, action="Permission Denied: Validate Dataset", status="FAILED")
        return {"success": False, "df": None, "message": "You are not authorized to validate datasets."}

    valid, df = validate_dataset(file_path)

    if not valid:
        log_event(username=username, action="Dataset Validation", status="FAILED")
        return {"success": False, "df": None, "message": "Validation failed. See report for details."}

    log_event(username=username, action="Dataset Validation", status="SUCCESS")
    return {"success": True, "df": df, "message": f"Validation passed ({len(df):,} rows)."}


# ---------------------------------------------------------------------------
# Secure import pipeline (Phase 7-9) - user picks a file via file dialog
# ---------------------------------------------------------------------------

def run_import_pipeline(username, role, file_path, progress_cb=None):
    """
    Runs: permission check -> validate -> hash -> save hash -> generate
    batch ID -> import_dataset() (encrypts + inserts + logs).

    progress_cb(step_label: str, pct: int) is called after each stage,
    if provided.

    Returns a result dict describing what happened.
    """
    def report(step, pct):
        if progress_cb:
            progress_cb(step, pct)

    if not has_permission(role, "import"):
        log_event(username=username, action="Permission Denied: Import Dataset", status="FAILED")
        return {"success": False, "stage": "permission", "message": "You are not authorized to import datasets."}

    # --- Validate ---
    report("Validating dataset...", 10)
    valid, df = validate_dataset(file_path)
    if not valid:
        log_event(username=username, action="Dataset Validation", status="FAILED")
        return {"success": False, "stage": "validation", "message": "Validation failed. Import stopped."}
    log_event(username=username, action="Dataset Validation", status="SUCCESS")

    # --- Hash ---
    report("Generating SHA-256 hash...", 30)
    file_hash = generate_hash(file_path)
    log_event(username=username, action="SHA-256 Hash Generated", status="SUCCESS")

    # --- Save hash (keyed by batch, so multiple uploads don't collide) ---
    batch_id = f"BATCH-{uuid.uuid4().hex[:8]}"
    report("Saving hash & generating batch ID...", 45)
    hash_file = os.path.join(HASH_DIR, f"{batch_id}.sha256")
    save_hash(file_hash, hash_file)

    # --- Import (encrypt + insert + audit log, all inside importer.py) ---
    report("Encrypting sensitive fields & importing to PostgreSQL...", 70)
    try:
        result = import_dataset(
            file_path=file_path,
            batch_id=batch_id,
            file_hash=file_hash,
            uploaded_by=username,
        )
    except Exception as e:
        report("Import failed", 100)
        return {
            "success": False,
            "stage": "import",
            "message": f"Import failed: {e}",
            "trace": traceback.format_exc(),
        }

    report("Done", 100)

    if result is None:
        # import_dataset() returns None early if batch already exists
        return {
            "success": False,
            "stage": "duplicate_batch",
            "message": f"Batch '{batch_id}' was already imported.",
        }

    upload_id, batch_id = result
    return {
        "success": True,
        "stage": "complete",
        "message": f"Imported {len(df):,} records.",
        "upload_id": upload_id,
        "batch_id": batch_id,
        "file_hash": file_hash,
        "hash_file": hash_file,
        "record_count": len(df),
    }


# ---------------------------------------------------------------------------
# Integrity verification (Phase 10) - GUI lets user pick file + hash file
# ---------------------------------------------------------------------------

def run_verify_integrity(username, role, file_path, hash_file):
    if not has_permission(role, "verify_hash"):
        log_event(username=username, action="Permission Denied: Verify Dataset Integrity", status="FAILED")
        return {"success": False, "match": None, "message": "You are not authorized to verify dataset integrity."}

    if not os.path.exists(hash_file):
        log_event(username=username, action="Dataset Integrity Verification", status="FAILED")
        return {"success": False, "match": None, "message": "Stored hash file not found."}

    with open(hash_file, "r") as f:
        stored_hash = f.read().strip()

    current_hash = generate_hash(file_path)
    match = current_hash == stored_hash

    log_event(
        username=username,
        action="Dataset Integrity Verification",
        status="SUCCESS" if match else "FAILED",
    )

    if match:
        return {"success": True, "match": True, "message": "Dataset integrity verified — no changes detected."}
    return {"success": True, "match": False, "message": "WARNING: dataset has been modified since import."}


# ---------------------------------------------------------------------------
# Audit logs / security events (Phase 9 / 12) - read-only queries
# ---------------------------------------------------------------------------

def get_audit_logs(username, role, limit=None):
    """
    Returns every audit log row, newest first. Pass a limit explicitly
    if you ever want to cap it again — None means no limit.
    """
    if not has_permission(role, "view_logs"):
        log_event(username=username, action="Permission Denied: View Audit Logs", status="FAILED")
        return None

    connection = get_connection()
    cursor = connection.cursor()
    query = """
        SELECT log_id, username, action, status, log_time
        FROM audit_logs
        ORDER BY log_time DESC
    """
    if limit:
        query += " LIMIT %s;"
        cursor.execute(query, (limit,))
    else:
        cursor.execute(query + ";")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    log_event(username=username, action="Viewed Audit Logs", status="SUCCESS")
    return rows


def get_security_events(username, role, limit=None):
    """
    Returns every security-relevant event, newest first. Pass a limit
    explicitly if you ever want to cap it again — None means no limit.
    """
    if not has_permission(role, "view_security_events"):
        log_event(username=username, action="Permission Denied: View Security Events", status="FAILED")
        return None

    connection = get_connection()
    cursor = connection.cursor()
    query = """
        SELECT log_id, username, action, status, log_time
        FROM audit_logs
        WHERE
            status IN ('FAILED', 'WARNING')
            OR action ILIKE '%%Permission Denied%%'
            OR action ILIKE '%%Integrity%%'
            OR action ILIKE '%%Encrypted%%'
        ORDER BY log_time DESC
    """
    if limit:
        query += " LIMIT %s;"
        cursor.execute(query, (limit,))
    else:
        cursor.execute(query + ";")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    log_event(username=username, action="Viewed Security Events", status="SUCCESS")
    return rows


# ---------------------------------------------------------------------------
# Export (Phase 11) - GUI supplies row count instead of input()
# ---------------------------------------------------------------------------

EXPORT_FOLDER = "exports"
EXPORT_THRESHOLD = 50000


def run_export(username, role, num_rows):
    import pandas as pd
    from pathlib import Path

    if not has_permission(role, "export"):
        log_event(username=username, action="Permission Denied: Export Data", status="FAILED")
        return {"success": False, "message": "You are not authorized to export data."}

    if num_rows <= 0:
        return {"success": False, "message": "Please enter a positive number."}

    connection = get_connection()
    df = pd.read_sql("SELECT * FROM customers LIMIT %s;", connection, params=(num_rows,))
    connection.close()

    Path(EXPORT_FOLDER).mkdir(exist_ok=True)
    file_name = f"{EXPORT_FOLDER}/customers_export.csv"
    df.to_csv(file_name, index=False)

    log_event(username=username, action="Data Export", status="SUCCESS")

    warning = None
    if len(df) >= EXPORT_THRESHOLD:
        log_event(username=username, action="Bulk Data Export Detected", status="WARNING")
        warning = f"Large export detected: {len(df):,} records exceeds the {EXPORT_THRESHOLD:,} threshold."

    return {
        "success": True,
        "message": f"Exported {len(df):,} records to {file_name}",
        "warning": warning,
        "file_name": file_name,
        "record_count": len(df),
    }
