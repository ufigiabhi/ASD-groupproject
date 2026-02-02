import tkinter as tk
from tkinter import messagebox

def open_tenant_dashboard(username):
    root = tk.Tk()
    root.title(f"Tenant Dashboard - {username}")
    root.geometry("700x650")
    root.configure(bg="#f0f4f8")
    root.resizable(False, False)

    # HEADER
    header = tk.Frame(root, bg="#0d47a1", height=50)
    header.pack(fill="x")

    tk.Label(
        header, text=f"Welcome, {username}",
        font=("Helvetica", 16, "bold"),
        bg="#0d47a1", fg="white"
    ).pack(side="left", padx=20)

    def logout():
        import login
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            root.destroy()
            login.run_login()

    tk.Button(
        header, text="Logout",
        bg="#c62828", fg="white",
        font=("Helvetica", 11, "bold"),
        command=logout
    ).pack(side="right", padx=20)

    #  Scroll
    def scrollable_section(parent, title):
        outer = tk.LabelFrame(parent, text=title, bg="white", fg="#0d47a1")
        outer.pack(fill="both", expand=True, padx=20, pady=10)

        canvas = tk.Canvas(outer, bg="white", height=130, highlightthickness=0)
        scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        content = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=content, anchor="nw")

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return content

    #PAYMENTS
    payments = [
        {"month": "Jan", "amount": 750, "status": "Paid"},
        {"month": "Feb", "amount": 750, "status": "Pending"},
    ]

    payments_frame = scrollable_section(root, "Payments")

    for p in payments:
        colour = "#2e7d32" if p["status"] == "Paid" else "#c62828"
        tk.Label(
            payments_frame,
            text=f"{p['month']} - £{p['amount']} ({p['status']})",
            fg=colour, bg="white", font=("Helvetica", 12)
        ).pack(anchor="w")

    # MAINTENANCE
    maintenance_requests = []

    maintenance_frame = scrollable_section(root, "Maintenance Requests")
    maintenance_list = tk.Frame(maintenance_frame, bg="white")
    maintenance_list.pack(fill="x")

    def refresh_maintenance():
        for widget in maintenance_list.winfo_children():
            widget.destroy()
        for r in maintenance_requests:
            tk.Label(
                maintenance_list,
                text=f"{r['issue']} - {r['status']}",
                bg="white", fg="#2e7d32",
                font=("Helvetica", 12)
            ).pack(anchor="w")

    maintenance_entry = tk.Entry(maintenance_frame, font=("Helvetica", 12))
    maintenance_entry.pack(fill="x", pady=5)

    def add_maintenance():
        text = maintenance_entry.get().strip()
        if not text:
            messagebox.showwarning("Input required", "Please enter a request")
            return
        maintenance_requests.append({"issue": text, "status": "Open"})
        maintenance_entry.delete(0, tk.END)
        refresh_maintenance()

    tk.Button(
        maintenance_frame, text="Submit Maintenance Request",
        bg="#1976d2", fg="white",
        font=("Helvetica", 11),
        command=add_maintenance
    ).pack(pady=5)

    #COMPLAINTS
    complaints = []

    complaint_frame = scrollable_section(root, "Complaints")
    complaint_list = tk.Frame(complaint_frame, bg="white")
    complaint_list.pack(fill="x")

    def refresh_complaints():
        for widget in complaint_list.winfo_children():
            widget.destroy()
        for c in complaints:
            tk.Label(
                complaint_list,
                text=f"{c['issue']} - {c['status']}",
                bg="white", fg="#2e7d32",
                font=("Helvetica", 12)
            ).pack(anchor="w")

    complaint_entry = tk.Entry(complaint_frame, font=("Helvetica", 12))
    complaint_entry.pack(fill="x", pady=5)

    def add_complaint():
        text = complaint_entry.get().strip()
        if not text:
            messagebox.showwarning("Input required", "Please enter a complaint")
            return
        complaints.append({"issue": text, "status": "Open"})
        complaint_entry.delete(0, tk.END)
        refresh_complaints()

    tk.Button(
        complaint_frame, text="Submit Complaint",
        bg="#1976d2", fg="white",
        font=("Helvetica", 11),
        command=add_complaint
    ).pack(pady=5)

    root.mainloop()
