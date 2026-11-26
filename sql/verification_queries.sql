SELECT Churn, COUNT(*) AS total_customers
FROM customers
GROUP BY Churn;

SELECT COUNT(*) AS missing_total_charges
FROM customers
WHERE TotalCharges IS NULL;
SELECT COUNT(DISTINCT customerID) AS unique_customers
FROM customers;

SELECT COUNT(*) AS zero_tenure_customers
FROM customers
WHERE tenure = 0;

SELECT customerID, MonthlyCharges
FROM customers
WHERE customerID = '7590-VHVEG';

SELECT COUNT(*) FROM customers;

DELETE FROM customers
WHERE customerID IN (
    '9002-FGHIJ',
    '9003-KLMNO',
    '9004-PQRST',
    '9005-UVWXY',
    '9006-BCDEF',
    '9007-GHIJK',
    '9008-LMNOP',
    '9009-QRSTU',
    '9010-VWXYZ'
);

UPDATE customers
SET
    gender = 'Female',
    SeniorCitizen = 0,
    Partner = 'Yes',
    Dependents = 'No',
    tenure = 1,
    PhoneService = 'No',
    MultipleLines = 'No phone service',
    InternetService = 'DSL',
    OnlineSecurity = 'No',
    OnlineBackup = 'Yes',
    DeviceProtection = 'No',
    TechSupport = 'No',
    StreamingTV = 'No',
    StreamingMovies = 'No',
    Contract = 'Month-to-month',
    PaperlessBilling = 'Yes',
    PaymentMethod = 'Electronic check',
    MonthlyCharges = 29.85,
    TotalCharges = 29.85,
    Churn = 'No'
WHERE customerID = '7590-VHVEG';

SELECT COUNT(*) FROM customers;

SELECT customerID, MonthlyCharges, TotalCharges
FROM customers
WHERE customerID = '7590-VHVEG';

DELETE FROM customers
WHERE customerID = '9001-ABCDE';

SHOW CREATE TABLE customers;

START TRANSACTION;

INSERT INTO customers (customerID, gender, tenure, Churn)
VALUES ('TEST001', 'Invalid', -5, 'Maybe');

SELECT * FROM customers
WHERE customerID = 'TEST001';
ROLLBACK;

USE churn_test_db;

SELECT *
FROM customers
WHERE customerID = 'PIPELINE-TEST-001';

USE churn_test_db;

DELETE FROM customers
WHERE customerID = 'PIPELINE-TEST-001';