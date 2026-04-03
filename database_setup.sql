-- ============================================================
-- PAMS - Paragon Apartment Management System
-- Complete Database Schema
-- Run this file in MySQL to set up all tables
-- Then run: python backend/database/setup_db.py
--   to populate mock data with correct password hashes
-- ============================================================

CREATE DATABASE IF NOT EXISTS asd_project;
USE asd_project;

-- Disable FK checks for clean drop/recreate
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS leases;
DROP TABLE IF EXISTS maintenance_requests;
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS tenants;
DROP TABLE IF EXISTS apartments;
DROP TABLE IF EXISTS properties;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- USERS TABLE (all staff + tenant accounts)
-- ============================================================
CREATE TABLE users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  UNIQUE NOT NULL,
    password_hash VARCHAR(64)  NOT NULL,
    role          ENUM('Admin','Manager','FrontDesk','Finance','Maintenance','Tenant') NOT NULL,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(100) NOT NULL,
    phone         VARCHAR(20),
    location      VARCHAR(50),
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login    DATETIME
);

-- ============================================================
-- PROPERTIES TABLE (multi-city offices)
-- ============================================================
CREATE TABLE properties (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    address      VARCHAR(200) NOT NULL,
    city         ENUM('Bristol','Cardiff','London','Manchester') NOT NULL,
    postcode     VARCHAR(10)  NOT NULL,
    total_units  INT          NOT NULL,
    year_built   YEAR
);

-- ============================================================
-- APARTMENTS TABLE
-- ============================================================
CREATE TABLE apartments (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    property_id    INT          NOT NULL,
    unit_number    VARCHAR(20)  NOT NULL,
    floor          INT          DEFAULT 0,
    bedrooms       INT          NOT NULL,
    bathrooms      INT          NOT NULL DEFAULT 1,
    size_sqm       FLOAT,
    monthly_rent   DECIMAL(10,2) NOT NULL,
    apartment_type VARCHAR(50),
    status         ENUM('available','occupied','maintenance') DEFAULT 'available',
    FOREIGN KEY (property_id) REFERENCES properties(id)
);

-- ============================================================
-- TENANTS TABLE (expanded with all required fields)
-- ============================================================
CREATE TABLE tenants (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT,
    name                VARCHAR(100) NOT NULL,
    ni_number           VARCHAR(20)  UNIQUE NOT NULL,
    phone               VARCHAR(20)  NOT NULL,
    email               VARCHAR(100) NOT NULL,
    occupation          VARCHAR(100),
    reference1          VARCHAR(200),
    reference2          VARCHAR(200),
    apartment_type      VARCHAR(50),
    lease_period_months INT,
    registered_date     DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================================================
-- LEASES TABLE
-- ============================================================
CREATE TABLE leases (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id             INT          NOT NULL,
    apartment_id          INT          NOT NULL,
    start_date            DATE         NOT NULL,
    end_date              DATE         NOT NULL,
    monthly_rent          DECIMAL(10,2) NOT NULL,
    deposit_amount        DECIMAL(10,2) NOT NULL,
    status                ENUM('active','expired','terminated') DEFAULT 'active',
    notice_given_date     DATE,
    early_termination_fee DECIMAL(10,2),
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id)    REFERENCES tenants(id),
    FOREIGN KEY (apartment_id) REFERENCES apartments(id)
);

-- ============================================================
-- INVOICES TABLE
-- ============================================================
CREATE TABLE invoices (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id   INT           NOT NULL,
    lease_id    INT,
    amount      DECIMAL(10,2) NOT NULL,
    issue_date  DATE          NOT NULL,
    due_date    DATE          NOT NULL,
    month       INT           NOT NULL CHECK (month BETWEEN 1 AND 12),
    year        INT           NOT NULL,
    status      ENUM('unpaid','paid','overdue','partial') DEFAULT 'unpaid',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    FOREIGN KEY (lease_id)  REFERENCES leases(id)
);

-- ============================================================
-- PAYMENTS TABLE
-- ============================================================
CREATE TABLE payments (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id     INT           NOT NULL,
    tenant_id      INT           NOT NULL,
    amount         DECIMAL(10,2) NOT NULL,
    payment_date   DATETIME DEFAULT CURRENT_TIMESTAMP,
    method         ENUM('Card','Bank Transfer','Cash') NOT NULL,
    status         ENUM('completed','pending','failed') DEFAULT 'completed',
    late_fee       DECIMAL(10,2) DEFAULT 0.00,
    receipt_number VARCHAR(50)   UNIQUE NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id),
    FOREIGN KEY (tenant_id)  REFERENCES tenants(id)
);

-- ============================================================
-- MAINTENANCE REQUESTS TABLE (updated)
-- ============================================================
CREATE TABLE maintenance_requests (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    apartment_id    INT          NOT NULL,
    tenant_id       INT,
    description     TEXT         NOT NULL,
    priority        ENUM('Low','Medium','High','Emergency') NOT NULL DEFAULT 'Medium',
    status          ENUM('OPEN','IN_PROGRESS','RESOLVED','CLOSED') NOT NULL DEFAULT 'OPEN',
    submission_date DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    scheduled_date  DATETIME,
    resolution_date DATETIME,
    time_taken      FLOAT,
    cost            DECIMAL(10,2),
    assigned_staff  VARCHAR(100),
    notes           TEXT,
    FOREIGN KEY (apartment_id) REFERENCES apartments(id),
    FOREIGN KEY (tenant_id)    REFERENCES tenants(id)
);

-- ============================================================
-- COMPLAINTS TABLE (updated)
-- ============================================================
CREATE TABLE complaints (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id       INT,
    tenant_name     VARCHAR(100) NOT NULL,
    issue           TEXT         NOT NULL,
    category        ENUM('Noise','Repair','Neighbour','Billing','Other') DEFAULT 'Other',
    status          ENUM('Open','Investigating','Resolved','Closed') DEFAULT 'Open',
    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolution_date DATETIME,
    resolution_notes TEXT,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);
