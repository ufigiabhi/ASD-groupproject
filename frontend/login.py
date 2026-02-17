import tkinter as tk
from tkinter import messagebox

from frontend.tenant_dashboard import open_tenant_dashboard
from frontend.Front_Desk_dashboard import open_frontdesk_dashboard

# Simulated users
USERS = {
    "tenant1": {"password": "pass123", "role": "Tenant"},
    "frontdesk1": {"password": "pass456", "role": "FrontDesk"},
}

def run_login():
    root = tk.Tk()
    root.title("PAMS Login")
    root.geometry("800x500")
    root.configure(bg="#f0f4f8")
    root.resizable(False, False)

    def login():
        username = entry_username.get()
        password = entry_password.get()

        if username in USERS and USERS[username]["password"] == password:
            role = USERS[username]["role"]
            messagebox.showinfo("Login Successful", f"Welcome {username}!\nRole: {role}")
            root.destroy()

            if role == "Tenant":
                open_tenant_dashboard(username)
            elif role == "FrontDesk":
                open_frontdesk_dashboard(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    header = tk.Label(
        root,
        text="Paragon Apartment Management System",
        font=("Helvetica", 18, "bold"),
        bg="#0d47a1",
        fg="white",
        pady=15
    )
    header.pack(fill="x")

    login_frame = tk.Frame(root, bg="white", padx=30, pady=30)
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(login_frame, text="Login", font=("Helvetica", 16, "bold"),
             bg="white", fg="#0d47a1").pack(pady=10)

    tk.Label(login_frame, text="Username:", bg="white").pack(anchor="w")
    entry_username = tk.Entry(login_frame)
    entry_username.pack(fill="x")

    tk.Label(login_frame, text="Password:", bg="white").pack(anchor="w", pady=(10, 0))
    entry_password = tk.Entry(login_frame, show="*")
    entry_password.pack(fill="x")

    tk.Button(login_frame, text="Login", bg="#1976d2", fg="white",
              command=login).pack(fill="x", pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_login()