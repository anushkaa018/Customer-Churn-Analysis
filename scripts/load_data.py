import subprocess
import sys
import pandas as pd
import mysql.connector

from db_connection import create_connection
from pathlib import Path

# Locate the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Choose the CSV file
if len(sys.argv) > 1:
    FILE_PATH = Path(sys.argv[1])
    #python automation/load_data.py "data/incoming/Telco-Customer-Churn-New.csv"(command-line argument)
else:
    FILE_PATH = BASE_DIR / "data" / "processed" / "Telco-Customer-Churn-Clean.csv"

# Run data validation before loading
VALIDATION_SCRIPT = Path(__file__).resolve().parent / "validate_data.py"

result = subprocess.run(
    [sys.executable, str(VALIDATION_SCRIPT), str(FILE_PATH)]
)

if result.returncode != 0:
    print("Data validation failed. Pipeline stopped.")
    sys.exit(1)

print("Data validation passed. Continuing pipeline...")

# Read CSV into a DataFrame
df = pd.read_csv(FILE_PATH)
# Read CSV into a DataFrame
df = pd.read_csv(FILE_PATH)

# Store customer IDs for database verification
customer_ids = df["customerID"].tolist()

print("Dataset loaded successfully!")
print("Total records:", len(df))

# Replace missing values (NaN) with None
df = df.astype(object).where(pd.notna(df), None)

# Convert DataFrame rows into tuples
records = list(df.itertuples(index=False, name=None))

print("Records prepared for MySQL:", len(records))

# Connect to MySQL
connection = create_connection()

if connection is None:
    print("Database connection failed.")
    sys.exit(1)

#cursor = connection.cursor()

sql = """
INSERT INTO customers (
    customerID, gender, SeniorCitizen, Partner, Dependents,
    tenure, PhoneService, MultipleLines, InternetService,
    OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
    StreamingTV, StreamingMovies, Contract, PaperlessBilling,
    PaymentMethod, MonthlyCharges, TotalCharges, Churn
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON DUPLICATE KEY UPDATE
    gender = VALUES(gender),
    SeniorCitizen = VALUES(SeniorCitizen),
    Partner = VALUES(Partner),
    Dependents = VALUES(Dependents),
    tenure = VALUES(tenure),
    PhoneService = VALUES(PhoneService),
    MultipleLines = VALUES(MultipleLines),
    InternetService = VALUES(InternetService),
    OnlineSecurity = VALUES(OnlineSecurity),
    OnlineBackup = VALUES(OnlineBackup),
    DeviceProtection = VALUES(DeviceProtection),
    TechSupport = VALUES(TechSupport),
    StreamingTV = VALUES(StreamingTV),
    StreamingMovies = VALUES(StreamingMovies),
    Contract = VALUES(Contract),
    PaperlessBilling = VALUES(PaperlessBilling),
    PaymentMethod = VALUES(PaymentMethod),
    MonthlyCharges = VALUES(MonthlyCharges),
    TotalCharges = VALUES(TotalCharges),
    Churn = VALUES(Churn)
"""


cursor = None

try:
    cursor = connection.cursor()

    cursor.executemany(sql, records)
    connection.commit()

    print("Data loading completed successfully!")

    # Verify customer IDs in MySQL
    placeholders = ", ".join(["%s"] * len(customer_ids))

    cursor.execute(
        f"SELECT COUNT(*) FROM customers WHERE customerID IN ({placeholders})",
        customer_ids
    )

    matched_count = cursor.fetchone()[0]

    print("Records processed:", len(customer_ids))
    print("Customer IDs found in MySQL:", matched_count)

    if matched_count == len(set(customer_ids)):
        print("Database verification passed!")
    else:
        print("Database verification failed!")
        connection.rollback()
        sys.exit(1)

except mysql.connector.Error as error:
    connection.rollback()
    print("Data loading failed:", error)
    sys.exit(1)

finally:
    if cursor is not None:
        cursor.close()

    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")
