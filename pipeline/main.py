import uuid

from auth import login
from authorization import has_permission

from validator import validate_dataset
from hasher import generate_hash, save_hash
from importer import import_dataset
from logger import log_event

DATASET = "dataset/customers.csv"
HASH_FILE = "hashes/customers.sha256"

# ============================================================
# Step 1: User Authentication
# ============================================================

user = login()

if user is None:
    print("\nAccess denied.")
    exit()

username, role = user

# ============================================================
# Step 2: Validate the dataset
# ============================================================

if not has_permission(role, "validate"):
    print("\nYou are not authorized to validate datasets.")
    exit()

valid, df = validate_dataset(DATASET)

if not valid:

    log_event(
        username=username,
        action="Dataset Validation",
        status="FAILED"
    )

    print("\nPipeline stopped.")
    exit()

log_event(
    username=username,
    action="Dataset Validation",
    status="SUCCESS"
)

print("\nPipeline can continue.")

# ============================================================
# Step 3: Generate SHA-256 hash
# ============================================================

print("\nGenerating SHA-256 hash...")

hash_value = generate_hash(DATASET)

print("Hash generated successfully.")
print(hash_value)
log_event(
    username=username,
    action="SHA-256 Hash Generated",
    status="SUCCESS"
)

# ============================================================
# Step 4: Save the hash
# ============================================================

save_hash(hash_value, HASH_FILE)

print(f"\nHash saved to: {HASH_FILE}")

# ============================================================
# Step 5: Generate Batch ID
# ============================================================

batch_id = f"BATCH-{uuid.uuid4().hex[:8]}"

print(f"\nGenerated Batch ID: {batch_id}")

# ============================================================
# Step 6: Import the dataset
# ============================================================

if not has_permission(role, "import"):
    print("\nYou are not authorized to import datasets.")
    exit()

print("\nImporting dataset into PostgreSQL...")

import_dataset(
    file_path=DATASET,
    batch_id=batch_id,
    file_hash=hash_value,
    uploaded_by=username
)

print("\nPipeline completed successfully.")