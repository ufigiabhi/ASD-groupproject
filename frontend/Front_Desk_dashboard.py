import tkinter as tk
from tkinter import messagebox
from backend.services.maintenance_service import MaintenanceService
from backend.services.tenant_service import TenantService
from backend.services.complaint_service import ComplaintService


def open_frontdesk_dashboard(username):
    maintenance_service = MaintenanceService()
    tenant_service = TenantService()
    complaint_service = ComplaintService()

    root = tk.Tk()
    root.title("Front Desk Dashboard - FULL DATABASE")
    root.geometry("1000x650")
    root.configure(bg="#f0f4f8")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    header = tk.Frame(root, bg="#0d47a1", height=50)
    header.grid(row=0, column=0, columnspan=2, sticky="ew")

    tk.Label(
        header,
        text="Front Desk Staff Panel - ALL DATA IN DATABASE",
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
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        return content

    # LEFT SIDE
    left_container = tk.Frame(root, bg="#f0f4f8")
    left_container.grid(row=1, column=0, sticky="nsew")
    left_container.grid_rowconfigure(1, weight=1)
    left_container.grid_columnconfigure(0, weight=1)

    register_frame = tk.LabelFrame(
        left_container,
        text="Register New Tenant (DATABASE)",
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
            messagebox.showwarning("Missing Data", "All fields are required")
            return

        try:
            tenant_service.register_tenant(
                tenant["Name"],
                tenant["NI Number"],
                tenant["Phone"],
                tenant["Email"],
                tenant["Apartment Type"],
                tenant["Lease Period"]
            )

            for e in fields.values():
                e.delete(0, tk.END)

            refresh_tenants()
            messagebox.showinfo("Success", "Tenant registered in database!")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        register_frame,
        text="Register Tenant",
        bg="#1976d2",
        fg="white",
        command=register_tenant
    ).pack(pady=8)

    tenants_frame = scrollable_section(left_container, "Registered Tenants (DATABASE)")
    tenants_frame.master.grid(row=1, column=0, sticky="nsew")

    def refresh_tenants():
        for widget in tenants_frame.winfo_children():
            widget.destroy()

        try:
            tenants = tenant_service.get_all_tenants()

            if not tenants:
                tk.Label(
                    tenants_frame,
                    text="No tenants registered yet",
                    bg="white",
                    fg="gray"
                ).pack(anchor="w", pady=5)
                return

            for t in tenants:
                tk.Label(
                    tenants_frame,
                    text=f"{t['name']} | {t['apartment_type']} | Lease: {t['lease_period']}",
                    bg="white",
                    font=("Helvetica", 11)
                ).pack(anchor="w", pady=2)

        except Exception as e:
            tk.Label(
                tenants_frame,
                text=f"Error: {str(e)}",
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)

    refresh_tenants()

    # RIGHT SIDE
    right_container = tk.Frame(root, bg="#f0f4f8")
    right_container.grid(row=1, column=1, sticky="nsew")
    right_container.grid_rowconfigure(0, weight=1)
    right_container.grid_rowconfigure(1, weight=1)
    right_container.grid_columnconfigure(0, weight=1)

    # MAINTENANCE
    maintenance_frame = scrollable_section(right_container, "Maintenance Requests (DATABASE)")
    maintenance_frame.master.grid(row=0, column=0, sticky="nsew")

    def refresh_maintenance():
        for widget in maintenance_frame.winfo_children():
            widget.destroy()

        try:
            requests = maintenance_service.get_all_requests()

            if not requests:
                tk.Label(
                    maintenance_frame,
                    text="No maintenance requests",
                    bg="white",
                    fg="gray"
                ).pack(anchor="w", pady=5)
                return

            for r in requests:
                text = f"Apt {r['apartment_id']} | {r['description']} | {r['priority']} | {r['status']}"
                tk.Label(
                    maintenance_frame,
                    text=text,
                    bg="white",
                    fg="#2e7d32",
                    font=("Helvetica", 11)
                ).pack(anchor="w", pady=2)

        except Exception as e:
            tk.Label(
                maintenance_frame,
                text=f"Error: {str(e)}",
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)

    refresh_maintenance()

    def add_request_popup():
        popup = tk.Toplevel(root)
        popup.title("New Maintenance Request")
        popup.geometry("350x250")

        tk.Label(popup, text="Apartment ID").pack(pady=5)
        apt_entry = tk.Entry(popup)
        apt_entry.pack(pady=5)

        tk.Label(popup, text="Description").pack(pady=5)
        desc_entry = tk.Entry(popup)
        desc_entry.pack(pady=5)

        tk.Label(popup, text="Priority").pack(pady=5)
        priority_var = tk.StringVar(value="Medium")
        tk.OptionMenu(popup, priority_var, "Low", "Medium", "High").pack(pady=5)

        def submit():
            try:
                maintenance_service.create_request(int(apt_entry.get()), desc_entry.get(), priority_var.get())
                popup.destroy()
                refresh_maintenance()
                messagebox.showinfo("Success", "Request created!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(popup, text="Submit", bg="#1976d2", fg="white", command=submit).pack(pady=15)

    tk.Button(
        right_container,
        text="Add Maintenance Request",
        bg="#1976d2",
        fg="white",
        command=add_request_popup
    ).grid(row=0, column=0, sticky="s", pady=10)

    # COMPLAINTS
    complaints_frame = scrollable_section(right_container, "Complaints (DATABASE)")
    complaints_frame.master.grid(row=1, column=0, sticky="nsew")

    def refresh_complaints():
        for widget in complaints_frame.winfo_children():
            widget.destroy()

        try:
            complaints = complaint_service.get_all_complaints()

            if not complaints:
                tk.Label(
                    complaints_frame,
                    text="No complaints",
                    bg="white",
                    fg="gray"
                ).pack(anchor="w", pady=5)
                return

            for c in complaints:
                tk.Label(
                    complaints_frame,
                    text=f"{c['tenant_name']} | {c['issue']} | {c['status']}",
                    bg="white",
                    fg="#6a1b9a",
                    font=("Helvetica", 11)
                ).pack(anchor="w", pady=2)

        except Exception as e:
            tk.Label(
                complaints_frame,
                text=f"Error: {str(e)}",
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)

    refresh_complaints()

    root.mainloop()