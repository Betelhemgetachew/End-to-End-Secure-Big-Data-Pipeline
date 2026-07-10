import uuid

from validator import validate_dataset
from hasher import generate_hash, save_hash
from importer import import_dataset

DATASET = "dataset/customers.csv"
HASH_FILE = "hashes/customers.sha256"

# Step 1: Validate the dataset
valid, df = validate_dataset(DATASET)

if not valid:
    print("\nPipeline stopped.")
    exit()

print("\nPipeline can continue.")

# Step 2: Generate SHA-256 hash
print("\nGenerating SHA-256 hash...")

hash_value = generate_hash(DATASET)

print("Hash generated successfully.")
print(hash_value)

# Step 3: Save the hash
save_hash(hash_value, HASH_FILE)

print(f"\nHash saved to: {HASH_FILE}")

# Step 4: Generate a unique batch ID
batch_id = f"BATCH-{uuid.uuid4().hex[:8]}"

print(f"\nGenerated Batch ID: {batch_id}")

# Step 5: Import the dataset
print("\nImporting dataset into PostgreSQL...")

import_dataset(
    file_path=DATASET,
    batch_id=batch_id,
    file_hash=hash_value,
    uploaded_by="Betelhem"
)

print("\nPipeline completed successfully.")