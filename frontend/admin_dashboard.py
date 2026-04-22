# ================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Esila Keskin 
# Student ID(s):  24064432 
# Description: Admin dashboard - user management, create and deactivate accounts per city
# ================================================================
import tkinter as tk
from tkinter import messagebox, ttk

from backend.services.user_service import UserService
from backend.services.apartment_service import ApartmentService
from backend.services.tenant_service import TenantService
from backend.services.lease_service import LeaseService
from backend.services.report_service import ReportService

PRIMARY = "#0d47a1"
ACCENT  = "#1976d2"
BG      = "#f0f4f8"

ROLES      = ["FrontDesk", "Finance", "Maintenance", "Admin", "Manager", "Tenant"]
APT_TYPES  = ["Studio", "1-Bedroom", "2-Bedroom", "3-Bedroom", "4-Bedroom+"]
APT_STATUS = ["available", "occupied", "maintenance"]
CITIES     = ["Bristol", "Cardiff", "London", "Manchester"]


def open_admin_dashboard(user: dict):
    username = user["full_name"] if isinstance(user, dict) else str(user)
    location = user.get("location", "All") if isinstance(user, dict) else "All"

    user_svc  = UserService()
    apt_svc   = ApartmentService()
    tenant_svc = TenantService()
    lease_svc  = LeaseService()
    report_svc = ReportService()

    root = tk.Tk()
    root.title(f"Admin Dashboard - {username} ({location})")
    root.geometry("1100x720")
    root.configure(bg=BG)

    #  Header 
    header = tk.Frame(root, bg=PRIMARY, height=52)
    header.pack(fill="x")
    tk.Label(header, text=f"Administrator - {username}  |  Location: {location}",
             font=("Helvetica", 15, "bold"), bg=PRIMARY, fg="white"
             ).pack(side="left", padx=20, pady=10)

    def logout():
        from frontend import login
        if messagebox.askyesno("Logout", "Are you sure?"):
            root.destroy()
            login.run_login()

    tk.Button(header, text="Logout", bg="#c62828", fg="white",
              font=("Helvetica", 10, "bold"), relief="flat",
              command=logout).pack(side="right", padx=15, pady=10)

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=10, pady=10)

    # TAB 1 - User Management
    tab_users = tk.Frame(nb, bg="white")
    nb.add(tab_users, text="  User Management  ")

    tk.Label(tab_users, text="User Accounts",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    cols_u = ("ID", "Username", "Role", "Full Name", "Email", "Phone",
              "Location", "Active", "Created")
    tree_u = ttk.Treeview(tab_users, columns=cols_u, show="headings", height=13)
    for c in cols_u:
        tree_u.heading(c, text=c)
        tree_u.column(c, width=110, anchor="w")
    tree_u.pack(fill="both", expand=True, padx=20, pady=5)

    def refresh_users():
        for row in tree_u.get_children():
            tree_u.delete(row)
        try:
            for u in user_svc.get_all_users():
                tree_u.insert("", "end", values=(
                    u["id"], u["username"], u["role"], u["full_name"],
                    u["email"], u.get("phone", ""),
                    u.get("location", "-"),
                    "Yes" if u["is_active"] else "No",
                    str(u.get("created_at", ""))[:10],
                ))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    refresh_users()

    btn_frame = tk.Frame(tab_users, bg="white")
    btn_frame.pack(pady=5)

    def create_user_popup():
        pop = tk.Toplevel(root)
        pop.title("Create User Account")
        pop.geometry("430x450")
        pop.configure(bg="white")

        fields = {}

        def f(label, key, widget_type="entry", opts=None):
            tk.Label(pop, text=label, bg="white").pack(pady=(8, 2), padx=20, anchor="w")
            if widget_type == "entry":
                w = tk.Entry(pop, width=35)
            elif widget_type == "combo":
                w = ttk.Combobox(pop, values=opts, state="readonly", width=33)
                if opts:
                    w.set(opts[0])
            elif widget_type == "password":
                w = tk.Entry(pop, width=35, show="*")
            w.pack(padx=20, anchor="w")
            fields[key] = w

        f("Username *", "username")
        f("Password *", "password", "password")
        f("Full Name *", "full_name")
        f("Email *", "email")
        f("Phone", "phone")
        f("Role *", "role", "combo", ROLES)
        f("Location", "location", "combo", ["-"] + CITIES)

        def submit():
            try:
                user_svc.create_user(
                    username=fields["username"].get().strip(),
                    password=fields["password"].get().strip(),
                    role=fields["role"].get(),
                    full_name=fields["full_name"].get().strip(),
                    email=fields["email"].get().strip(),
                    phone=fields["phone"].get().strip() or None,
                    location=(fields["location"].get() or None)
                        if fields["location"].get() != "-" else None,
                )
                pop.destroy()
                refresh_users()
                messagebox.showinfo("Done", "User created.")
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Button(pop, text="Create User", bg=ACCENT, fg="white",
                  relief="flat", command=submit).pack(pady=18)

    def deactivate_selected():
        sel = tree_u.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a user first.")
            return
        uid = tree_u.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirm", f"Deactivate user ID {uid}?"):
            return
        try:
            user_svc.deactivate_user(uid)
            refresh_users()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(btn_frame, text="+ Create User", bg=ACCENT, fg="white",
              relief="flat", command=create_user_popup).pack(side="left", padx=8)
    tk.Button(btn_frame, text="Deactivate Selected", bg="#c62828", fg="white",
              relief="flat", command=deactivate_selected).pack(side="left", padx=8)
    tk.Button(btn_frame, text="Refresh", bg="#555", fg="white",
              relief="flat", command=refresh_users).pack(side="left", padx=8)

    # TAB 2 - Apartment Management
    tab_apt = tk.Frame(nb, bg="white")
    nb.add(tab_apt, text="  Apartments  ")

    # Filter
    apt_filter = tk.Frame(tab_apt, bg="white")
    apt_filter.pack(fill="x", padx=20, pady=(15, 5))
    tk.Label(apt_filter, text="Filter by City:", bg="white").pack(side="left")
    city_var = ttk.Combobox(apt_filter, values=["All"] + CITIES,
                            state="readonly", width=14)
    city_var.set("All")
    city_var.pack(side="left", padx=8)

    cols_a = ("ID", "Property", "City", "Unit", "Floor", "Beds", "Baths",
              "Size (m²)", "Rent/mo", "Type", "Status")
    tree_a = ttk.Treeview(tab_apt, columns=cols_a, show="headings", height=15)
    for c in cols_a:
        tree_a.heading(c, text=c)
        tree_a.column(c, width=95, anchor="w")
    tree_a.pack(fill="both", expand=True, padx=20, pady=5)

    status_colours = {"available": "#c8e6c9", "occupied": "#fff9c4",
                      "maintenance": "#ffcdd2"}
    for tag, col in status_colours.items():
        tree_a.tag_configure(tag, background=col)

    def refresh_apts():
        for row in tree_a.get_children():
            tree_a.delete(row)
        try:
            city = city_var.get()
            rows = (apt_svc.get_apartments_by_city(city)
                    if city != "All" else apt_svc.get_all_apartments())
            for r in rows:
                tag = r.get("status", "available")
                tree_a.insert("", "end", tags=(tag,), values=(
                    r["id"], r.get("property_name", ""),
                    r.get("city", ""), r["unit_number"],
                    r.get("floor", 0), r["bedrooms"], r["bathrooms"],
                    r.get("size_sqm", ""), f"£{float(r['monthly_rent']):,.2f}",
                    r.get("apartment_type", ""), r["status"],
                ))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(apt_filter, text="Filter", bg=ACCENT, fg="white",
              relief="flat", command=refresh_apts).pack(side="left", padx=8)
    refresh_apts()

    def change_apt_status():
        sel = tree_a.selection()
        if not sel:
            messagebox.showwarning("Select", "Select an apartment first.")
            return
        apt_id = tree_a.item(sel[0])["values"][0]
        pop = tk.Toplevel(root)
        pop.title("Change Status")
        pop.geometry("300x180")
        pop.configure(bg="white")
        tk.Label(pop, text=f"Apartment ID: {apt_id}", bg="white",
                 font=("Helvetica", 11)).pack(pady=(20, 5))
        tk.Label(pop, text="New Status:", bg="white").pack()
        st_var = ttk.Combobox(pop, values=APT_STATUS, state="readonly", width=25)
        st_var.set(APT_STATUS[0]); st_var.pack(pady=5)

        def apply():
            try:
                apt_svc.set_status(apt_id, st_var.get())
                pop.destroy()
                refresh_apts()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

        tk.Button(pop, text="Apply", bg=ACCENT, fg="white",
                  relief="flat", command=apply).pack(pady=12)

    tk.Button(tab_apt, text="Change Status", bg="#e65100", fg="white",
              relief="flat", command=change_apt_status).pack(pady=5)

    # TAB 3 - Lease Tracker
    
    tab_lease = tk.Frame(nb, bg="white")
    nb.add(tab_lease, text="  Lease Tracker  ")

    tk.Label(tab_lease, text="All Leases",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    cols_l = ("ID", "Tenant", "Property", "City", "Unit",
              "Start", "End", "Rent", "Deposit", "Status")
    tree_l = ttk.Treeview(tab_lease, columns=cols_l, show="headings", height=14)
    for c in cols_l:
        tree_l.heading(c, text=c)
        tree_l.column(c, width=105, anchor="w")
    tree_l.pack(fill="both", expand=True, padx=20, pady=5)
    tree_l.tag_configure("expired", background="#ffcdd2")
    tree_l.tag_configure("terminated", background="#ef9a9a")

    def refresh_leases():
        for row in tree_l.get_children():
            tree_l.delete(row)
        try:
            for r in lease_svc.get_all_leases():
                tag = r.get("status", "active")
                tree_l.insert("", "end", tags=(tag if tag != "active" else "",), values=(
                    r["id"], r.get("tenant_name", ""),
                    r.get("property_name", ""), r.get("city", ""),
                    r.get("unit_number", ""),
                    str(r.get("start_date", "")), str(r.get("end_date", "")),
                    f"£{float(r['monthly_rent']):,.2f}",
                    f"£{float(r['deposit_amount']):,.2f}",
                    r.get("status", "").upper(),
                ))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    refresh_leases()

    # Expiring soon panel
    exp_frame = tk.Frame(tab_lease, bg="#fff3cd", relief="groove", bd=1)
    exp_frame.pack(fill="x", padx=20, pady=5)
    tk.Label(exp_frame, text="Leases Expiring Within 30 Days:",
             font=("Helvetica", 10, "bold"), bg="#fff3cd"
             ).pack(side="left", padx=10, pady=5)
    exp_var = tk.StringVar(value="-")
    tk.Label(exp_frame, textvariable=exp_var, bg="#fff3cd",
             font=("Helvetica", 10)).pack(side="left", padx=5)

    def load_expiring():
        try:
            expiring = lease_svc.get_expiring_soon(30)
            if expiring:
                exp_var.set(
                    "  |  ".join(
                        f"{r['tenant_name']} → {r['end_date']}" for r in expiring
                    )
                )
            else:
                exp_var.set("None in the next 30 days.")
        except Exception:
            exp_var.set("Could not load.")

    load_expiring()
    tk.Button(tab_lease, text="Refresh Leases", bg=ACCENT, fg="white",
              relief="flat", command=lambda: [refresh_leases(), load_expiring()]
              ).pack(pady=5)

    # TAB 4 - Reports
    tab_rep = tk.Frame(nb, bg="white")
    nb.add(tab_rep, text="  Reports  ")

    tk.Label(tab_rep, text="System Reports",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    rep_nb = ttk.Notebook(tab_rep)
    rep_nb.pack(fill="both", expand=True, padx=10, pady=5)

    # Occupancy
    occ_tab = tk.Frame(rep_nb, bg="white")
    rep_nb.add(occ_tab, text="Occupancy")

    cols_o = ("City", "Total Units", "Occupied", "Available",
              "Under Maintenance", "Occupancy %")
    tree_o = ttk.Treeview(occ_tab, columns=cols_o, show="headings", height=8)
    for c in cols_o:
        tree_o.heading(c, text=c)
        tree_o.column(c, width=140, anchor="center")
    tree_o.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_occ():
        for row in tree_o.get_children():
            tree_o.delete(row)
        try:
            for r in report_svc.occupancy_report():
                tree_o.insert("", "end", values=(
                    r["city"], r["total_units"], r["occupied"],
                    r["available"], r["under_maintenance"],
                    f"{r['occupancy_pct'] or 0:.1f}%",
                ))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(occ_tab, text="Load Report", bg=ACCENT, fg="white",
              relief="flat", command=refresh_occ).pack(pady=8)
    refresh_occ()

    # Financial
    fin_tab = tk.Frame(rep_nb, bg="white")
    rep_nb.add(fin_tab, text="Financial Summary")

    fin_frame = tk.Frame(fin_tab, bg="white", padx=30)
    fin_frame.pack(anchor="nw", pady=20)
    fin_var = tk.StringVar()
    tk.Label(fin_frame, textvariable=fin_var, bg="white",
             font=("Helvetica", 11), justify="left").pack(anchor="w")

    def refresh_fin():
        try:
            r = report_svc.financial_summary()
            fin_var.set(
                f"Collected: £{float(r.get('collected') or 0):,.2f}\n"
                f"Pending: £{float(r.get('pending') or 0):,.2f}\n"
                f"Overdue: £{float(r.get('overdue') or 0):,.2f}\n"
                f"Total Late Fees:£{float(r.get('total_late_fees') or 0):,.2f}\n"
                f"Total Invoices: {r.get('total_invoices', 0)}"
            )
        except Exception as exc:
            fin_var.set(f"Error: {exc}")

    tk.Button(fin_tab, text="Load Financial Summary", bg=ACCENT, fg="white",
              relief="flat", command=refresh_fin).pack(pady=8)
    refresh_fin()

    # Maintenance costs
    mc_tab = tk.Frame(rep_nb, bg="white")
    rep_nb.add(mc_tab, text="Maintenance Costs")

    cols_mc = ("City", "Total Requests", "Open/In-Progress",
               "Total Cost £", "Avg Hours")
    tree_mc = ttk.Treeview(mc_tab, columns=cols_mc, show="headings", height=8)
    for c in cols_mc:
        tree_mc.heading(c, text=c)
        tree_mc.column(c, width=155, anchor="center")
    tree_mc.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_mc():
        for row in tree_mc.get_children():
            tree_mc.delete(row)
        try:
            for r in report_svc.maintenance_cost_report():
                tree_mc.insert("", "end", values=(
                    r["city"], r["total_requests"], r["open_requests"],
                    f"£{float(r.get('total_cost') or 0):,.2f}",
                    f"{float(r.get('avg_hours') or 0):.1f}",
                ))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(mc_tab, text="Load Report", bg=ACCENT, fg="white",
              relief="flat", command=refresh_mc).pack(pady=8)
    refresh_mc()

    root.mainloop()
