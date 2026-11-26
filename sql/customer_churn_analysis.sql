CREATE DATABASE churn_test_db;
SHOW DATABASES;
use churn_test_db;
show tables;
select * from customers;

SELECT COUNT(*) AS missing_total_charges
FROM customers
WHERE TotalCharges IS NULL;

-- 1. Count imported customer records
SELECT COUNT(*) AS total_customers
FROM customers;

-- 2. Check the table structure
DESCRIBE customers;

-- 3. Count missing TotalCharges values
SELECT COUNT(*) AS missing_total_charges
FROM customers
WHERE TotalCharges IS NULL;
-- Inspect records with zero tenure
SELECT customerID, tenure, MonthlyCharges, TotalCharges
FROM customers
WHERE tenure = 0;
-- Check whether MySQL imported zero TotalCharges values
SELECT COUNT(*) AS zero_total_charges
FROM customers
WHERE TotalCharges = 0;
-- Restore the 11 missing TotalCharges values as NULL
UPDATE customers
SET TotalCharges = NULL
WHERE tenure = 0
AND TotalCharges = 0;
-- 4. BASIC CUSTOMER ANALYSIS
-- Display all columns and records from the customers table
SELECT *
FROM customers;

-- Display only important customer information
SELECT customerID, gender, tenure, Contract, MonthlyCharges, Churn
FROM customers;

-- Display the first 10 customer records
SELECT *
FROM customers
LIMIT 10;

-- Find customers who have left the company
SELECT *
FROM customers
WHERE Churn = 'Yes';

-- Find customers who are still with the company
SELECT *
FROM customers
WHERE Churn = 'No';

-- Find customers using month-to-month contracts
SELECT *
FROM customers
WHERE Contract = 'Month-to-month';

-- Find customers with tenure of 12 months or less
SELECT *
FROM customers
WHERE tenure <= 12;

-- Find customers who have left and had a month-to-month contract
SELECT *
FROM customers
WHERE Churn = 'Yes'
AND Contract = 'Month-to-month';
-- Display customers from lowest to highest monthly charges
SELECT customerID, MonthlyCharges
FROM customers
ORDER BY MonthlyCharges ASC;

-- Display customers from highest to lowest monthly charges
SELECT customerID, MonthlyCharges
FROM customers
ORDER BY MonthlyCharges DESC;

-- Display customers from highest to lowest tenure
SELECT customerID, tenure
FROM customers
ORDER BY tenure DESC;

-- Display the 10 customers with the highest monthly charges
SELECT customerID, MonthlyCharges
FROM customers
ORDER BY MonthlyCharges DESC
LIMIT 10;

-- Count the total number of customer records
SELECT COUNT(*) AS total_customers
FROM customers;

-- Count the number of customers who left
SELECT COUNT(*) AS churned_customers
FROM customers
WHERE Churn = 'Yes';

-- Count the number of customers who stayed
SELECT COUNT(*) AS retained_customers
FROM customers
WHERE Churn = 'No';

-- Count unique customer IDs
SELECT COUNT(DISTINCT customerID) AS unique_customers
FROM customers;

-- Find all unique contract types
SELECT DISTINCT Contract
FROM customers;

-- Find all unique internet service types
SELECT DISTINCT InternetService
FROM customers;

-- Find all unique payment methods
SELECT DISTINCT PaymentMethod
FROM customers;

-- Find all unique churn categories
SELECT DISTINCT Churn
FROM customers;

-- Count customers in each churn category
SELECT Churn, COUNT(*) AS customer_count
FROM customers
GROUP BY Churn;

-- Count customers in each contract type
SELECT Contract, COUNT(*) AS customer_count
FROM customers
GROUP BY Contract;

-- Count customers in each internet service category
SELECT InternetService, COUNT(*) AS customer_count
FROM customers
GROUP BY InternetService;

-- Count customers using each payment method
SELECT PaymentMethod, COUNT(*) AS customer_count
FROM customers
GROUP BY PaymentMethod;

-- Calculate average monthly charges for each contract type
SELECT Contract, AVG(MonthlyCharges) AS average_monthly_charges
FROM customers
GROUP BY Contract;

-- 5. CHURN ANALYSIS
-- Count customers whose Churn status is 'Yes'
SELECT COUNT(*) AS churned_customers
FROM customers
WHERE Churn = 'Yes';
-- Count customers who stayed with the company
SELECT COUNT(*) AS retained_customers
FROM customers
WHERE Churn = 'No';
-- Calculate the overall customer churn rate as a percentage

SELECT
    ROUND(
        SUM(
            CASE
                WHEN Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM customers;
-- Count the total customers in each contract type
SELECT
    Contract,
    COUNT(*) AS total_customers
FROM customers
GROUP BY Contract;
-- Count total and churned customers for each contract type
SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(
        CASE
            WHEN Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers
FROM customers
GROUP BY Contract;
-- Calculate churn rate separately for each contract type
SELECT
    Contract,
    ROUND(
        SUM(
            CASE
                WHEN Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY Contract;
-- Business Finding:
-- Month-to-month contracts have the highest churn rate (42.71%).
-- Two-year contracts have the lowest churn rate (2.83%).
-- Investigate why customers on shorter contracts leave more frequently.

-- Display each customer with their assigned tenure group
SELECT
    customerID,
    tenure,
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49-72 months'
    END AS tenure_group
FROM customers;

-- TENURE GROUP ANALYSIS
SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49-72 months'
    END AS tenure_group,
    COUNT(*) AS total_customers
FROM customers
GROUP BY
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49-72 months'
    END;
    
-- Calculate customer count, churned customers, and churn rate by tenure group

SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49-72 months'
    END AS tenure_group,

    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,

    ROUND(
        SUM(
            CASE
                WHEN Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS churn_rate

FROM customers

GROUP BY
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49-72 months'
    END;
-- Business Finding:
-- Customers with 0-12 months of tenure have the highest churn rate (47.44%).
-- Customers with 49-72 months of tenure have the lowest churn rate (9.51%).
-- The company should investigate early-stage customer dissatisfaction
-- and test targeted retention offers.

-- Classify customers into monthly charge groups
SELECT
    customerID,
    MonthlyCharges,
    CASE
        WHEN MonthlyCharges <= 50 THEN 'Low'
        WHEN MonthlyCharges <= 85 THEN 'Medium'
        ELSE 'High'
    END AS charge_group
FROM customers;
-- Business Finding:
-- High-charge customers have the highest churn rate (33.82%).
-- Low-charge customers have the lowest churn rate (15.70%).
-- Investigate whether customers feel they receive sufficient value
-- for the monthly price they pay.
-- =====================================
-- MONTHLY CHARGE ANALYSIS
-- =====================================

-- Compare customer count, churned customers, and churn rate
-- across Low, Medium, and High monthly charge groups

SELECT
    CASE
        WHEN MonthlyCharges <= 50 THEN 'Low'
        WHEN MonthlyCharges <= 85 THEN 'Medium'
        ELSE 'High'
    END AS charge_group,

    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,

    ROUND(
        SUM(
            CASE
                WHEN Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS churn_rate

FROM customers

GROUP BY
    CASE
        WHEN MonthlyCharges <= 50 THEN 'Low'
        WHEN MonthlyCharges <= 85 THEN 'Medium'
        ELSE 'High'
    END;
    
-- Find customers with month-to-month contracts
SELECT *
FROM customers
WHERE Contract = 'Month-to-month';

-- Find high-paying customers with month-to-month contracts
SELECT customerID, Contract
FROM customers
WHERE Contract = 'Month-to-month'
AND MonthlyCharges > 85;

-- Count high-paying customers with month-to-month contracts
SELECT COUNT(*) AS customer_count
FROM customers
WHERE Contract = 'Month-to-month'
AND MonthlyCharges > 85;

-- Count churned, high-paying customers with month-to-month contracts
SELECT COUNT(*) AS churned_customers
FROM customers
WHERE Contract = 'Month-to-month'
AND MonthlyCharges > 85
AND Churn = 'Yes';

-- Calculate churn rate among high-paying, month-to-month customers
SELECT
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS segment_churn_rate
FROM customers
WHERE Contract = 'Month-to-month'
AND MonthlyCharges > 85;


USE churn_test_db;

-- Churn analysis by contract and tenure group
WITH customer_segments AS (
    SELECT
        customerID,
        Contract,
        Churn,
        CASE
            WHEN tenure <= 12 THEN '0-12 months'
            WHEN tenure <= 24 THEN '13-24 months'
            WHEN tenure <= 48 THEN '25-48 months'
            ELSE '49-72 months'
        END AS tenure_group
    FROM customers
)

SELECT
    Contract,
    tenure_group,
    COUNT(*) AS total_customers,

    SUM(
        CASE WHEN Churn = 'Yes'
        THEN 1 ELSE 0 END
    ) AS churned_customers,

    ROUND(
        SUM(
            CASE WHEN Churn = 'Yes'
            THEN 1 ELSE 0 END
        ) * 100.0 / COUNT(*),
        2
    ) AS churn_rate

FROM customer_segments

GROUP BY Contract, tenure_group
ORDER BY Contract, tenure_group;
