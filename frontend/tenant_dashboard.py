import tkinter as tk
from tkinter import messagebox, ttk

# Service layer imports used to load tenant data, invoices, payments,
# complaints, maintenance requests and lease actions from the backend
from backend.services.tenant_service import TenantService
from backend.services.invoice_service import InvoiceService
from backend.services.payment_service import PaymentService
from backend.services.complaint_service import ComplaintService
from backend.services.maintenance_service import MaintenanceService
from backend.services.lease_service import LeaseService

# Colour constants used to keep the tenant portal styling consistent
PRIMARY = "#0d47a1"
ACCENT  = "#1976d2"
BG      = "#f0f4f8"

# Month and year options used by the payment history filter controls
MONTHS     = ["All", "January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
MONTH_NUMS = {name: idx for idx, name in enumerate(MONTHS)}
YEARS      = ["All"] + [str(y) for y in range(2024, 2028)]


def open_tenant_dashboard(user: dict):
    # Use the full name when a user dictionary is provided,
    # otherwise fall back to a string version of the value
    username = user["full_name"] if isinstance(user, dict) else str(user)

    # Create service instances used across the different tenant portal tabs
    tenant_svc  = TenantService()
    invoice_svc = InvoiceService()
    payment_svc = PaymentService()
    complaint_svc = ComplaintService()
    maint_svc   = MaintenanceService()
    lease_svc   = LeaseService()

    # Try to find the tenant record linked to the logged-in user account
    try:
        tenant = tenant_svc.get_tenant_by_username(
            user["username"] if isinstance(user, dict) else username
        )
    except Exception:
        tenant = None

    # Store the tenant ID for reuse in payment, complaint and maintenance queries
    tenant_id = tenant["id"] if tenant else None

    # Main tenant portal window setup
    root = tk.Tk()
    root.title(f"Tenant Portal - {username}")
    root.geometry("980x680")
    root.configure(bg=BG)

    # Header section showing the tenant portal title and logout option
    header = tk.Frame(root, bg=PRIMARY, height=52)

    # Return the user to the login page after confirmation
    def logout():
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

    # Tab displaying tenant personal details and current lease information
     # TAB 1 - My Details & Lease
    tab_info = tk.Frame(nb, bg="white")
    nb.add(tab_info, text="  My Details  ")

    # Load and display the tenant's personal and lease details
    def load_info():
        # Clear existing widgets before rebuilding the tab contents
        for w in tab_info.winfo_children():
            w.destroy()
        tk.Label(tab_info, text="My Details & Lease",
                 font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
                 ).pack(pady=(15, 10), padx=25, anchor="w")

        # Stop early if this account is not linked to a tenant record
        if not tenant_id:
            tk.Label(tab_info, text="No tenant record linked to this account.",
                     bg="white", fg="gray").pack(padx=25)
            return

        # Retrieve full tenant and lease information from the backend
        try:
            t = tenant_svc.get_tenant_by_id(tenant_id)
        except Exception as exc:
            tk.Label(tab_info, text=f"Error: {exc}", bg="white", fg="red").pack()
            return

        if not t:
            tk.Label(tab_info, text="Tenant record not found.", bg="white", fg="gray").pack()
            return

        # Personal information fields shown in the top section
        info_rows = [
            ("Name", t.get("name", "")),
            ("NI Number", t.get("ni_number", "")),
            ("Phone", t.get("phone", "")),
            ("Email", t.get("email", "")),
            ("Occupation",   t.get("occupation", "-")),
        ]
        # Lease and property information shown below the personal details
        lease_rows = [
            ("Property", t.get("property_name", "-")),
            ("City", t.get("city", "-")),
            ("Unit", t.get("unit_number", "-")),
            ("Apt Type", t.get("apt_type", "-")),
            ("Monthly Rent", f"£{float(t.get('lease_rent', 0) or 0):,.2f}"),
            ("Lease Start",  str(t.get("start_date", "-"))),
            ("Lease End", str(t.get("end_date", "-"))),
            ("Deposit", f"£{float(t.get('deposit_amount', 0) or 0):,.2f}"),
            ("Lease Status", (t.get("lease_status") or "No active lease").upper()),
        ]

        frame = tk.Frame(tab_info, bg="white", padx=25)
        frame.pack(anchor="nw", fill="x")

        tk.Label(frame, text="Personal Information",
                 font=("Helvetica", 11, "bold"), bg="white", fg=ACCENT
                 ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        for i, (k, v) in enumerate(info_rows, 1):
            tk.Label(frame, text=k + ":", bg="white",
                     font=("Helvetica", 10, "bold"), width=14, anchor="e"
                     ).grid(row=i, column=0, sticky="e", pady=2)
            tk.Label(frame, text=v, bg="white",
                     font=("Helvetica", 10), anchor="w"
                     ).grid(row=i, column=1, sticky="w", padx=(10, 0))

        tk.Label(frame, text="Lease Information",
                 font=("Helvetica", 11, "bold"), bg="white", fg=ACCENT
                 ).grid(row=len(info_rows)+2, column=0, columnspan=2,
                        sticky="w", pady=(15, 5))
        for i, (k, v) in enumerate(lease_rows, len(info_rows)+3):
            tk.Label(frame, text=k + ":", bg="white",
                     font=("Helvetica", 10, "bold"), width=14, anchor="e"
                     ).grid(row=i, column=0, sticky="e", pady=2)
            clr = "#c62828" if k == "Lease Status" and "terminated" in str(v).lower() else "#333"
            tk.Label(frame, text=v, bg="white",
                     font=("Helvetica", 10), fg=clr, anchor="w"
                     ).grid(row=i, column=1, sticky="w", padx=(10, 0))

        # Only show the early termination option when an active lease exists
        # Early termination button
        if t.get("lease_id"):
            tk.Button(
                tab_info,
                text="Request Early Termination (1 month notice, 5% penalty)",
                bg="#e65100", fg="white", relief="flat",
                font=("Helvetica", 10),
                command=lambda: request_early_termination(t["lease_id"])
            ).pack(pady=15, padx=25, anchor="w")

    # Record an early termination request after tenant confirmation

    def request_early_termination(lease_id):
        if not messagebox.askyesno(
            "Early Termination",
            "You must give 1 month's notice.\n"
            "A penalty of 5% of your monthly rent will be charged.\n\n"
            "Proceed?"
        ):
            return
        try:
            penalty = lease_svc.request_early_termination(lease_id)
            messagebox.showinfo(
                "Notice Given",
                f"Early termination notice recorded.\n"
                f"Penalty fee: £{penalty:,.2f}\n"
                "Your tenancy ends 1 month from today."
            )
            load_info()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    # Populate the details tab when the dashboard first opens
    load_info()

    # Tab displaying invoice and payment history for the tenant
    # TAB 2 - Payment History
    tab_pay = tk.Frame(nb, bg="white")
    nb.add(tab_pay, text="  Payments  ")

    tk.Label(tab_pay, text="Payment History",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    # Filter controls for narrowing payment history by month and year
    pay_filter = tk.Frame(tab_pay, bg="white")
    pay_filter.pack(fill="x", padx=20, pady=(0, 8))

    tk.Label(pay_filter, text="Month:", bg="white").pack(side="left")
    pay_month = ttk.Combobox(pay_filter, values=MONTHS, state="readonly", width=13)
    pay_month.set("All"); pay_month.pack(side="left", padx=(5, 12))

    tk.Label(pay_filter, text="Year:", bg="white").pack(side="left")
    pay_year = ttk.Combobox(pay_filter, values=YEARS, state="readonly", width=8)
    pay_year.set("All"); pay_year.pack(side="left", padx=5)

    # Table columns for invoice and payment history
    cols_p = ("Month", "Year", "Amount", "Due Date", "Status",
              "Paid On", "Method", "Receipt")
    tree_p = ttk.Treeview(tab_pay, columns=cols_p, show="headings", height=16)
    for c in cols_p:
        tree_p.heading(c, text=c)
        tree_p.column(c, width=110, anchor="w")
    tree_p.pack(fill="both", expand=True, padx=20, pady=5)

    # Row colours used to visually distinguish invoice/payment status
    tag_cols = {"paid": "#c8e6c9", "overdue": "#ffcdd2",
                "unpaid": "#fff9c4", "partial": "#ffe0b2"}
    for tag, col in tag_cols.items():
        tree_p.tag_configure(tag, background=col)

    # Reload the payment table using the selected month and year filters
    def refresh_payments():
        # Clear existing payment rows before inserting refreshed data
        for row in tree_p.get_children():
            tree_p.delete(row)
        if not tenant_id:
            return
        try:
            # Fetch invoice records for the logged-in tenant
            rows = invoice_svc.get_invoices_for_tenant(tenant_id)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        # Read the selected filter values from the combobox controls
        m_filter = MONTH_NUMS.get(pay_month.get(), 0)
        y_filter = pay_year.get()

        for r in rows:
            # Skip rows that do not match the currently selected filters
            if m_filter and r.get("month") != m_filter:
                continue
            if y_filter != "All" and str(r.get("year")) != y_filter:
                continue
            status = r.get("status", "unpaid")
            # Find payment for this invoice
            paid_on = method = receipt = "-"
            try:
                # Attempt to match each invoice with a recorded payment
                pays = payment_svc.get_payments_for_tenant(tenant_id)
                match = next((p for p in pays if p["invoice_id"] == r["id"]), None)
                if match:
                    paid_on = str(match.get("payment_date", ""))[:10]
                    method  = match.get("method", "-")
                    receipt = match.get("receipt_number", "-")
            except Exception:
                pass

            # Insert the formatted payment record into the table
            tree_p.insert("", "end", tags=(status,), values=(
                MONTHS[r.get("month", 1)],
                r.get("year"),
                f"£{float(r.get('amount', 0)):,.2f}",
                str(r.get("due_date", "")),
                status.upper(),
                paid_on, method, receipt
            ))

    # Button used to apply the selected payment filters
    tk.Button(pay_filter, text="Filter", bg=ACCENT, fg="white",
              relief="flat", command=refresh_payments).pack(side="left", padx=10)
    # Load payment history when the tab is created
    refresh_payments()

    # Tab showing submitted maintenance requests and their progress
    # TAB 3 - Maintenance Requests
    tab_maint = tk.Frame(nb, bg="white")
    nb.add(tab_maint, text="  Maintenance  ")

    tk.Label(tab_maint, text="My Maintenance Requests",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    # Table columns for tenant maintenance request history
    cols_m = ("ID", "Description", "Priority", "Status",
              "Submitted", "Scheduled", "Resolved")
    tree_m = ttk.Treeview(tab_maint, columns=cols_m, show="headings", height=12)
    for c in cols_m:
        tree_m.heading(c, text=c)
        tree_m.column(c, width=130, anchor="w")
    tree_m.pack(fill="both", expand=True, padx=20, pady=5)

    # Reload maintenance requests linked to the current tenant
    def refresh_maintenance():
        # Clear existing rows before refreshing maintenance data
        for row in tree_m.get_children():
            tree_m.delete(row)
        if not tenant_id:
            return
        try:
            # Fetch and display all maintenance requests for this tenant
            for r in maint_svc.get_requests_for_tenant(tenant_id):
                tree_m.insert("", "end", values=(
                    r.get("id"),
                    r.get("description", "")[:50],
                    r.get("priority"),
                    r.get("status"),
                    str(r.get("submission_date", ""))[:16],
                    str(r.get("scheduled_date") or "-")[:16],
                    str(r.get("resolution_date") or "-")[:16],
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Open a popup form for submitting a new maintenance request

    def submit_maintenance():
        pop = tk.Toplevel(root)
        pop.title("New Maintenance Request")
        pop.geometry("420x300")
        pop.configure(bg="white")

        tk.Label(pop, text="Describe the issue:", bg="white",
                 font=("Helvetica", 11)).pack(pady=(20, 5), padx=20, anchor="w")
        desc_e = tk.Text(pop, height=5, width=45, font=("Helvetica", 10))
        desc_e.pack(padx=20)

        tk.Label(pop, text="Priority:", bg="white",
                 font=("Helvetica", 10)).pack(pady=(10, 2), padx=20, anchor="w")
        pri_var = tk.StringVar(value="Medium")
        ttk.Combobox(pop, textvariable=pri_var,
                     values=["Low", "Medium", "High", "Emergency"],
                     state="readonly", width=38).pack(padx=20)

        def do_submit():
            desc = desc_e.get("1.0", tk.END).strip()
            if not desc:
                messagebox.showwarning("Missing", "Please describe the issue.")
                return
            try:
                apt_id = 1  # default; in a real flow this comes from the lease
                if tenant and tenant.get("lease_id"):
                    # get apartment_id from active lease
                    from backend.services.lease_service import LeaseService
                    ls = LeaseService()
                    lease = ls.get_active_lease_for_tenant(tenant_id)
                    if lease:
                        apt_id = lease.get("apartment_id", 1)

                maint_svc.create_request(apt_id, desc, pri_var.get(), tenant_id)
                pop.destroy()
                refresh_maintenance()
                messagebox.showinfo("Submitted", "Maintenance request submitted.")
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Button(pop, text="Submit", bg=ACCENT, fg="white",
                  relief="flat", command=do_submit).pack(pady=15)

    tk.Button(tab_maint, text="+ Submit Request", bg=ACCENT, fg="white",
              relief="flat", command=submit_maintenance).pack(pady=8)
    refresh_maintenance()

    # TAB 4 - Complaints
    tab_comp = tk.Frame(nb, bg="white")
    nb.add(tab_comp, text="  Complaints  ")

    tk.Label(tab_comp, text="My Complaints",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    cols_c = ("ID", "Issue", "Category", "Status", "Submitted", "Resolved")
    tree_c = ttk.Treeview(tab_comp, columns=cols_c, show="headings", height=12)
    for c in cols_c:
        tree_c.heading(c, text=c)
        tree_c.column(c, width=140, anchor="w")
    tree_c.pack(fill="both", expand=True, padx=20, pady=5)

    def refresh_complaints():
        for row in tree_c.get_children():
            tree_c.delete(row)
        if not tenant_id:
            return
        try:
            for c in complaint_svc.get_complaints_for_tenant(tenant_id):
                tree_c.insert("", "end", values=(
                    c.get("id"),
                    c.get("issue", "")[:60],
                    c.get("category", "Other"),
                    c.get("status"),
                    str(c.get("submission_date", ""))[:16],
                    str(c.get("resolution_date") or "-")[:16],
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_complaint():
        pop = tk.Toplevel(root)
        pop.title("Submit Complaint")
        pop.geometry("420x280")
        pop.configure(bg="white")

        tk.Label(pop, text="Issue Description:", bg="white",
                 font=("Helvetica", 11)).pack(pady=(20, 5), padx=20, anchor="w")
        issue_e = tk.Text(pop, height=4, width=45, font=("Helvetica", 10))
        issue_e.pack(padx=20)

        tk.Label(pop, text="Category:", bg="white",
                 font=("Helvetica", 10)).pack(pady=(10, 2), padx=20, anchor="w")
        cat_var = tk.StringVar(value="Other")
        ttk.Combobox(pop, textvariable=cat_var,
                     values=["Noise", "Repair", "Neighbour", "Billing", "Other"],
                     state="readonly", width=38).pack(padx=20)

        def submit():
            issue = issue_e.get("1.0", tk.END).strip()
            if not issue:
                messagebox.showwarning("Missing", "Please describe the issue.")
                return
            try:
                complaint_svc.create_complaint(
                    username, issue, cat_var.get(), tenant_id
                )
                pop.destroy()
                refresh_complaints()
                messagebox.showinfo("Submitted", "Complaint submitted.")
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Button(pop, text="Submit", bg=ACCENT, fg="white",
                  relief="flat", command=submit).pack(pady=12)

    tk.Button(tab_comp, text="+ Submit Complaint", bg="#6a1b9a", fg="white",
              relief="flat", command=add_complaint).pack(pady=8)
    refresh_complaints()

    root.mainloop()
