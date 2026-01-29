# PAMS System Understanding Notes  

## User Roles

- Front Desk Staff:  
  Responsible for registering new tenants, managing tenant details, handling tenant inquiries, submitting complaints on behalf of tenants, and logging maintenance requests. Front desk staff interact mainly with Tenant, Lease, Complaint, and Maintenance Request entities.

- Finance Manager:  
  Responsible for managing invoices, monitoring payments, handling late payments, generating financial alerts, and reviewing payment histories. This role primarily interacts with Invoice and Payment entities.

- Maintenance Staff:  
  Responsible for handling maintenance requests, updating maintenance status, recording time taken and costs, and resolving issues. This role interacts with Maintenance Request and Apartment entities.

- Administrator:  
  Has full access to the system within a specific location. Administrators manage user accounts, apartments, leases, and reports, and oversee overall system operations. This role interacts with almost all system components.

- Manager:  
  Oversees apartment occupancy across locations, monitors performance, reviews reports, and supports business expansion into new cities. This role focuses on reporting, occupancy, and high-level system insights.

---

## Core System Components

- Account/User Management  
  Handles authentication, login, password management, and role-based access control through the User and Staff classes.

- Tenant Management  
  Manages tenant records, personal details, lease information, complaints, and payment history.

- Apartment Management  
  Handles property and apartment details, unit registration, occupancy tracking, and apartment status updates.

- Payment & Billing  
  Manages invoices, rent payments, late payment detection, fee recording, and payment status tracking.

- Maintenance Management  
  Manages maintenance requests, prioritisation, assignment of staff, resolution tracking, time taken, and cost logging.

- Reporting & Analytics  
  Generates operational insights such as occupancy rates, financial summaries, late payment alerts, and maintenance cost tracking.

---

## Key Entities and Responsibilities

### User
- Stores login credentials and authentication data  
- Supports role-based login functionality  
- Tracks last login date and access permissions  

### Staff
- Stores staff details such as role, contact information, and employee ID  
- Can add tenants, generate invoices, resolve complaints, and assign maintenance staff  

### Tenant
- Stores tenant personal details including name, contact details, occupation, and move-in date  
- Linked to lease information, payment history, complaints, and maintenance requests  
- Can submit complaints, make payments, and request repairs  

### Lease
- Stores lease duration, rent amount, deposit, and lease status  
- Determines whether a lease is active or expired  
- Supports lease termination and renewal logic  

### Property
- Stores property-level details such as name, address, number of units, and year built  
- Calculates occupancy rates and tracks vacant units  

### Apartment
- Stores apartment-specific details including unit number, rent, bedrooms, status, and size  
- Tracks tenant assignment and availability  

### Invoice
- Stores billing information such as issue date, due date, total amount, and payment status  
- Sends late payment alerts and marks invoices as paid  

### Payment
- Stores payment amount, date, method, and status  
- Determines whether a payment is late and records late fees  

### Complaint
- Stores tenant complaints, submission details, status, and resolution notes  
- Supports tenant notifications after resolution  

### Maintenance Request
- Stores issue description, priority, submission date, resolution details, time taken, and associated costs  
- Tracks maintenance lifecycle from submission to resolution  

---

## Notes

- The system is implemented as a desktop-based application.  
- Role-based access control is mandatory to protect sensitive tenant and financial data.  
- All system data must be persistent and stored in a database.  
- The system is designed to support multi-location property management.  
