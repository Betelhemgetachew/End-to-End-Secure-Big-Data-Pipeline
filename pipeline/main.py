from validator import validate_dataset

DATASET = "dataset/customers.csv"

valid, df = validate_dataset(DATASET)

if valid:
    print("\nPipeline can continue.")
else:
    print("\nPipeline stopped.")