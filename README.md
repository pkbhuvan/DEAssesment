# DEAssesment
#

## Overview

This project is an end-to-end ETL (Extract, Transform, Load) pipeline developed as part of the Data Engineering Assessment.

The pipeline ingests patient membership and claim files from multiple insurance clients, performs data validation and cleansing, transforms the data into a standardized format, joins membership and claims information, derives business metrics, and prepares the data for loading into a PostgreSQL database.

---

## Project Structure


DEAssessment/
│
├── data/
│   └── raw/
│       ├── Patient-membership-clientA-202301.xlsx
│       ├── Patient-membership-clientA-202302.xlsx
│       ├── Patient-membership-clientA-202307.xlsx
│       ├── Patient-claim-clientA-202301.xlsx
│       ├── Patient-claim-clientA-202302.xlsx
│       └── Patient-claim-clientA-202307.xlsx
│
├── src/
│
│   │   ├── validation/
│   │   ├── claim_validation.py
│   │   ├── date_validation.py
│   │   ├── duplicate_validation.py
│   │   ├── gender_validation.py
│   │   ├── membership_date_validation.py
│   │   ├── missing_value_validation.py
│   │   ├── phone_validation.py
│   │   └── zip_validation.py
│   │
│   ├── transformation/
│   │   ├── diagnosis.py
│   │   ├── join_data.py
│   │   └── metrics.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── load_data.py
│   │   └── schema.sql
│   │
│   └── utils/
│       ├── file_reader.py
│       └── logger.py
│
├── tests/
│
├── main.py
├── requirements.txt
└── README.md


---

# Features

The ETL pipeline performs the following tasks:

- Reads multiple membership files.
- Reads multiple claim files.
- Standardizes column names.
- Converts date columns to datetime format.
- Removes duplicate membership records.
- Validates membership dates.
- Validates phone numbers.
- Removes invalid claim records.
- Joins membership and claims using `member_id`.
- Calculates business metrics.
- Categorizes diagnosis types.
- Generates logs for each ETL step.
- Supports loading processed data into PostgreSQL.

---

# Data Validation

The following validations are implemented:

- Duplicate Member Validation
- Membership Date Validation
- Phone Number Validation
- Claim Number Validation
- Date Conversion
- Missing Value Validation
- Gender Validation
- ZIP Code Validation

---

# Business Transformations

The project derives the following information:

- Membership Status
- Diagnosis Category
- Claim Payment Amount
- Member Claim History

---

# Technologies Used

- Python 3.12
- Pandas
- SQLAlchemy
- PostgreSQL
- OpenPyXL
- Logging
- Pytest

---

# Installation

Clone the repository.

bash
git clone <repository-url>

cd DEAssessment


Install dependencies.

bash
pip install -r requirements.txt


---

# Running the ETL Pipeline

Execute the following command:

bash
python main.py


---

# PostgreSQL Configuration

Update the database connection in:


src/database/connection.py


Example:

python
DATABASE_URL = "postgresql://username:password@localhost:5432/"


If PostgreSQL is unavailable, the loading can be skipped by setting SKIP_DB_LOAD = True in src/database/load_data.py.
Change the value to False and ensure PostgreSQL is running and the connection settings are configured correctly.

---

# Running Unit Tests

Execute:

bash
pytest


or

bash
pytest tests/


---

# Logging

Logs are generated during each ETL step to provide visibility into:

- File reading
- Validation
- Transformation
- Data loading
- Exceptions

---

# Assumptions

- Member ID uniquely identifies a patient.
- Claim Number uniquely identifies a claim.
- Membership records retain the latest membership information after duplicate removal.
- Files are stored under the `data/raw` directory.
- Client-specific parsing can be extended by implementing additional parser classes.

---

# Future Improvements

- Add Docker support.
- Add CI/CD pipeline.
- Improve database indexing.
- Increase unit test coverage.

---

# Author

Prepared by:
Kalyan Bhuvanesh
