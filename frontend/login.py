# ================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# File:        [FILENAME].py
# Author(s):    Esila Keskin / Abhinav Singh Rawat
# Student ID(s):  24064432 / 24027772
# Description: Login GUI - credential entry, SHA-256 authentication, role-based dashboard routing
# ================================================================
import tkinter as tk
from tkinter import messagebox
from backend.services.user_service import UserService

# Colour constants used to keep the login page styling consistent
PRIMARY = "#0d47a1"
ACCENT  = "#1976d2"
BG      = "#f0f4f8"

# Create a single user service instance to handle authentication
_user_service = UserService()


def _launch_dashboard(user: dict, root: tk.Tk):
    # Close the login window before opening the selected dashboard
    root.destroy()
    role = user["role"]

    # Open the correct dashboard based on the authenticated user's role
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
        # Show an error if the role returned from the database is not recognised
        messagebox.showerror("Error", f"Unknown role: {role}")


def run_login():
    # Main login window setup
    root = tk.Tk()
    root.title("Paragon Apartment Management System - Login")
    root.geometry("860x540")
    root.configure(bg=BG)
    root.resizable(False, False)

    # Header bar displaying the system name
    header = tk.Frame(root, bg=PRIMARY, height=70)
    header.pack(fill="x")
    tk.Label(
        header,
        text="Paragon Apartment Management System",
        font=("Helvetica", 20, "bold"),
        bg=PRIMARY, fg="white"
    ).pack(pady=18)

    # Subtitle showing the intended scope of the system
    tk.Label(
        root,
        text="Multi-City Property Management  |  Bristol · Cardiff · London · Manchester",
        font=("Helvetica", 10),
        bg=BG, fg="#546e7a"
    ).pack(pady=(12, 0))

    # Central login card containing the input fields and button
    card = tk.Frame(root, bg="white", padx=45, pady=40,
                    relief="groove", bd=1)
    card.place(relx=0.5, rely=0.58, anchor="center")

    tk.Label(
        card, text="Staff & Tenant Login",
        font=("Helvetica", 15, "bold"),
        bg="white", fg=PRIMARY
    ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Username input field
    tk.Label(card, text="Username", bg="white",
             font=("Helvetica", 11)).grid(row=1, column=0, sticky="w")
    entry_username = tk.Entry(card, font=("Helvetica", 11), width=28)
    entry_username.grid(row=2, column=0, pady=(4, 12))

    # Password input field
    tk.Label(card, text="Password", bg="white",
             font=("Helvetica", 11)).grid(row=3, column=0, sticky="w")
    entry_password = tk.Entry(card, show="*", font=("Helvetica", 11), width=28)
    entry_password.grid(row=4, column=0, pady=(4, 16))

    # Label used to show inline validation or login errors
    status_var = tk.StringVar()
    status_lbl = tk.Label(card, textvariable=status_var, bg="white",
                          fg="#c62828", font=("Helvetica", 10))
    status_lbl.grid(row=5, column=0)

    def login():
        # Read and trim the values entered by the user
        u = entry_username.get().strip()
        p = entry_password.get().strip()

        # Prevent blank login attempts
        if not u or not p:
            status_var.set("Please enter both username and password.")
            return

        try:
            # Attempt to authenticate the user through the service layer
            user = _user_service.authenticate(u, p)
        except Exception as exc:
            # Display a helpful message if the database connection fails
            messagebox.showerror(
                "Connection Error",
                f"Cannot connect to database.\n{exc}\n\n"
                "Run: python -m backend.database.setup_db"
            )
            return

        if user:
            # Clear any existing error message and open the correct dashboard
            status_var.set("")
            _launch_dashboard(user, root)
        else:
            # Show an error message and clear only the password field
            status_var.set("Invalid username or password.")
            entry_password.delete(0, tk.END)

    # Pressing Enter in the password field submits the login form
    entry_password.bind("<Return>", lambda _: login())

    # Pressing Enter in the username field moves focus to the password field
    entry_username.bind("<Return>", lambda _: entry_password.focus())

    # Login button to trigger authentication
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

    # Demo account hint shown below the login card
    hint = (
        "Roles: Admin · Manager · FrontDesk · Finance · Maintenance · Tenant\n"
        "Demo - admin1/Admin@123 · frontdesk1/Front@123 · finance1/Finance@123\n"
        "        maint1/Maint@123 · tenant1/Tenant@123 · manager1/Manager@123"
    )
    tk.Label(root, text=hint, bg=BG, fg="#78909c",
             font=("Helvetica", 9), justify="center").pack(pady=(6, 0))

    # Set the cursor focus to the username field when the page opens
    entry_username.focus()

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    # Run the login page when this file is executed directly
    run_login()
