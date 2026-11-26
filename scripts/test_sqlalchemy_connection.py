
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

# Load existing project credentials
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Connect to the separate test database
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
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DATABASE()")
        )
        print("Connected database:", result.scalar())
        print("SQLAlchemy connection successful!")

except Exception as error:
    print("Connection failed:", error)

finally:
    engine.dispose()
