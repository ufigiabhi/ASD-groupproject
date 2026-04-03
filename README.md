bash - to run app
python -m frontend.login

STEPS FOR BACKEND TO WORK

-Make sure you download the SQL file Esila gave on the whatsapp group the name of the file should be "Dump20260302"
-First open MY SQL Workbench, add a new connection and have the connection name to whatever you want, the hostname should be "127.0.0.1" Port should be "3306" and Username should be "root" and then just click "ok" to make the new connection. Once you are in the connection click "Server" and then select "Data Import".
-In the data import select the "Import from Self-Contained file" and then select the "Dump20260302" that you previously downloaded and then click "New" and just name it like "asd_project".
-Now make sure "Dump Structure and Data" is selected out of the 3 options and then click start Import and then refresh your MY SQL Connection.
-You should have the Schema imported now which you can see on the right side bar of the MY SQL Workbench.
-Open our ASD-GroupProject folder and go to the file "backend/database/db.py" in the db.py file make sure to change the host, password or database if you need to.

NEW VERSION!!!!!!!!!!!
  How to Run

  python main.py

  ---
  First-Time Setup (everyone needs to do this once)

  1. Install Python dependencies

  pip install mysql-connector-python matplotlib

  2. Set up MySQL

  Open MySQL Workbench and create a connection with these settings:
  - Hostname: 127.0.0.1
  - Port: 3306
  - Username: root

  3. Check your password in db.py

  Open backend/database/db.py and make sure the password matches your MySQL root password. Change it if needed.

  4. Set up the database (choose one option)

  Option A - Python script (easiest, recommended):

  Open a terminal in the project folder and run:
  python -m backend.database.setup_db
  This automatically creates the asd_project database, all 9 tables, and fills them with mock data.

  Option B - Import the SQL dump via MySQL Workbench:

  1. Open MySQL Workbench and connect
  2. Click Server then Data Import
  3. Select Import from Self-Contained File and choose Dump_PAMS_latest.sql from the project folder
  4. Click New and name the schema asd_project
  5. Make sure Dump Structure and Data is selected
  6. Click Start Import then refresh

  ---
  Login Credentials
<img width="299" height="407" alt="image" src="https://github.com/user-attachments/assets/06f056cf-c7fe-4fae-9b24-4f51f7a47a53" />


  ---
  What Each Role Can Do

  Admin - Manage user accounts, view/update apartments, track all leases including expiry alerts, view reports for their city

  Manager - Multi-city occupancy charts, financial reports, maintenance cost reports, expand business by adding new properties/cities

  Front Desk - Register new tenants (all fields: NI number, occupation, references, lease period dropdown, start month/year dropdown), view tenants, log
  maintenance requests and complaints

  Finance - View financial overview with month/year filters, browse invoices and payments, record rent payments (generates receipt), view overdue alerts

  Maintenance - View open requests ordered by priority, assign staff, mark resolved with time and cost logged

  Tenant - View personal details and lease info, payment history with month/year filter, submit maintenance requests and complaints, request early lease
  termination (1 month notice, 5% penalty)

  ---
  Running Tests

  python -m unittest backend.tests.test_models -v

  36 unit tests covering all model classes and input validation.

  ---
  Project Structure

  main.py                          - Entry point
  backend/
    database/
      db.py                        - MySQL connection (change password here)
      setup_db.py                  - One-time DB setup and mock data
    models/                        - OOP model classes
    services/                      - Business logic layer
    tests/
      test_models.py               - 36 automated unit tests
  frontend/
    login.py                       - Login screen (all 6 roles)
    Front_Desk_dashboard.py        - Front Desk panel
    Finance.py                     - Finance Manager panel
    maintenance_dashboard.py       - Maintenance Staff panel
    admin_dashboard.py             - Administrator panel
    manager_dashboard.py           - Manager panel
    tenant_dashboard.py            - Tenant portal
  database_setup.sql               - SQL schema reference
  Dump_PAMS_latest.sql             - Full database dump with mock data
  requirements.txt                 - Python dependencies
  HOW_TO_RUN.txt                   - Detailed instructions
