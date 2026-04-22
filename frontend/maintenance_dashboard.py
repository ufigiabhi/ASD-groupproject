# ================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Esila Keskin / Aston George Merry
# Student ID(s):  24064432  / 24063013
# Description: Maintenance Staff panel - priority 
# ================================================================
import tkinter as tk
from tkinter import messagebox, ttk

from backend.services.maintenance_service import MaintenanceService

PRIMARY = "#0d47a1"
ACCENT  = "#1976d2"
BG      = "#f0f4f8"


def open_maintenance_dashboard(user: dict):
    username = user["full_name"] if isinstance(user, dict) else str(user)
    svc = MaintenanceService()

    root = tk.Tk()
    root.title(f"Maintenance Staff - {username}")
    root.geometry("1050x680")
    root.configure(bg=BG)

    #   Header  
    header = tk.Frame(root, bg=PRIMARY, height=52)
    header.pack(fill="x")
    tk.Label(header, text=f"Maintenance Staff Panel - {username}",
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

    # TAB 1 - Open / In-Progress Requests
    tab_open = tk.Frame(nb, bg="white")
    nb.add(tab_open, text="  Open Requests  ")

    tk.Label(tab_open, text="Open & In-Progress Requests (Priority Ordered)",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    cols = ("ID", "Property", "City", "Unit", "Tenant", "Description",
            "Priority", "Status", "Submitted", "Assigned To")
    tree = ttk.Treeview(tab_open, columns=cols, show="headings", height=18)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=105, anchor="w")
    tree.pack(fill="both", expand=True, padx=20, pady=5)

    tag_map = {
        "Emergency": "#ffcdd2",
        "High":      "#ffe0b2",
        "Medium":    "#fff9c4",
        "Low":       "#e8f5e9",
    }
    for tag, col in tag_map.items():
        tree.tag_configure(tag, background=col)

    def refresh_open():
        for row in tree.get_children():
            tree.delete(row)
        try:
            for r in svc.get_open_requests():
                tag = r.get("priority", "Medium")
                tree.insert("", "end", tags=(tag,), values=(
                    r.get("id"),
                    r.get("property_name", "-"),
                    r.get("city", "-"),
                    r.get("unit_number", "-"),
                    r.get("tenant_name") or "-",
                    r.get("description", "")[:50],
                    r.get("priority"),
                    r.get("status"),
                    str(r.get("submission_date", ""))[:16],
                    r.get("assigned_staff") or "-",
                ))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    refresh_open()
    tk.Button(tab_open, text="Refresh", bg=ACCENT, fg="white",
              relief="flat", command=refresh_open).pack(pady=5)

     # TAB 2 - Assign & Update Request
    tab_update = tk.Frame(nb, bg="white")
    nb.add(tab_update, text="  Update Request  ")

    tk.Label(tab_update, text="Assign Staff / Update Status",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(20, 10), padx=25, anchor="w")

    frm = tk.Frame(tab_update, bg="white", padx=25)
    frm.pack(anchor="nw")

    def lbl(txt):
        tk.Label(frm, text=txt, bg="white",
                 font=("Helvetica", 10)).pack(anchor="w", pady=(10, 2))

    def ent(w=30):
        e = tk.Entry(frm, width=w, font=("Helvetica", 10))
        e.pack(anchor="w")
        return e

    lbl("Request ID *")
    req_id_e = ent()

    lbl("Assign to Staff Member")
    staff_e = ent()
    staff_e.insert(0, username)

    result_var = tk.StringVar()
    tk.Label(tab_update, textvariable=result_var, bg="white",
             fg="#2e7d32", font=("Helvetica", 10, "bold")).pack(pady=5)

    def do_assign():
        try:
            rid = int(req_id_e.get().strip())
        except ValueError:
            messagebox.showerror("Invalid", "Enter a numeric Request ID.")
            return
        try:
            svc.assign_staff(rid, staff_e.get().strip() or username)
            result_var.set(f"Request #{rid} assigned to {staff_e.get().strip()}")
            refresh_open()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(frm, text="Assign Staff", bg=ACCENT, fg="white",
              relief="flat", command=do_assign).pack(pady=12, anchor="w")

    tk.Label(frm, text="─" * 50, bg="white", fg="#ccc").pack(pady=10, anchor="w")

    tk.Label(frm, text="Resolve Request",
             font=("Helvetica", 11, "bold"), bg="white", fg="#2e7d32"
             ).pack(anchor="w")

    lbl("Request ID to Resolve *")
    res_id_e = ent()

    lbl("Time Taken (hours) *")
    time_e = ent()

    lbl("Cost (£) *")
    cost_e = ent()

    def do_resolve():
        try:
            rid  = int(res_id_e.get().strip())
            hrs  = float(time_e.get().strip())
            cost = float(cost_e.get().strip())
        except ValueError:
            messagebox.showerror("Invalid", "ID, time and cost must be numbers.")
            return
        try:
            svc.resolve_request(rid, hrs, cost)
            result_var.set(f"Request #{rid} marked RESOLVED - {hrs}h / £{cost}")
            refresh_open()
            refresh_all()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(frm, text="Mark as Resolved", bg="#2e7d32", fg="white",
              relief="flat", command=do_resolve).pack(pady=12, anchor="w")

    # TAB 3 - All Requests History
    tab_all = tk.Frame(nb, bg="white")
    nb.add(tab_all, text="  All Requests  ")

    tk.Label(tab_all, text="All Maintenance Requests",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(15, 5), padx=20, anchor="w")

    cols_a = ("ID", "Apartment", "Description", "Priority", "Status",
              "Submitted", "Resolved", "Time (h)", "Cost £", "Staff")
    tree_a = ttk.Treeview(tab_all, columns=cols_a, show="headings", height=18)
    for c in cols_a:
        tree_a.heading(c, text=c)
        tree_a.column(c, width=108, anchor="w")
    tree_a.pack(fill="both", expand=True, padx=20, pady=5)

    def refresh_all():
        for row in tree_a.get_children():
            tree_a.delete(row)
        try:
            for r in svc.get_all_requests():
                tree_a.insert("", "end", values=(
                    r.get("id"),
                    r.get("apartment_id"),
                    r.get("description", "")[:45],
                    r.get("priority"),
                    r.get("status"),
                    str(r.get("submission_date", ""))[:16],
                    str(r.get("resolution_date") or "-")[:16],
                    r.get("time_taken") or "-",
                    f"£{float(r.get('cost') or 0):,.2f}" if r.get("cost") else "-",
                    r.get("assigned_staff") or "-",
                ))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    refresh_all()
    tk.Button(tab_all, text="Refresh", bg=ACCENT, fg="white",
              relief="flat", command=refresh_all).pack(pady=5)

    root.mainloop()
