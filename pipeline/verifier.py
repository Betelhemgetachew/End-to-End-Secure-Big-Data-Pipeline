from authorization import has_permission
from hasher import generate_hash
from logger import log_event

DATASET = "dataset/customers.csv"
HASH_FILE = "hashes/customers.sha256"


def verify_dataset_hash(username, role):
    """
    Verify that the dataset has not been modified.
    """

    if not has_permission(role, "verify_hash"):

        log_event(
            username=username,
            action="Permission Denied: Verify Dataset Integrity",
            status="FAILED"
        )

        print("\nYou are not authorized to verify dataset integrity.")
        return

    try:

        with open(HASH_FILE, "r") as file:
            stored_hash = file.read().strip()

    except FileNotFoundError:

        log_event(
            username=username,
            action="Dataset Integrity Verification",
            status="FAILED"
        )

        print("\nStored hash file not found.")
        return

    current_hash = generate_hash(DATASET)

    if current_hash == stored_hash:

        log_event(
            username=username,
            action="Dataset Integrity Verification",
            status="SUCCESS"
        )

        print("\nDataset integrity verified.")
        print("The dataset has NOT been modified.")

    else:

        log_event(
            username=username,
            action="Dataset Integrity Verification",
            status="FAILED"
        )

        print("\nWARNING!")
        print("Dataset integrity verification FAILED.")
        print("The dataset has been modified.")