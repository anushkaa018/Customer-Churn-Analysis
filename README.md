Customer Churn & Retention Analysis

A data analytics project focused on understanding customer churn, identifying high-risk customer segments, and exploring strategies to improve customer retention.

Project Overview

This project analyzes customer churn data to identify patterns behind customer cancellations and understand which customer segments are more likely to churn.

The project follows a data analytics workflow using Python, MySQL, and Power BI, covering data exploration, cleaning, SQL analysis, visualization, dashboard development, and data validation.

Business Objectives

Identify key factors contributing to customer churn.

Analyze churn across different customer segments.

Identify high-risk customer groups.

Understand the relationship between tenure, contract type, and monthly charges with churn.

Provide data-driven insights to support customer retention strategies.

Tools & Technologies

Python – Data analysis and automation

Pandas – Data manipulation and analysis

Matplotlib – Data visualization

MySQL – Database storage and SQL analysis

Power BI – Interactive dashboard development

Git & GitHub – Version control and project management

Project Workflow

Dataset Understanding

Data Exploration using Python & Pandas

Data Cleaning

SQL Analysis using MySQL

Customer Analysis & Visualization using Matplotlib

Interactive Power BI Dashboard connected to MySQL

Data Validation & Database Loading

Key Insights

Overall customer churn rate was approximately 26.54%.

Month-to-month customers had the highest churn rate of 42.71%.

Customers with two-year contracts had a significantly lower churn rate of 2.83%.

Customers with shorter tenure were more likely to churn.

Higher monthly charges were associated with higher churn.

Customers with month-to-month contracts and high monthly charges formed a high-risk segment, with a churn rate of 52.33%.

Data Validation & Database Loading

Python scripts were developed for data validation and database loading.

Implemented Components

48 automated validation checks

Validation of data types, missing values, duplicate records, categorical values, and numerical ranges

MySQL database connection using environment variables

Data loading functionality for MySQL

Handling of new records

Updating existing records without creating duplicates

Validation of datasets before loading through the Python workflow

Logging of validation results and loading activities

The validation and database loading components were tested using valid and invalid datasets to verify insertion, updating, and rejection behavior.

A complete end-to-end automated pipeline connecting the entire workflow is currently under development.

## Dashboard & Database Integration

The Power BI dashboard is connected directly to **MySQL**, using the database as its data source instead of CSV files.

The project demonstrates integration between Python, MySQL, and Power BI in an end-to-end data analytics workflow.

## Dashboard Preview

The interactive Power BI dashboard allows users to explore customer churn patterns and analyze customer segments using different metrics and filters.

![Customer Churn Dashboard](images/customer_churn_analysis_dashboard_screenshot.png)

## Project Structure

```text
Customer-churn-analysis/
├── automation/
├── dashboard/
├── data/
├── images/
├── notebooks/
├── reports/
├── sql/
└── README.md
```

## Data Source

The project uses the **IBM Telco Customer Churn dataset**, containing customer information, services, account details, and churn status.

- **Total records:** 7,043 customers
- **Total columns:** 21
- **Target variable:** `Churn`

## Requirements

- Python 3.x
- MySQL Server
- Power BI Desktop
- Git

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Customer-churn-analysis
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MySQL

- Install and start MySQL Server.
- Create the project database.
- Create a `.env` file in the project root directory.
- Add your MySQL credentials to the `.env` file.
- The `.env` file is excluded from Git using `.gitignore` to protect sensitive credentials.

### 4. Run the Project

- Explore the notebooks in the `notebooks/` folder.
- Execute SQL queries from the `sql/` folder.
- Run the automation scripts from the `automation/` folder.
- Open the Power BI dashboard from the `dashboard/` folder.

## Conclusion

This project demonstrates an end-to-end data analytics workflow, from data exploration and cleaning to SQL analysis, visualization, dashboard development, and data pipeline automation.

The analysis identified key customer segments associated with higher churn and provided data-driven insights that can support customer retention strategies.

