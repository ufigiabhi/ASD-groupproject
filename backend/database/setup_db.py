"""
PAMS - Database Setup Script
Run this once to create all tables and populate mock data.
Usage:  python -m backend.database.setup_db
"""

import hashlib
from datetime import datetime, date, timedelta
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "314159Pi.com",
}

DB_NAME = "asd_project"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_conn(with_db=True):
     """
    Create and return a database connection.
    If with_db=False, connect without selecting a database.
    """
    cfg = dict(DB_CONFIG)
    if with_db:
        cfg["database"] = DB_NAME
    return mysql.connector.connect(**cfg)


def create_database():
    conn = get_conn(with_db=False)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    cur.close()
    conn.close()
    print(f"[OK] Database '{DB_NAME}' ready.")


def create_tables():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SET FOREIGN_KEY_CHECKS = 0")

    tables = [
        "payments", "invoices", "leases",
        "maintenance_requests", "complaints",
        "tenants", "apartments", "properties", "users"
    ]
    for t in tables:
        cur.execute(f"DROP TABLE IF EXISTS `{t}`")

    cur.execute("SET FOREIGN_KEY_CHECKS = 1")

    cur.execute("""
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
        )
    """)

    cur.execute("""
        CREATE TABLE properties (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            name        VARCHAR(100) NOT NULL,
            address     VARCHAR(200) NOT NULL,
            city        ENUM('Bristol','Cardiff','London','Manchester') NOT NULL,
            postcode    VARCHAR(10)  NOT NULL,
            total_units INT          NOT NULL,
            year_built  YEAR
        )
    """)

    cur.execute("""
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
        )
    """)

    cur.execute("""
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
        )
    """)

    cur.execute("""
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
        )
    """)

    cur.execute("""
        CREATE TABLE invoices (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id   INT           NOT NULL,
            lease_id    INT,
            amount      DECIMAL(10,2) NOT NULL,
            issue_date  DATE          NOT NULL,
            due_date    DATE          NOT NULL,
            month       INT           NOT NULL,
            year        INT           NOT NULL,
            status      ENUM('unpaid','paid','overdue','partial') DEFAULT 'unpaid',
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id),
            FOREIGN KEY (lease_id)  REFERENCES leases(id)
        )
    """)

    cur.execute("""
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
        )
    """)

    cur.execute("""
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
        )
    """)

    cur.execute("""
        CREATE TABLE complaints (
            id               INT AUTO_INCREMENT PRIMARY KEY,
            tenant_id        INT,
            tenant_name      VARCHAR(100) NOT NULL,
            issue            TEXT         NOT NULL,
            category         ENUM('Noise','Repair','Neighbour','Billing','Other') DEFAULT 'Other',
            status           ENUM('Open','Investigating','Resolved','Closed') DEFAULT 'Open',
            submission_date  DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolution_date  DATETIME,
            resolution_notes TEXT,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("[OK] All tables created.")


def insert_mock_data():
    conn = get_conn()
    cur = conn.cursor()

    # ---- USERS ----
    users = [
        ("admin1",    hash_password("Admin@123"),    "Admin",       "Alice Admin",    "alice@paragon.com",   "07700900001", "Bristol"),
        ("manager1",  hash_password("Manager@123"),  "Manager",     "Mark Manager",   "mark@paragon.com",    "07700900002", None),
        ("frontdesk1",hash_password("Front@123"),    "FrontDesk",   "Fiona Desk",     "fiona@paragon.com",   "07700900003", "Bristol"),
        ("finance1",  hash_password("Finance@123"),  "Finance",     "Frank Finance",  "frank@paragon.com",   "07700900004", "Bristol"),
        ("maint1",    hash_password("Maint@123"),    "Maintenance", "Mike Maint",     "mike@paragon.com",    "07700900005", "Bristol"),
        ("frontdesk2",hash_password("Front@123"),    "FrontDesk",   "Greg Desk",      "greg@paragon.com",    "07700900006", "Cardiff"),
        ("admin2",    hash_password("Admin@123"),    "Admin",       "Bob Admin",      "bob@paragon.com",     "07700900007", "London"),
        ("tenant1",   hash_password("Tenant@123"),   "Tenant",      "John Smith",     "john.s@email.com",    "07700900008", None),
        ("tenant2",   hash_password("Tenant@123"),   "Tenant",      "Sarah Jones",    "sarah.j@email.com",   "07700900009", None),
        ("tenant3",   hash_password("Tenant@123"),   "Tenant",      "David Brown",    "david.b@email.com",   "07700900010", None),
    ]
    cur.executemany("""
        INSERT INTO users (username, password_hash, role, full_name, email, phone, location)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, users)

    # ---- PROPERTIES ----
    properties = [
        ("Paragon Bristol",    "15 Queen Square",       "Bristol",    "BS1 4NT", 12, 2008),
        ("Paragon Cardiff",    "22 Cardiff Bay Road",   "Cardiff",    "CF10 5BT", 8, 2012),
        ("Paragon London",     "10 Canary Wharf Lane",  "London",     "E14 5AB", 20, 2015),
        ("Paragon Manchester", "5 Spinningfields Ave",  "Manchester", "M3 3AP",  10, 2018),
    ]
    cur.executemany("""
        INSERT INTO properties (name, address, city, postcode, total_units, year_built)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, properties)

    # ---- APARTMENTS ----
    apartments = [
        # Bristol (property 1)
        (1, "101", 1, 1, 1, 45.0,  950.00,  "Studio",    "occupied"),
        (1, "102", 1, 1, 1, 55.0,  1100.00, "1-Bedroom", "occupied"),
        (1, "201", 2, 2, 1, 70.0,  1400.00, "2-Bedroom", "occupied"),
        (1, "202", 2, 2, 2, 75.0,  1500.00, "2-Bedroom", "available"),
        (1, "301", 3, 3, 2, 95.0,  2000.00, "3-Bedroom", "available"),
        (1, "302", 3, 1, 1, 52.0,  1050.00, "1-Bedroom", "maintenance"),
        # Cardiff (property 2)
        (2, "101", 1, 1, 1, 42.0,   800.00, "Studio",    "available"),
        (2, "102", 1, 2, 1, 65.0,  1200.00, "2-Bedroom", "occupied"),
        (2, "201", 2, 2, 2, 78.0,  1350.00, "2-Bedroom", "available"),
        # London (property 3)
        (3, "101", 1, 1, 1, 40.0,  1800.00, "Studio",    "occupied"),
        (3, "102", 1, 2, 1, 62.0,  2500.00, "2-Bedroom", "available"),
        (3, "201", 2, 3, 2, 90.0,  3200.00, "3-Bedroom", "available"),
        # Manchester (property 4)
        (4, "101", 1, 1, 1, 44.0,   750.00, "Studio",    "available"),
        (4, "102", 1, 2, 1, 68.0,  1100.00, "2-Bedroom", "available"),
    ]
    cur.executemany("""
        INSERT INTO apartments
        (property_id, unit_number, floor, bedrooms, bathrooms, size_sqm,
         monthly_rent, apartment_type, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, apartments)

    # ---- TENANTS ----
    tenants = [
        # user_id 8 = tenant1 (John Smith)
        (8,  "John Smith",  "AB123456A", "07700900008", "john.s@email.com",
         "Software Engineer", "Dr. Peter Hall, UWE Bristol", "Ms. Carol White",
         "2-Bedroom", 12),
        # user_id 9 = tenant2 (Sarah Jones)
        (9,  "Sarah Jones", "CD789012B", "07700900009", "sarah.j@email.com",
         "Nurse",            "Dr. Anna Green, NHS",          "Mr. Tom Black",
         "1-Bedroom", 12),
        # user_id 10 = tenant3 (David Brown)
        (10, "David Brown", "EF345678C", "07700900010", "david.b@email.com",
         "Teacher",          "Mrs. Jane Doe, Avon School",  "Mr. Paul Grey",
         "Studio", 6),
        # Extra tenant with no user account (walk-in registration)
        (None, "Emma Wilson", "GH901234D", "07700900011", "emma.w@email.com",
         "Accountant", "Mr. Raj Patel, KPMG", "Mrs. Sue Hill",
         "2-Bedroom", 24),
    ]
    cur.executemany("""
        INSERT INTO tenants
        (user_id, name, ni_number, phone, email, occupation,
         reference1, reference2, apartment_type, lease_period_months)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tenants)

    # ---- LEASES ----
    leases = [
        # tenant 1 → apt 3 (Bristol 201, 2-bed, £1400)
        (1, 3, "2025-04-01", "2026-04-01", 1400.00, 2800.00, "active",  None, None),
        # tenant 2 → apt 2 (Bristol 102, 1-bed, £1100)
        (2, 2, "2025-06-01", "2026-06-01", 1100.00, 2200.00, "active",  None, None),
        # tenant 3 -> apt 1 (Bristol 101, studio, £950) - 6-month lease
        (3, 1, "2025-10-01", "2026-04-01",  950.00, 1900.00, "active",  None, None),
        # tenant 4 → apt 8 (Cardiff 102, 2-bed, £1200)
        (4, 8, "2025-01-01", "2027-01-01", 1200.00, 2400.00, "active",  None, None),
        # expired lease example
        (1, 3, "2024-01-01", "2025-01-01", 1350.00, 2700.00, "expired", None, None),
    ]
    cur.executemany("""
        INSERT INTO leases
        (tenant_id, apartment_id, start_date, end_date,
         monthly_rent, deposit_amount, status, notice_given_date, early_termination_fee)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, leases)

    # ---- INVOICES (6 months of history) ----
    invoice_rows = []
    # Tenant 1, lease 1, £1400/month - Oct 2025 to Mar 2026
    months = [
        (10, 2025, "2025-10-01", "2025-10-28", "paid"),
        (11, 2025, "2025-11-01", "2025-11-28", "paid"),
        (12, 2025, "2025-12-01", "2025-12-28", "paid"),
        (1,  2026, "2026-01-01", "2026-01-28", "paid"),
        (2,  2026, "2026-02-01", "2026-02-28", "paid"),
        (3,  2026, "2026-03-01", "2026-03-28", "overdue"),
        (4,  2026, "2026-04-01", "2026-04-28", "unpaid"),
    ]
    for m, y, iss, due, st in months:
        invoice_rows.append((1, 1, 1400.00, iss, due, m, y, st))

    # Tenant 2, lease 2, £1100/month - Oct 2025 to Apr 2026
    t2_months = [
        (10, 2025, "2025-10-01", "2025-10-28", "paid"),
        (11, 2025, "2025-11-01", "2025-11-28", "paid"),
        (12, 2025, "2025-12-01", "2025-12-28", "paid"),
        (1,  2026, "2026-01-01", "2026-01-28", "paid"),
        (2,  2026, "2026-02-01", "2026-02-28", "overdue"),
        (3,  2026, "2026-03-01", "2026-03-28", "unpaid"),
    ]
    for m, y, iss, due, st in t2_months:
        invoice_rows.append((2, 2, 1100.00, iss, due, m, y, st))

    # Tenant 3, lease 3, £950/month - Oct 2025 to Mar 2026
    t3_months = [
        (10, 2025, "2025-10-01", "2025-10-28", "paid"),
        (11, 2025, "2025-11-01", "2025-11-28", "paid"),
        (12, 2025, "2025-12-01", "2025-12-28", "paid"),
        (1,  2026, "2026-01-01", "2026-01-28", "unpaid"),
    ]
    for m, y, iss, due, st in t3_months:
        invoice_rows.append((3, 3, 950.00, iss, due, m, y, st))

    cur.executemany("""
        INSERT INTO invoices
        (tenant_id, lease_id, amount, issue_date, due_date, month, year, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, invoice_rows)

    # ---- PAYMENTS (for paid invoices) ----
    payments = [
        # Tenant 1: invoices 1-5 paid
        (1, 1, 1400.00, "2025-10-05", "Card",          "completed", 0.00,  "RCP-00001"),
        (2, 1, 1400.00, "2025-11-04", "Bank Transfer",  "completed", 0.00,  "RCP-00002"),
        (3, 1, 1400.00, "2025-12-03", "Card",           "completed", 0.00,  "RCP-00003"),
        (4, 1, 1400.00, "2026-01-06", "Card",           "completed", 0.00,  "RCP-00004"),
        (5, 1, 1400.00, "2026-02-03", "Bank Transfer",  "completed", 0.00,  "RCP-00005"),
        # Tenant 2: invoices 8-11 paid (ids offset by 7)
        (8, 2,  1100.00, "2025-10-07", "Cash",          "completed", 0.00,  "RCP-00006"),
        (9, 2,  1100.00, "2025-11-05", "Card",          "completed", 0.00,  "RCP-00007"),
        (10,2,  1100.00, "2025-12-04", "Card",          "completed", 0.00,  "RCP-00008"),
        (11,2,  1100.00, "2026-01-07", "Bank Transfer", "completed", 0.00,  "RCP-00009"),
        # Tenant 3: invoices 14-16 paid (ids offset by 13)
        (14,3,   950.00, "2025-10-06", "Card",          "completed", 0.00,  "RCP-00010"),
        (15,3,   950.00, "2025-11-08", "Cash",          "completed", 0.00,  "RCP-00011"),
        (16,3,   950.00, "2025-12-06", "Card",          "completed", 0.00,  "RCP-00012"),
    ]
    cur.executemany("""
        INSERT INTO payments
        (invoice_id, tenant_id, amount, payment_date, method, status, late_fee, receipt_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, payments)

    # ---- MAINTENANCE REQUESTS ----
    maintenance = [
        (3, 1, "Leaking kitchen sink",    "High",      "RESOLVED",    "2025-11-10 09:00:00",
         None, "2025-11-11 14:00:00", 2.5, 180.00, "Mike Maint",   "Replaced washer"),
        (2, 2, "Broken window latch",     "Medium",    "RESOLVED",    "2025-12-05 11:00:00",
         None, "2025-12-07 10:00:00", 1.5,  90.00, "Mike Maint",   "Replaced latch"),
        (1, 3, "Boiler not heating",      "Emergency", "IN_PROGRESS", "2026-02-20 08:00:00",
         "2026-02-22 09:00:00", None, None, None,  "Mike Maint",   None),
        (3, 1, "Cracked bathroom tile",   "Low",       "OPEN",        "2026-03-01 15:00:00",
         None, None, None, None, None, None),
        (8, 4, "Washing machine fault",   "Medium",    "OPEN",        "2026-03-10 10:00:00",
         None, None, None, None, None, None),
        (10,None,"Lobby light flickering","Low",       "IN_PROGRESS", "2026-03-15 09:00:00",
         "2026-03-20 10:00:00", None, None, None, "Mike Maint",    None),
    ]
    cur.executemany("""
        INSERT INTO maintenance_requests
        (apartment_id, tenant_id, description, priority, status,
         submission_date, scheduled_date, resolution_date,
         time_taken, cost, assigned_staff, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, maintenance)

    # ---- COMPLAINTS ----
    complaints = [
        (1, "John Smith",  "Noise from upstairs flat after 11pm",   "Noise",   "Resolved",
         "2026-01-15 10:00:00", "2026-01-18 14:00:00", "Spoken to upstairs tenant. Resolved."),
        (2, "Sarah Jones", "Hot water not working for 3 days",       "Repair",  "Investigating",
         "2026-02-10 09:00:00", None, None),
        (3, "David Brown", "Billing charge appears incorrect",       "Billing", "Open",
         "2026-03-05 11:00:00", None, None),
        (4, "Emma Wilson", "Neighbour's dog barking constantly",     "Neighbour","Open",
         "2026-03-20 14:00:00", None, None),
    ]
    cur.executemany("""
        INSERT INTO complaints
        (tenant_id, tenant_name, issue, category, status,
         submission_date, resolution_date, resolution_notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, complaints)

    conn.commit()
    cur.close()
    conn.close()
    print("[OK] Mock data inserted.")
    print()
    print("=" * 50)
    print("  TEST LOGIN CREDENTIALS")
    print("=" * 50)
    print("  Role        | Username    | Password")
    print("  ------------|-------------|----------")
    print("  Admin       | admin1      | Admin@123")
    print("  Manager     | manager1    | Manager@123")
    print("  Front Desk  | frontdesk1  | Front@123")
    print("  Finance     | finance1    | Finance@123")
    print("  Maintenance | maint1      | Maint@123")
    print("  Tenant      | tenant1     | Tenant@123")
    print("  Tenant      | tenant2     | Tenant@123")
    print("  Tenant      | tenant3     | Tenant@123")
    print("=" * 50)


if __name__ == "__main__":
    create_database()
    create_tables()
    insert_mock_data()
    print("\n[DONE] Database setup complete.")
