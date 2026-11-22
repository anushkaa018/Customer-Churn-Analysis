# Customer Churn & Retention Analysis

A data analytics project focused on understanding customer churn, identifying high-risk customer segments, and exploring strategies to improve customer retention.

## Project Overview

This project analyzes customer churn data to identify patterns behind customer cancellations and understand which customer segments are more likely to churn.

Using Python, SQL, and Power BI, the project explores customer behavior, analyzes churn patterns, identifies high-risk segments, and presents insights through an interactive dashboard.

## Business Objectives

- Identify key factors associated with customer churn.
- Analyze churn across different customer segments.
- Identify high-risk customer groups.
- Understand the relationship between tenure, contract type, and monthly charges with churn.
- Provide data-driven insights to support customer retention strategies.

## Tools & Technologies

- **Python** – Data analysis and data processing
- **Pandas** – Data manipulation and analysis
- **Matplotlib** – Data visualization
- **MySQL** – Database management and SQL analysis
- **Power BI** – Interactive dashboard development
- **Git & GitHub** – Version control

## Project Workflow

1. Dataset Understanding
2. Exploratory Data Analysis (EDA)
3. Data Cleaning & Preparation
4. Customer Churn Analysis using SQL
5. Data Visualization using Matplotlib
6. Interactive Power BI Dashboard Development
7. Data Validation & Database Loading

## Key Insights

- Overall customer churn rate was approximately **26.54%**.
- Month-to-month customers had the highest churn rate of **42.71%**.
- Customers with two-year contracts had a significantly lower churn rate of **2.83%**.
- Customers with shorter tenure were more likely to churn.
- Higher monthly charges were associated with higher churn.
- Customers with month-to-month contracts and high monthly charges formed a high-risk segment, with a churn rate of **52.33%**.

## Data Validation & Database Loading

Python scripts were developed to validate datasets and support database loading.

### Features

- **48 automated validation checks**
- Data type validation
- Missing value checks
- Duplicate record detection
- Categorical value validation
- Numerical range validation
- MySQL database connection configuration using environment variables
- Data loading and handling of new and existing records
- Logging of validation and processing activities

The validation and data loading components were tested using valid and invalid datasets to evaluate data quality and loading behavior.

## Dashboard & Database Integration

The Power BI dashboard provides an interactive overview of customer churn and enables exploration of customer segments using different metrics and filters.

The dashboard is connected to MySQL as its data source.

## Dashboard Preview

![Customer Churn Dashboard](images/customer_churn_analysis_dashboard_screenshot.png)

## Project Structure

```text
Customer-Churn-Analysis/
├── dashboard/
├── data/
├── images/
├── notebooks/
├── reports/
├── scripts/
├── sql/
└── README.md
```

## Data Source

**IBM Telco Customer Churn Dataset**

The dataset contains customer information, service subscriptions, account details, and churn status.

- **Total Records:** 7,043 customers
- **Total Columns:** 21
- **Target Variable:** `Churn`

## Requirements

- Python 3.x
- MySQL Server
- Power BI Desktop
- Git

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Customer-Churn-Analysis
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database Credentials

- Install and start MySQL Server.
- Configure the project database.
- Create a `.env` file in the project root.
- Add your database credentials to the `.env` file.

Database credentials are excluded from version control using `.gitignore`.

### 4. Explore the Project

- Explore the notebooks in the `notebooks/` folder.
- Review SQL queries in the `sql/` folder.
- Explore Python scripts in the `scripts/` folder.
- Open the Power BI dashboard in the `dashboard/` folder.

## Conclusion

This project demonstrates practical data analytics skills through customer churn analysis, data cleaning, SQL querying, data visualization, dashboard development, and data validation.

The analysis highlights customer segments associated with higher churn and provides insights that can support data-driven customer retention strategies.