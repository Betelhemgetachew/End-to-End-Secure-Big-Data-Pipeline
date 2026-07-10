from validator import validate_dataset
from hasher import generate_hash, save_hash

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

print("\nIntegrity module completed successfully.")