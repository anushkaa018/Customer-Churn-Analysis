import logging
import sys
from pathlib import Path

import pandas as pd
from pandas.api.types import is_float_dtype, is_integer_dtype, is_string_dtype


# --------------------------------------------------
# Configuration
# --------------------------------------------------

# Use the file path provided through command-line arguments.
if len(sys.argv) > 1:
    FILE_PATH = Path(sys.argv[1])
    #python automation/validate_data.py "data/incoming/Telco-Customer-Churn-New.csv"(command-line argument)

# Otherwise, use the original cleaned dataset.
else:
    FILE_PATH = Path(
        r"E:\My Project\Customer-churn-analysis\data\processed\Telco-Customer-Churn-Clean.csv"
    )

# The log file is created beside this Python script.
LOG_FILE = Path(__file__).resolve().parent / "validation.log"

# These checks are specific to the current IBM Telco dataset.
CUSTOMER_ID_PATTERN = r"\d{4}-[A-Za-z]{5}"

EXPECTED_COLUMNS = [
    "customerID", "gender", "SeniorCitizen", "Partner",
    "Dependents", "tenure", "PhoneService", "MultipleLines",
    "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV",
    "StreamingMovies", "Contract", "PaperlessBilling",
    "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn"
]

EXPECTED_DTYPES = {
    "customerID": "string",
    "SeniorCitizen": "integer",
    "tenure": "integer",
    "MonthlyCharges": "float",
    "TotalCharges": "float",
    "Churn": "string"
}

ALLOWED_VALUES = {
    "Churn": {"Yes", "No"},
    "SeniorCitizen": {0, 1},
    "Partner": {"Yes", "No"},
    "Dependents": {"Yes", "No"},
    "gender": {"Male", "Female"},
    "PhoneService": {"Yes", "No"},
    "MultipleLines": {"Yes", "No", "No phone service"},
    "InternetService": {"DSL", "Fiber optic", "No"},
    "OnlineSecurity": {"Yes", "No", "No internet service"},
    "OnlineBackup": {"Yes", "No", "No internet service"},
    "DeviceProtection": {"Yes", "No", "No internet service"},
    "TechSupport": {"Yes", "No", "No internet service"},
    "StreamingTV": {"Yes", "No", "No internet service"},
    "StreamingMovies": {"Yes", "No", "No internet service"},
    "Contract": {"Month-to-month", "One year", "Two year"},
    "PaperlessBilling": {"Yes", "No"},
    "PaymentMethod": {
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    }
}

# Project validation boundaries, not observed dataset maximums.
NUMERICAL_RULES = {
    "tenure": lambda values: (values < 0) | (values > 72),
    "MonthlyCharges": lambda values: (values < 0) | (values > 200),
    "TotalCharges": lambda values: values < 0
}


# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)
logging.info("Data validation application started.")

validation_results = {}


def record_result(check_name, passed, message):
    """Save a check result and write it to the log."""
    status = "PASS" if passed else "FAIL"
    validation_results[check_name] = status

    if passed:
        logging.info("%s: %s", check_name, message)
    else:
        logging.warning("%s: %s", check_name, message)


def matches_expected_dtype(series, expected_type):
    """Check a pandas Series against a broad expected type."""
    if expected_type == "string":
        return is_string_dtype(series.dtype)
    if expected_type == "integer":
        return is_integer_dtype(series.dtype)
    if expected_type == "float":
        return is_float_dtype(series.dtype)
    return False


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print(f"Error: Dataset file not found:\n{FILE_PATH}")
    logging.exception("Dataset file not found: %s", FILE_PATH)
    sys.exit(1)
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")
    logging.exception("The CSV file is empty: %s", FILE_PATH)
    sys.exit(1)
except Exception:
    print("Unexpected error while loading the dataset. Check validation.log.")
    logging.exception("Unexpected error while loading dataset.")
    sys.exit(1)

print("Dataset loaded successfully!")
logging.info("Dataset loaded successfully: %s", FILE_PATH)
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())


# --------------------------------------------------
# Validate required columns
# --------------------------------------------------

missing_columns = sorted(set(EXPECTED_COLUMNS) - set(df.columns))

if missing_columns:
    record_result(
        "Required Columns", False,
        f"Missing required columns: {missing_columns}"
    )
    print("Validation failed. Missing required columns:", missing_columns)
    print("Cannot safely continue with the remaining checks.")
    logging.error("Validation stopped because required columns are missing.")
    sys.exit(1)

record_result("Required Columns", True, "All required columns are present.")
print("All required columns are present!")


# --------------------------------------------------
# Display missing-value summary
# --------------------------------------------------

missing_summary = df.isnull().sum()
print("\nMissing Values Summary:")
print(missing_summary[missing_summary > 0])


# --------------------------------------------------
# Validate data types
# --------------------------------------------------

for column, expected_type in EXPECTED_DTYPES.items():
    passed = matches_expected_dtype(df[column], expected_type)
    actual_type = str(df[column].dtype)

    record_result(
        f"Data Type: {column}", passed,
        f"Expected {expected_type}; found {actual_type}."
    )

    if passed:
        print(f"{column} data type validation passed!")
    else:
        print(
            f"Validation failed for {column}: "
            f"expected {expected_type}, found {actual_type}"
        )


# --------------------------------------------------
# Validate customer IDs
# --------------------------------------------------

duplicate_count = int(df["customerID"].duplicated().sum())
record_result(
    "Duplicate Customer IDs", duplicate_count == 0,
    f"{duplicate_count} duplicate customer IDs found."
)

if duplicate_count:
    print(f"Validation failed: {duplicate_count} duplicate customer IDs found!")
    print(df[df["customerID"].duplicated(keep=False)][["customerID"]])
else:
    print("Customer ID validation passed: No duplicates found!")


missing_id_mask = df["customerID"].isna()
blank_id_mask = (
    df["customerID"].astype("string").str.strip().eq("").fillna(False)
)
missing_id_count = int((missing_id_mask | blank_id_mask).sum())

record_result(
    "Missing or Blank Customer IDs", missing_id_count == 0,
    f"{missing_id_count} missing or blank customer IDs found."
)

if missing_id_count:
    print(f"Validation failed: {missing_id_count} missing or blank customer IDs found!")
    print(df.loc[missing_id_mask | blank_id_mask, ["customerID"]])
else:
    print("Customer ID validation passed: No missing or blank IDs found!")


invalid_id_mask = ~df["customerID"].astype("string").str.fullmatch(
    CUSTOMER_ID_PATTERN, na=False
)
invalid_id_count = int(invalid_id_mask.sum())

record_result(
    "Customer ID Format", invalid_id_count == 0,
    f"{invalid_id_count} customer IDs have an invalid format."
)

if invalid_id_count:
    print(f"Validation failed: {invalid_id_count} customer IDs have an invalid format!")
    print(df.loc[invalid_id_mask, ["customerID"]])
else:
    print("Customer ID format validation passed!")


# --------------------------------------------------
# Validate categorical values
# --------------------------------------------------

for column, valid_values in ALLOWED_VALUES.items():
    invalid_mask = ~df[column].isin(valid_values)
    invalid_count = int(invalid_mask.sum())

    record_result(
        f"Categorical: {column}", invalid_count == 0,
        f"{invalid_count} invalid values found."
    )

    if invalid_count:
        print(f"Validation failed for {column}: {invalid_count} invalid records found!")
        print(df.loc[invalid_mask, ["customerID", column]])
    else:
        print(f"{column} validation passed!")


# --------------------------------------------------
# Validate blank strings
# --------------------------------------------------

blank_string_columns = [
    "customerID", "gender", "Partner", "Dependents", "PhoneService",
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod", "Churn"
]

for column in blank_string_columns:
    blank_mask = (
        df[column].astype("string").str.strip().eq("").fillna(False)
    )
    blank_count = int(blank_mask.sum())

    record_result(
        f"Blank Strings: {column}", blank_count == 0,
        f"{blank_count} blank or whitespace-only values found."
    )

    if blank_count:
        print(f"Validation failed for {column}: {blank_count} blank values found!")
        print(df.loc[blank_mask, ["customerID", column]])


# --------------------------------------------------
# Validate numerical ranges
# --------------------------------------------------

for column, validation_rule in NUMERICAL_RULES.items():
    invalid_mask = validation_rule(df[column])
    invalid_count = int(invalid_mask.sum())

    record_result(
        f"Numerical: {column}", invalid_count == 0,
        f"{invalid_count} values outside the configured validation range."
    )

    if invalid_count:
        print(f"Validation failed for {column}: {invalid_count} invalid records found!")
        print(df.loc[invalid_mask, ["customerID", column]])
    else:
        print(f"{column} numerical validation passed!")


# --------------------------------------------------
# # Validate TotalCharges missing values
# --------------------------------------------------

missing_total_charges = int(df["TotalCharges"].isna().sum())

record_result(
    "TotalCharges Missing Values",
    True,
    f"{missing_total_charges} missing values found."
)

print(f"TotalCharges: {missing_total_charges} missing values found.")

# --------------------------------------------------
# Final validation report
# --------------------------------------------------

print("\n" + "=" * 50)
print("FINAL DATA VALIDATION REPORT")
print("=" * 50)

for check, result in validation_results.items():
    print(f"{check}: {result}")

passed_checks = list(validation_results.values()).count("PASS")
failed_checks = list(validation_results.values()).count("FAIL")

print("-" * 50)
print(f"Total Checks: {len(validation_results)}")
print(f"Passed: {passed_checks}")
print(f"Failed: {failed_checks}")

if failed_checks == 0:
    print("\nOVERALL STATUS: ALL VALIDATIONS PASSED!")
    logging.info(
        "Validation completed successfully. Passed: %s; Failed: %s.",
        passed_checks, failed_checks
    )
else:
    print("\nOVERALL STATUS: VALIDATION FAILED!")
    logging.warning(
        "Validation completed with failures. Passed: %s; Failed: %s.",
        passed_checks, failed_checks
    )

logging.info("Data validation application finished.")
print(f"\nLog file saved at: {LOG_FILE}")

if failed_checks > 0:
    sys.exit(1)
