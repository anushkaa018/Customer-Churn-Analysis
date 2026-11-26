
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

url = URL.create(
    "mysql+mysqlconnector",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=3306,
    database="churn_test_db"
)

engine = create_engine(url)

test_id = "PIPELINE-TEST-001"

try:
    with engine.begin() as connection:

        # Insert a temporary customer
        connection.execute(
            text("""
                INSERT INTO customers
                (customerID, gender, SeniorCitizen, Partner,
                 Dependents, tenure, PhoneService, MultipleLines,
                 InternetService, OnlineSecurity, OnlineBackup,
                 DeviceProtection, TechSupport, StreamingTV,
                 StreamingMovies, Contract, PaperlessBilling,
                 PaymentMethod, MonthlyCharges, TotalCharges, Churn)
                VALUES
                (:id, 'Male', 0, 'No', 'No', 1, 'Yes', 'No',
                 'DSL', 'No', 'No', 'No', 'No', 'No', 'No',
                 'Month-to-month', 'Yes', 'Electronic check',
                 99.99, 99.99, 'No')
            """),
            {"id": test_id}
        )

        print("Temporary customer inserted!")

        # Verify the record
        result = connection.execute(
            text("""
                SELECT customerID, MonthlyCharges
                FROM customers
                WHERE customerID = :id
            """),
            {"id": test_id}
        ).fetchone()

        print("MySQL verification:", result)

    print("Python to MySQL test successful!")

except Exception as error:
    print("Test failed:", error)

finally:
    engine.dispose()
