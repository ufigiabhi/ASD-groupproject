# PAMS - Paragon Apartment Management System

## How to Run

```bash
python main.py
```

---

## First-Time Setup (everyone needs to do this once)

### 1. Install Python dependencies

```bash
pip install mysql-connector-python matplotlib
```

### 2. Set up MySQL

Open MySQL Workbench and create a connection with these settings:

- Hostname: `127.0.0.1`
- Port: `3306`
- Username: `root`

### 3. Check your password in db.py

Open `backend/database/db.py` and make sure the password matches your MySQL root password.

### 4. Set up the database (choose one option)

#### **Option A - Python script (easiest, recommended)**

```bash
python -m backend.database.setup_db
```

This automatically creates the `asd_project` database, all 9 tables, and fills them with mock data.

#### **Option B - Import SQL dump via MySQL Workbench**

1. Open MySQL Workbench and connect  
2. Click **Server → Data Import**  
3. Select **Import from Self-Contained File** and choose `Dump_PAMS_latest.sql`  
4. Click **New** and name the schema `asd_project`  
5. Ensure **Dump Structure and Data** is selected  
6. Click **Start Import** and refresh  

---

## Login Credentials

| Role        | Username    | Password     |
|-------------|-------------|--------------|
| Admin       | admin1      | Admin@123    |
| Manager     | manager1    | Manager@123  |
| Front Desk  | frontdesk1  | Front@123    |
| Finance     | finance1    | Finance@123  |
| Maintenance | maint1      | Maint@123    |
| Tenant      | tenant1     | Tenant@123   |
| Tenant      | tenant2     | Tenant@123   |
| Tenant      | tenant3     | Tenant@123   |

---

## What Each Role Can Do

**Admin** - Manage user accounts, update apartments, track leases (including expiry alerts), view city-level reports.

**Manager** - Multi-city occupancy charts, financial reports, maintenance cost reports, add new properties/cities.

**Front Desk** - Register new tenants (NI number, occupation, references, lease period, start month/year), view tenants, log maintenance requests & complaints.

**Finance** - View financial overview, browse invoices/payments, record rent payments (auto-receipt), view overdue alerts.

**Maintenance** - View open requests by priority, assign staff, mark resolved with time & cost logged.

**Tenant** - View personal details and lease info, payment history with filters, submit maintenance requests & complaints, request early lease termination (1-month notice, 5% penalty).

---

## Running Tests

```bash
python -m unittest backend.tests.test_models -v
```

36 unit tests covering all model classes and input validation.

---

## Project Structure

| Path / File | Description |
|------------|-------------|
| **main.py** | Entry point of the application |
| **backend/database/db.py** | MySQL connection (update password here) |
| **backend/database/setup_db.py** | One-time DB setup + mock data insertion |
| **backend/models/** | OOP model classes |
| **backend/services/** | Business logic layer |
| **backend/tests/test_models.py** | 36 automated unit tests |
| **frontend/login.py** | Login screen (all 6 user roles) |
| **frontend/Front_Desk_dashboard.py** | Front Desk dashboard |
| **frontend/Finance.py** | Finance Manager dashboard |
| **frontend/maintenance_dashboard.py** | Maintenance Staff dashboard |
| **frontend/admin_dashboard.py** | Administrator dashboard |
| **frontend/manager_dashboard.py** | Manager dashboard |
| **frontend/tenant_dashboard.py** | Tenant portal |
| **database_setup.sql** | SQL schema reference |
| **Dump_PAMS_latest.sql** | Full database dump with mock data |
| **requirements.txt** | Python dependencies |
````
