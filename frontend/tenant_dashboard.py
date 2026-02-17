import tkinter as tk
from tkinter import messagebox

FONT_HEADER = ("Helvetica", 16, "bold")
FONT_BODY = ("Helvetica", 12)

def open_tenant_dashboard(username):
    root = tk.Tk()
    root.title(f"Tenant Dashboard - {username}")
    root.geometry("700x650")
    root.configure(bg="#f0f4f8")
    root.minsize(650, 600)

    # Header
    header = tk.Frame(root, bg="#0d47a1", height=50)
    header.pack(fill="x")

    tk.Label(
        header,
        text=f"Welcome, {username}",
        font=FONT_HEADER,
        bg="#0d47a1",
        fg="white"
    ).pack(side="left", padx=20)

    def logout():
        import frontend.login as login
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            root.destroy()
            login.run_login()

    tk.Button(
        header,
        text="Logout",
        bg="#c62828",
        fg="white",
        font=("Helvetica", 11, "bold"),
        relief="flat",
        command=logout
    ).pack(side="right", padx=20)

    def section(parent, title):
        frame = tk.LabelFrame(parent, text=title, bg="white", fg="#0d47a1")
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        return frame

    # Payments
    payments = [
        {"month": "Jan", "amount": 750, "status": "Paid"},
        {"month": "Feb", "amount": 750, "status": "Pending"},
    ]

    payments_frame = section(root, "Payments")

    for p in payments:
        colour = "#2e7d32" if p["status"] == "Paid" else "#c62828"
        tk.Label(
            payments_frame,
            text=f"{p['month']} - £{p['amount']} ({p['status']})",
            fg=colour,
            bg="white",
            font=FONT_BODY
        ).pack(anchor="w", pady=2)

    # Maintenance
    maintenance_requests = []
    maintenance_frame = section(root, "Maintenance Requests")

    entry = tk.Entry(maintenance_frame, font=FONT_BODY)
    entry.pack(fill="x", pady=5)

    def add_maintenance():
        text = entry.get().strip()
        if not text:
            messagebox.showwarning("Input required", "Please enter a request")
            return
        maintenance_requests.append({"issue": text, "status": "Open"})
        entry.delete(0, tk.END)
        refresh()

    tk.Button(
        maintenance_frame,
        text="Submit Maintenance Request",
        bg="#1976d2",
        fg="white",
        relief="flat",
        command=add_maintenance
    ).pack(pady=5)

    def refresh():
        for w in maintenance_frame.pack_slaves():
            if isinstance(w, tk.Label) and "£" not in w.cget("text"):
                w.destroy()
        for r in maintenance_requests:
            tk.Label(
                maintenance_frame,
                text=f"{r['issue']} ({r['status']})",
                bg="white",
                fg="#2e7d32",
                font=FONT_BODY
            ).pack(anchor="w")

    root.mainloop()