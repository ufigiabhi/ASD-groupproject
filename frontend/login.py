import tkinter as tk
from tkinter import messagebox
from backend.services.user_service import UserService

PRIMARY = "#0d47a1"
ACCENT  = "#1976d2"
BG      = "#f0f4f8"

_user_service = UserService()


def _launch_dashboard(user: dict, root: tk.Tk):
    root.destroy()
    role = user["role"]

    if role == "Tenant":
        from frontend.tenant_dashboard import open_tenant_dashboard
        open_tenant_dashboard(user)

    elif role == "FrontDesk":
        from frontend.Front_Desk_dashboard import open_frontdesk_dashboard
        open_frontdesk_dashboard(user)

    elif role == "Finance":
        from frontend.Finance import open_Finance
        open_Finance(user)

    elif role == "Maintenance":
        from frontend.maintenance_dashboard import open_maintenance_dashboard
        open_maintenance_dashboard(user)

    elif role == "Admin":
        from frontend.admin_dashboard import open_admin_dashboard
        open_admin_dashboard(user)

    elif role == "Manager":
        from frontend.manager_dashboard import open_manager_dashboard
        open_manager_dashboard(user)

    else:
        messagebox.showerror("Error", f"Unknown role: {role}")


def run_login():
    root = tk.Tk()
    root.title("Paragon Apartment Management System - Login")
    root.geometry("860x540")
    root.configure(bg=BG)
    root.resizable(False, False)

    #   Header  
    header = tk.Frame(root, bg=PRIMARY, height=70)
    header.pack(fill="x")
    tk.Label(
        header,
        text="Paragon Apartment Management System",
        font=("Helvetica", 20, "bold"),
        bg=PRIMARY, fg="white"
    ).pack(pady=18)

    #   Subtitle  
    tk.Label(
        root,
        text="Multi-City Property Management  |  Bristol · Cardiff · London · Manchester",
        font=("Helvetica", 10),
        bg=BG, fg="#546e7a"
    ).pack(pady=(12, 0))

    #   Card  
    card = tk.Frame(root, bg="white", padx=45, pady=40,
                    relief="groove", bd=1)
    card.place(relx=0.5, rely=0.58, anchor="center")

    tk.Label(
        card, text="Staff & Tenant Login",
        font=("Helvetica", 15, "bold"),
        bg="white", fg=PRIMARY
    ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    tk.Label(card, text="Username", bg="white",
             font=("Helvetica", 11)).grid(row=1, column=0, sticky="w")
    entry_username = tk.Entry(card, font=("Helvetica", 11), width=28)
    entry_username.grid(row=2, column=0, pady=(4, 12))

    tk.Label(card, text="Password", bg="white",
             font=("Helvetica", 11)).grid(row=3, column=0, sticky="w")
    entry_password = tk.Entry(card, show="*", font=("Helvetica", 11), width=28)
    entry_password.grid(row=4, column=0, pady=(4, 16))

    status_var = tk.StringVar()
    status_lbl = tk.Label(card, textvariable=status_var, bg="white",
                          fg="#c62828", font=("Helvetica", 10))
    status_lbl.grid(row=5, column=0)

    def login():
        u = entry_username.get().strip()
        p = entry_password.get().strip()

        if not u or not p:
            status_var.set("Please enter both username and password.")
            return

        try:
            user = _user_service.authenticate(u, p)
        except Exception as exc:
            messagebox.showerror(
                "Connection Error",
                f"Cannot connect to database.\n{exc}\n\n"
                "Run: python -m backend.database.setup_db"
            )
            return

        if user:
            status_var.set("")
            _launch_dashboard(user, root)
        else:
            status_var.set("Invalid username or password.")
            entry_password.delete(0, tk.END)

    entry_password.bind("<Return>", lambda _: login())
    entry_username.bind("<Return>", lambda _: entry_password.focus())

    tk.Button(
        card,
        text="Login",
        bg=ACCENT, fg="white",
        font=("Helvetica", 11, "bold"),
        relief="flat",
        width=26,
        cursor="hand2",
        command=login
    ).grid(row=6, column=0, pady=(6, 0))

    #   Hint  
    hint = (
        "Roles: Admin · Manager · FrontDesk · Finance · Maintenance · Tenant\n"
        "Demo - admin1/Admin@123 · frontdesk1/Front@123 · finance1/Finance@123\n"
        "        maint1/Maint@123 · tenant1/Tenant@123 · manager1/Manager@123"
    )
    tk.Label(root, text=hint, bg=BG, fg="#78909c",
             font=("Helvetica", 9), justify="center").pack(pady=(6, 0))

    entry_username.focus()
    root.mainloop()


if __name__ == "__main__":
    run_login()
