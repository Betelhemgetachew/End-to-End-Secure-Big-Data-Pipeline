from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "first_name",
    "last_name",
    "email",
    "phone",
    "national_id",
    "city",
    "account_number",
    "account_type",
    "account_balance"
]

VALID_ACCOUNT_TYPES = {
    "standard",
    "premium",
    "business"
}


def validate_dataset(file_path):
    """
    Validate the dataset before it enters the pipeline.
    Returns:
        (True, dataframe) if validation succeeds
        (False, None) if validation fails
    """

    errors = []

    # -------------------------
    # Check file exists
    # -------------------------

    if not Path(file_path).exists():
        errors.append(f"File not found: {file_path}")
        print_errors(errors)
        return False, None

    # -------------------------
    # Read CSV
    # -------------------------

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        errors.append(str(e))
        print_errors(errors)
        return False, None

    # -------------------------
    # Empty dataset
    # -------------------------

    if df.empty:
        errors.append("Dataset is empty.")

    # -------------------------
    # Required columns
    # -------------------------

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        errors.append(
            f"Missing columns: {', '.join(sorted(missing_columns))}"
        )

    # -------------------------
    # Missing values
    # -------------------------

    if df.isnull().values.any():
        errors.append("Dataset contains missing values.")

    # -------------------------
    # Duplicate emails
    # -------------------------

    if "email" in df.columns:
        duplicates = df["email"].duplicated().sum()

        if duplicates > 0:
            errors.append(
                f"Duplicate emails found: {duplicates}"
            )

    # -------------------------
    # Duplicate account numbers
    # -------------------------

    if "account_number" in df.columns:
        duplicates = df["account_number"].duplicated().sum()

        if duplicates > 0:
            errors.append(
                f"Duplicate account numbers found: {duplicates}"
            )

    # -------------------------
    # Account type validation
    # -------------------------

    if "account_type" in df.columns:

        invalid = df[
            ~df["account_type"].isin(VALID_ACCOUNT_TYPES)
        ]

        if not invalid.empty:
            errors.append(
                f"Invalid account types: {len(invalid)}"
            )

    # -------------------------
    # Negative balances
    # -------------------------

    if "account_balance" in df.columns:

        negatives = df[
            df["account_balance"] < 0
        ]

        if not negatives.empty:
            errors.append(
                f"Negative balances: {len(negatives)}"
            )

    # -------------------------
    # Print results
    # -------------------------

    print("=" * 50)
    print("DATASET VALIDATION REPORT")
    print("=" * 50)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    if errors:

        print("\nValidation FAILED\n")

        print_errors(errors)

        return False, None

    print("\nValidation PASSED")

    return True, df


def print_errors(errors):

    print("\nErrors Found:")

    for error in errors:
        print(f"  ✗ {error}")