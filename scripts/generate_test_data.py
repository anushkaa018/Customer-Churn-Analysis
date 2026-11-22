import pandas as pd

data = {
    "customerID": [
    "7590-VHVEG",
    "9002-FGHIJ",
    "9003-KLMNO",
    "9004-PQRST",
    "9005-UVWXY",
    "9006-BCDEF",
    "9007-GHIJK",
    "9008-LMNOP",
    "9009-QRSTU",
    "9010-VWXYZ"
],
    "gender": ["Male", "Female"] * 5,
    "SeniorCitizen": [0] * 10,
    "Partner": ["Yes", "No"] * 5,
    "Dependents": ["No", "Yes"] * 5,
    "tenure": [1, 3, 6, 12, 24, 36, 48, 60, 70, 72],
    "PhoneService": ["Yes"] * 10,
    "MultipleLines": ["No", "Yes"] * 5,
    "InternetService": ["DSL", "Fiber optic"] * 5,
    "OnlineSecurity": ["No", "Yes"] * 5,
    "OnlineBackup": ["Yes", "No"] * 5,
    "DeviceProtection": ["No", "Yes"] * 5,
    "TechSupport": ["Yes", "No"] * 5,
    "StreamingTV": ["No", "Yes"] * 5,
    "StreamingMovies": ["Yes", "No"] * 5,
    "Contract": ["Month-to-month", "One year"] * 5,
    "PaperlessBilling": ["Yes"] * 10,
    "PaymentMethod": ["Electronic check", "Credit card (automatic)"] * 5,
    "MonthlyCharges": [99.99, 75.20, 55.00, 89.90, 60.25, 95.50, 70.00, 110.00, 80.25, 65.75],
    "TotalCharges": [45.50, 225.60, 330.00, 1078.80, 1446.00, 3438.00, 3360.00, 6600.00, 5617.50, 4734.00],
    "Churn": ["No", "Yes", "No", "No", "Yes", "No", "No", "Yes", "No", "No"]
}

df = pd.DataFrame(data)

file_path = "E:/My Project/Customer-churn-analysis/data/incoming/Telco-Customer-Churn-New.csv"

df.to_csv(file_path, index=False)

print("Test data generated successfully!")
print("Records created:", len(df))
print(df.head())