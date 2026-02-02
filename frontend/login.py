# login.py
import tkinter as tk
from tkinter import messagebox
from tenant_dashboard import open_tenant_dashboard  # import dashboard function

# Simulated users
USERS = {
    "tenant1": {"password": "pass123", "role": "Tenant"},
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
            if role == "Tenant":
                messagebox.showinfo("Login Successful", f"Welcome {username}!\nRole: {role}")
                root.destroy()  # Close login
                open_tenant_dashboard(username)  # Open tenant dashboard
            else:
                messagebox.showinfo("Login", f"Role '{role}' not implemented yet")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # Header
    header = tk.Label(root, text="Paragon Apartment Management System",
                      font=("Helvetica", 18, "bold"), bg="#0d47a1", fg="white", pady=15)
    header.pack(fill="x")

    # Login frame
    login_frame = tk.Frame(root, bg="white", padx=30, pady=30)
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(login_frame, text="Login", font=("Helvetica", 16, "bold"), bg="white", fg="#0d47a1").pack(pady=10)
    tk.Label(login_frame, text="Username:", bg="white", font=("Helvetica", 12)).pack(anchor="w", pady=(10,0))
    entry_username = tk.Entry(login_frame, font=("Helvetica", 12))
    entry_username.pack(fill="x", pady=5)
    tk.Label(login_frame, text="Password:", bg="white", font=("Helvetica", 12)).pack(anchor="w", pady=(10,0))
    entry_password = tk.Entry(login_frame, show="*", font=("Helvetica", 12))
    entry_password.pack(fill="x", pady=5)
    tk.Button(login_frame, text="Login", bg="#1976d2", fg="white", font=("Helvetica", 12, "bold"), command=login).pack(fill="x", pady=20)

    root.mainloop()


if __name__ == "__main__":
    run_login()
