import tkinter as tk
from tkinter import messagebox

from backend.services.maintenance_service import MaintenanceService
from frontend import front_desk_dummy_data

def open_frontdesk_dashboard(username):
    service = MaintenanceService()

    root = tk.Tk()
    root.title("Front Desk Dashboard")
    root.geometry("1000x650")
    root.configure(bg="#f0f4f8")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    header = tk.Frame(root, bg="#0d47a1", height=50)
    header.grid(row=0, column=0, columnspan=2, sticky="ew")

    tk.Label(
        header,
        text="Front Desk Staff Panel",
        font=("Helvetica", 16, "bold"),
        bg="#0d47a1",
        fg="white"
    ).pack(side="left", padx=20)

    def logout():
        from frontend import login
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            root.destroy()
            login.run_login()

    tk.Button(
        header,
        text="Logout",
        bg="#c62828",
        fg="white",
        command=logout
    ).pack(side="right", padx=20)

    def scrollable_section(parent, title):
        frame = tk.LabelFrame(parent, text=title, bg="white", fg="#0d47a1")
        frame.grid(sticky="nsew", padx=15, pady=15)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        content = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=content, anchor="nw")

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        return content

    left_container = tk.Frame(root, bg="#f0f4f8")
    left_container.grid(row=1, column=0, sticky="nsew")

    register_frame = tk.LabelFrame(
        left_container,
        text="Register New Tenant",
        bg="white",
        fg="#0d47a1",
        padx=10,
        pady=10
    )
    register_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)

    fields = {}
    for label in ["Name", "NI Number", "Phone", "Email", "Apartment Type", "Lease Period"]:
        tk.Label(register_frame, text=label, bg="white").pack(anchor="w")
        entry = tk.Entry(register_frame)
        entry.pack(fill="x", pady=2)
        fields[label] = entry

    def register_tenant():
        tenant = {k: v.get().strip() for k, v in fields.items()}
        if "" in tenant.values():
            messagebox.showwarning("Missing Data", "All fields are required.")
            return
        front_desk_dummy_data.tenants.append(tenant)
        for e in fields.values():
            e.delete(0, tk.END)
        refresh_tenants()

    tk.Button(
        register_frame,
        text="Register Tenant",
        bg="#1976d2",
        fg="white",
        command=register_tenant
    ).pack(pady=8)

    tenants_frame = scrollable_section(left_container, "Registered Tenants")
    tenants_frame.master.grid(row=1, column=0, sticky="nsew")

    def refresh_tenants():
        for widget in tenants_frame.winfo_children():
            widget.destroy()
        for t in front_desk_dummy_data.tenants:
            tk.Label(
                tenants_frame,
                text=f"{t['Name']} | {t['Apartment Type']} | Lease: {t['Lease Period']}",
                bg="white"
            ).pack(anchor="w")

    refresh_tenants()

    right_container = tk.Frame(root, bg="#f0f4f8")
    right_container.grid(row=1, column=1, sticky="nsew")

    maintenance_frame = scrollable_section(right_container, "Maintenance Requests")
    maintenance_frame.master.grid(row=0, column=0, sticky="nsew")

    def refresh_maintenance():
        for widget in maintenance_frame.winfo_children():
            widget.destroy()

        for r in service.get_all_requests():
            tk.Label(
                maintenance_frame,
                text=f"Apt {r['apartment_id']} → {r['description']} ({r['status']})",
                bg="white",
                fg="#2e7d32"
            ).pack(anchor="w")

    refresh_maintenance()

    def add_request_popup():
        popup = tk.Toplevel(root)
        popup.title("New Maintenance Request")

        tk.Label(popup, text="Apartment ID").pack()
        apt = tk.Entry(popup)
        apt.pack()

        tk.Label(popup, text="Description").pack()
        desc = tk.Entry(popup)
        desc.pack()

        def submit():
            service.create_request(int(apt.get()), desc.get())
            popup.destroy()
            refresh_maintenance()

        tk.Button(popup, text="Submit", command=submit).pack(pady=10)

    tk.Button(
        right_container,
        text="Add Maintenance Request",
        bg="#1976d2",
        fg="white",
        command=add_request_popup
    ).grid(row=0, column=0, sticky="s", pady=10)

    complaints_frame = scrollable_section(right_container, "Complaints")
    complaints_frame.master.grid(row=1, column=0, sticky="nsew")

    def refresh_complaints():
        for widget in complaints_frame.winfo_children():
            widget.destroy()
        for c in front_desk_dummy_data.complaints:
            tk.Label(
                complaints_frame,
                text=f"{c['tenant']} → {c['issue']} ({c['status']})",
                bg="white"
            ).pack(anchor="w")

    refresh_complaints()

    root.mainloop()