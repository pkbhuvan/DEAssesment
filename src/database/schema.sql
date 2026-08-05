CREATE TABLE IF NOT EXISTS members (
    member_id VARCHAR PRIMARY KEY,
    first_name VARCHAR,
    middle_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,
    date_of_birth DATE,
    address VARCHAR,
    city VARCHAR,
    state VARCHAR,
    zip_code VARCHAR,
    phone_number VARCHAR,
    membership_end_date DATE,
    ethnicity VARCHAR
);

CREATE TABLE IF NOT EXISTS claims (
    claim_number VARCHAR PRIMARY KEY,
    member_id VARCHAR,
    date_received DATE,
    hospital_service VARCHAR,
    code_system VARCHAR,
    cost_total NUMERIC,
    status VARCHAR
);

CREATE TABLE IF NOT EXISTS member_claims (
    claim_number VARCHAR PRIMARY KEY,
    member_id VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,
    date_of_birth DATE,
    membership_end_date DATE,
    hospital_service VARCHAR,
    code_system VARCHAR,
    cost_total NUMERIC,
    status VARCHAR
);
