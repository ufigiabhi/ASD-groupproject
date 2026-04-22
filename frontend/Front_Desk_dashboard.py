import tkinter as tk
from tkinter import messagebox, ttk

# Service layer imports used to handle database/business logic
from backend.services.maintenance_service import MaintenanceService
from backend.services.tenant_service import TenantService
from backend.services.complaint_service import ComplaintService
from backend.services.lease_service import LeaseService
from backend.services.apartment_service import ApartmentService

# UI colour constants for a consistent theme across the dashboard
PRIMARY = "#0d47a1"
ACCENT  = "#1976d2"
BG = "#f0f4f8"

# Dropdown options for registration form fields
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
YEARS  = [str(y) for y in range(2024, 2032)]
LEASE_PERIOD_OPTIONS = ["6", "12", "18", "24", "36"]
APT_TYPE_OPTIONS = ["Studio", "1-Bedroom", "2-Bedroom", "3-Bedroom", "4-Bedroom+"]


def open_frontdesk_dashboard(user: dict):
    # Display the full name if a user dictionary is passed in,
    # otherwise fall back to converting the value to a string
    username = user["full_name"] if isinstance(user, dict) else str(user)

    # Create service instances for each dashboard feature
    maintenance_service = MaintenanceService()
    tenant_service = TenantService()
    complaint_service   = ComplaintService()
    lease_service = LeaseService()
    apartment_service   = ApartmentService()

    # Main application window
    root = tk.Tk()
    root.title(f"Front Desk - {username}")
    root.geometry("1100x720")
    root.configure(bg=BG)

    # Header section with page title and logout button
    header = tk.Frame(root, bg=PRIMARY, height=52)
    header.pack(fill="x")
    tk.Label(header, text=f"Front Desk Dashboard - {username}",
             font=("Helvetica", 15, "bold"), bg=PRIMARY, fg="white"
             ).pack(side="left", padx=20, pady=10)

    def logout():
        # Return the user to the login page after confirming logout
        from frontend import login
        if messagebox.askyesno("Logout", "Are you sure?"):
            root.destroy()
            login.run_login()

    tk.Button(header, text="Logout", bg="#c62828", fg="white",
              font=("Helvetica", 10, "bold"), relief="flat",
              command=logout).pack(side="right", padx=15, pady=10)

    # Notebook widget used to separate dashboard features into tabs
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=10, pady=10)


    # TAB 1 - Register Tenant
    tab_reg = tk.Frame(nb, bg="white")
    nb.add(tab_reg, text="  Register Tenant  ")

    tk.Label(tab_reg, text="Register New Tenant",
             font=("Helvetica", 14, "bold"), bg="white", fg=PRIMARY
             ).grid(row=0, column=0, columnspan=4, pady=(15, 10), padx=20, sticky="w")

    # Form field definitions:
    # (label text, key used in widgets dict, widget type)
    fields_def = [
        ("Full Name *", "name", "entry"),
        ("NI Number *", "ni_number", "entry"),
        ("Phone *", "phone", "entry"),
        ("Email *", "email", "entry"),
        ("Occupation", "occupation", "entry"),
        ("Reference 1", "reference1", "entry"),
        ("Reference 2", "reference2", "entry"),
        ("Apartment Type *",   "apartment_type", "combo_apt"),
        ("Lease Period (months) *", "lease_period_months", "combo_lease"),
        ("Lease Start Month *","start_month", "combo_month"),
        ("Lease Start Year *", "start_year", "combo_year"),
        ("Monthly Rent (£) *", "monthly_rent", "entry"),
        ("Deposit (£) *", "deposit_amount", "entry"),
    ]

    # Store each input widget so values can be retrieved later
    widgets = {}

    # Dynamically create the registration form layout
    for idx, (label, key, wtype) in enumerate(fields_def):
        col = (idx % 2) * 2
        row = (idx // 2) + 1

        tk.Label(tab_reg, text=label, bg="white",
                 font=("Helvetica", 10)).grid(row=row, column=col,
                                              sticky="w", padx=(20 if col == 0 else 15, 5),
                                              pady=3)

        if wtype == "entry":
            w = tk.Entry(tab_reg, font=("Helvetica", 10), width=26)
        elif wtype == "combo_apt":
            w = ttk.Combobox(tab_reg, values=APT_TYPE_OPTIONS,
                             state="readonly", width=24)
            w.set(APT_TYPE_OPTIONS[0])
        elif wtype == "combo_lease":
            w = ttk.Combobox(tab_reg, values=LEASE_PERIOD_OPTIONS,
                             state="readonly", width=24)
            w.set("12")
        elif wtype == "combo_month":
            w = ttk.Combobox(tab_reg, values=MONTHS,
                             state="readonly", width=24)
            w.set(MONTHS[0])
        elif wtype == "combo_year":
            w = ttk.Combobox(tab_reg, values=YEARS,
                             state="readonly", width=24)
            w.set(YEARS[0])

        w.grid(row=row, column=col + 1, sticky="w",
               padx=(0, 20), pady=3)
        widgets[key] = w

    def _get(key):
        # Helper function to safely get trimmed values from form widgets
        w = widgets[key]
        return w.get().strip() if hasattr(w, "get") else ""

    def register_tenant():
        # Required fields must be completed before registration can proceed
        required = ["name", "ni_number", "phone", "email",
                    "apartment_type", "lease_period_months",
                    "start_month", "start_year",
                    "monthly_rent", "deposit_amount"]

        for k in required:
            if not _get(k):
                messagebox.showwarning("Missing Data", f"'{k}' is required.")
                return

        # Validate numeric fields before sending data to the service layer
        try:
            rent    = float(_get("monthly_rent"))
            deposit = float(_get("deposit_amount"))
            period  = int(_get("lease_period_months"))
        except ValueError:
            messagebox.showerror("Invalid Data", "Rent, deposit and lease period must be numbers.")
            return

        try:
            # Register the tenant first and get their generated tenant ID
            tenant_id = tenant_service.register_tenant(
                name=_get("name"),
                ni_number=_get("ni_number"),
                phone=_get("phone"),
                email=_get("email"),
                occupation=_get("occupation"),
                reference1=_get("reference1"),
                reference2=_get("reference2"),
                apartment_type=_get("apartment_type"),
                lease_period_months=period,
            )

            # Build lease start and end dates from the selected month/year/period
            from datetime import date
            import calendar
            m_idx = MONTHS.index(_get("start_month")) + 1
            y     = int(_get("start_year"))
            start = date(y, m_idx, 1)

            # Calculate end date by moving forward the lease period in months
            end_month = m_idx + period
            end_year  = y + (end_month - 1) // 12
            end_month = ((end_month - 1) % 12) + 1
            end = date(end_year, end_month, 1)

            # Attempt to find an available apartment matching the selected type
            available = apartment_service.get_available_apartments()
            match = next(
                (a for a in available
                 if a["apartment_type"] == _get("apartment_type")),
                None
            )

            # If a suitable apartment is found, create the lease immediately
            if match:
                lease_service.create_lease(
                    tenant_id=tenant_id,
                    apartment_id=match["id"],
                    start_date=start,
                    end_date=end,
                    monthly_rent=rent,
                    deposit_amount=deposit,
                )
                apt_info = f"Assigned: {match['property_name']} - Unit {match['unit_number']}"
            else:
                apt_info = "No matching apartment available - lease not created."

            # Clear entry fields after successful registration
            for w in widgets.values():
                if isinstance(w, tk.Entry):
                    w.delete(0, tk.END)

            # Refresh the tenant table so the new record appears immediately
            refresh_tenants()

            messagebox.showinfo(
                "Tenant Registered",
                f"Tenant '{_get('name') or 'new tenant'}' registered.\n{apt_info}"
            )
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))

    row_btn = len(fields_def) // 2 + 2
    tk.Button(tab_reg, text="Register Tenant", bg=ACCENT, fg="white",
              font=("Helvetica", 11, "bold"), relief="flat",
              command=register_tenant).grid(
        row=row_btn, column=0, columnspan=4, pady=18)
    

    # TAB 2 - Tenant List
    tab_tenants = tk.Frame(nb, bg="white")
    nb.add(tab_tenants, text="  Tenants  ")

    tk.Label(tab_tenants, text="Registered Tenants",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    # Table used to display all registered tenants and lease info
    cols_t = ("Name", "NI Number", "Phone", "Email", "Type", "Lease Period",
              "Property", "Unit", "Lease End")
    tree_t = ttk.Treeview(tab_tenants, columns=cols_t, show="headings", height=18)
    for c in cols_t:
        tree_t.heading(c, text=c)
        tree_t.column(c, width=110, anchor="w")
    tree_t.pack(fill="both", expand=True, padx=20, pady=10)

    sb_t = ttk.Scrollbar(tab_tenants, orient="vertical", command=tree_t.yview)
    tree_t.configure(yscrollcommand=sb_t.set)

    def refresh_tenants():
        # Clear existing rows before repopulating the table
        for row in tree_t.get_children():
            tree_t.delete(row)
        try:
            for t in tenant_service.get_all_tenants():
                tree_t.insert("", "end", values=(
                    t.get("name", ""),
                    t.get("ni_number", ""),
                    t.get("phone", ""),
                    t.get("email", ""),
                    t.get("apartment_type", ""),
                    f"{t.get('lease_period_months', '')} months",
                    t.get("property_name", "-"),
                    t.get("unit_number", "-"),
                    str(t.get("end_date", "-")),
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    refresh_tenants()
    tk.Button(tab_tenants, text="Refresh", bg=ACCENT, fg="white",
              relief="flat", command=refresh_tenants).pack(pady=5)


    # TAB 3 - Maintenance Requests
    tab_maint = tk.Frame(nb, bg="white")
    nb.add(tab_maint, text="  Maintenance  ")

    tk.Label(tab_maint, text="Maintenance Requests",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    # Table showing all maintenance requests currently stored in the system
    cols_m = ("ID", "Apartment", "Description", "Priority", "Status",
              "Submitted", "Assigned To")
    tree_m = ttk.Treeview(tab_maint, columns=cols_m, show="headings", height=16)
    for c in cols_m:
        tree_m.heading(c, text=c)
        tree_m.column(c, width=120, anchor="w")
    tree_m.pack(fill="both", expand=True, padx=20, pady=5)

    def refresh_maintenance():
        # Reload all maintenance records into the table
        for row in tree_m.get_children():
            tree_m.delete(row)
        try:
            for r in maintenance_service.get_all_requests():
                tree_m.insert("", "end", values=(
                    r.get("id"), r.get("apartment_id"),
                    r.get("description", "")[:50],
                    r.get("priority"), r.get("status"),
                    str(r.get("submission_date", ""))[:16],
                    r.get("assigned_staff") or "-",
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    refresh_maintenance()

    def add_maintenance_popup():
        # Popup form for creating a new maintenance request
        pop = tk.Toplevel(root)
        pop.title("New Maintenance Request")
        pop.geometry("400x320")
        pop.configure(bg="white")

        tk.Label(pop, text="Apartment ID", bg="white").pack(pady=(15, 2))
        apt_e = tk.Entry(pop, width=30)
        apt_e.pack()

        tk.Label(pop, text="Description", bg="white").pack(pady=(10, 2))
        desc_e = tk.Entry(pop, width=30)
        desc_e.pack()

        tk.Label(pop, text="Priority", bg="white").pack(pady=(10, 2))
        pri_var = tk.StringVar(value="Medium")
        ttk.Combobox(pop, textvariable=pri_var,
                     values=["Low", "Medium", "High", "Emergency"],
                     state="readonly", width=28).pack()

        def submit():
            # Submit the new maintenance request and refresh the table
            try:
                maintenance_service.create_request(
                    int(apt_e.get()), desc_e.get(), pri_var.get()
                )
                pop.destroy()
                refresh_maintenance()
                messagebox.showinfo("Done", "Maintenance request created.")
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Button(pop, text="Submit", bg=ACCENT, fg="white",
                  relief="flat", command=submit).pack(pady=18)

    tk.Button(tab_maint, text="+ Add Request", bg=ACCENT, fg="white",
              relief="flat", command=add_maintenance_popup
              ).pack(pady=8)


    # TAB 4 - Complaints
    tab_comp = tk.Frame(nb, bg="white")
    nb.add(tab_comp, text="  Complaints  ")

    tk.Label(tab_comp, text="Tenant Complaints",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    # Table displaying complaints submitted by tenants
    cols_c = ("ID", "Tenant", "Issue", "Category", "Status", "Submitted")
    tree_c = ttk.Treeview(tab_comp, columns=cols_c, show="headings", height=14)
    for c in cols_c:
        tree_c.heading(c, text=c)
        tree_c.column(c, width=140, anchor="w")
    tree_c.pack(fill="both", expand=True, padx=20, pady=5)

    def refresh_complaints():
        # Reload complaint data from the database into the table
        for row in tree_c.get_children():
            tree_c.delete(row)
        try:
            for c in complaint_service.get_all_complaints():
                tree_c.insert("", "end", values=(
                    c.get("id"), c.get("tenant_name"),
                    c.get("issue", "")[:60],
                    c.get("category", "Other"),
                    c.get("status"),
                    str(c.get("submission_date", ""))[:16],
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    refresh_complaints()

    def add_complaint_popup():
        # Popup window for staff to log a complaint manually
        pop = tk.Toplevel(root)
        pop.title("Log Complaint")
        pop.geometry("420x320")
        pop.configure(bg="white")

        tk.Label(pop, text="Tenant Name", bg="white").pack(pady=(15, 2))
        name_e = tk.Entry(pop, width=35)
        name_e.pack()

        tk.Label(pop, text="Issue Description", bg="white").pack(pady=(10, 2))
        issue_e = tk.Entry(pop, width=35)
        issue_e.pack()

        tk.Label(pop, text="Category", bg="white").pack(pady=(10, 2))
        cat_var = tk.StringVar(value="Other")
        ttk.Combobox(pop, textvariable=cat_var,
                     values=["Noise", "Repair", "Neighbour", "Billing", "Other"],
                     state="readonly", width=33).pack()

        def submit():
            # Basic validation before complaint submission
            if not name_e.get().strip() or not issue_e.get().strip():
                messagebox.showwarning("Missing", "Name and issue are required.")
                return
            try:
                complaint_service.create_complaint(
                    name_e.get().strip(),
                    issue_e.get().strip(),
                    cat_var.get()
                )
                pop.destroy()
                refresh_complaints()
                messagebox.showinfo("Done", "Complaint logged.")
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Button(pop, text="Submit", bg=ACCENT, fg="white",
                  relief="flat", command=submit).pack(pady=18)

    tk.Button(tab_comp, text="+ Log Complaint", bg="#6a1b9a", fg="white",
              relief="flat", command=add_complaint_popup).pack(pady=8)

    # Start the Tkinter event loop
    root.mainloop()