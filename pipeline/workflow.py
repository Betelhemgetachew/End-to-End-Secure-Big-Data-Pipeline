import uuid

from authorization import has_permission
from validator import validate_dataset
from hasher import generate_hash, save_hash
from importer import import_dataset
from logger import log_event

DATASET = "dataset/customers.csv"
HASH_FILE = "hashes/customers.sha256"

def validate_workflow(username, role):
    """
    Validate the dataset.
    """

    if not has_permission(role, "validate"):

        log_event(
            username=username,
            action="Permission Denied: Validate Dataset",
            status="FAILED"
        )

        print("\nYou are not authorized to validate datasets.")
        return False

    valid, _ = validate_dataset(DATASET)

    if not valid:

        log_event(
            username=username,
            action="Dataset Validation",
            status="FAILED"
        )

        print("\nPipeline stopped.")

        return False

    log_event(
        username=username,
        action="Dataset Validation",
        status="SUCCESS"
    )

    print("\nDataset validation completed successfully.")

    return True

def import_workflow(username, role):
    """
    Run the secure import pipeline.
    """

    if not has_permission(role, "import"):

        log_event(
            username=username,
            action="Permission Denied: Import Dataset",
            status="FAILED"
        )

        print("\nYou are not authorized to import datasets.")
        return

    # -----------------------------------------
    # Always validate before importing
    # -----------------------------------------

    valid = validate_workflow(username, role)

    if not valid:
        return

    # -----------------------------------------
    # Generate SHA-256 hash
    # -----------------------------------------

    print("\nGenerating SHA-256 hash...")

    hash_value = generate_hash(DATASET)

    print("Hash generated successfully.")
    print(hash_value)

    log_event(
        username=username,
        action="SHA-256 Hash Generated",
        status="SUCCESS"
    )

    # -----------------------------------------
    # Save hash
    # -----------------------------------------

    save_hash(hash_value, HASH_FILE)

    print(f"\nHash saved to: {HASH_FILE}")

    # -----------------------------------------
    # Generate Batch ID
    # -----------------------------------------

    batch_id = f"BATCH-{uuid.uuid4().hex[:8]}"

    print(f"\nGenerated Batch ID: {batch_id}")

    # -----------------------------------------
    # Import
    # -----------------------------------------

    print("\nImporting dataset into PostgreSQL...")

    import_dataset(
        file_path=DATASET,
        batch_id=batch_id,
        file_hash=hash_value,
        uploaded_by=username
    )

    print("\nPipeline completed successfully.")