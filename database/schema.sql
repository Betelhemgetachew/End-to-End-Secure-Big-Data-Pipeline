-- ============================================================
-- End-to-End Secure Big Data Pipeline
-- Database Schema
-- ============================================================

-- ============================================================
-- Table: uploads
-- Stores information about every uploaded CSV file.
-- ============================================================

CREATE TABLE uploads (
    upload_id SERIAL PRIMARY KEY,
    batch_id VARCHAR(50) UNIQUE NOT NULL,
    filename VARCHAR(255) NOT NULL,
    uploaded_by VARCHAR(100) NOT NULL,
    file_hash CHAR(64) NOT NULL,
    upload_status VARCHAR(20)
        CHECK (upload_status IN ('SUCCESS', 'FAILED'))
        NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Table: customers
-- Stores customer records imported from uploaded CSV files.
-- ============================================================

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,

    upload_id INTEGER NOT NULL,

    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,

    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    national_id VARCHAR(30),

    city VARCHAR(100),

    account_number VARCHAR(20) UNIQUE NOT NULL,

    account_type VARCHAR(20)
        CHECK (account_type IN ('standard', 'premium', 'business'))
        DEFAULT 'standard',

    account_balance DECIMAL(12,2)
        CHECK (account_balance >= 0),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer_upload
        FOREIGN KEY (upload_id)
        REFERENCES uploads(upload_id)
);

-- ============================================================
-- Table: audit_logs
-- Records normal security-related activities.
-- ============================================================

CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,

    username VARCHAR(100) NOT NULL,

    action VARCHAR(255) NOT NULL,

    status VARCHAR(20)
        CHECK (status IN ('SUCCESS', 'FAILED')),

    ip_address VARCHAR(45),

    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Table: security_events
-- Records detected security incidents.
-- ============================================================

CREATE TABLE security_events (
    event_id SERIAL PRIMARY KEY,

    upload_id INTEGER,

    event_type VARCHAR(100) NOT NULL,

    severity VARCHAR(20)
        CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),

    description TEXT,

    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_security_upload
        FOREIGN KEY (upload_id)
        REFERENCES uploads(upload_id)
);