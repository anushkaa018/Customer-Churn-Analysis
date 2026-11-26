
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "processed" / "Telco-Customer-Churn-Clean.csv"

# Load database credentials
load_dotenv(BASE_DIR / ".env")

url = URL.create(
    drivername="mysql+mysqlconnector",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=3306,
    database="churn_test_db"
)

engine = create_engine(url)

try:
    # Read processed dataset
    df = pd.read_csv(CSV_PATH)

    print("CSV loaded:", len(df), "rows")

    with engine.begin() as connection:

        # Prevent accidental duplicate loading
        existing_count = connection.execute(
            text("SELECT COUNT(*) FROM customers")
        ).scalar()

        if existing_count > 0:
            raise ValueError(
                "The customers table is not empty. Loading stopped."
            )

        # Load data into MySQL
        df.to_sql(
            name="customers",
            con=connection,
            if_exists="append",
            index=False,
            chunksize=1000
        )

        # Verify database records
        db_count = connection.execute(
            text("SELECT COUNT(*) FROM customers")
        ).scalar()

        print("Records loaded:", db_count)

        if db_count != len(df):
            raise ValueError("Record count verification failed.")

    print("Data loading and verification successful!")

except Exception as error:
    print("Error:", error)

finally:
    engine.dispose()
