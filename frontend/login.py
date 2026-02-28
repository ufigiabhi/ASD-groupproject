import tkinter as tk
from tkinter import messagebox
from frontend.tenant_dashboard import open_tenant_dashboard
from frontend.Front_Desk_dashboard import open_frontdesk_dashboard

USERS = {
    "tenant1": {"password": "pass123", "role": "Tenant"},
    "frontdesk1": {"password": "pass456", "role": "FrontDesk"},
}

PRIMARY = "#0d47a1"
ACCENT = "#1976d2"
BG = "#f0f4f8"

def run_login():
    root = tk.Tk()
    root.title("Paragon Apartment Management System")
    root.geometry("820x520")
    root.configure(bg=BG)
    root.resizable(False, False)

    header = tk.Frame(root, bg=PRIMARY, height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Paragon Apartment Management System",
        font=("Helvetica", 20, "bold"),
        bg=PRIMARY,
        fg="white"
    ).pack(pady=18)

    card = tk.Frame(root, bg="white", padx=40, pady=35)
    card.place(relx=0.5, rely=0.55, anchor="center")

    tk.Label(
        card, text="System Login",
        font=("Helvetica", 16, "bold"),
        bg="white", fg=PRIMARY
    ).pack(pady=(0, 20))

    tk.Label(card, text="Username", bg="white", font=("Helvetica", 11)).pack(anchor="w")
    entry_username = tk.Entry(card, font=("Helvetica", 11), width=30)
    entry_username.pack(pady=6)

    tk.Label(card, text="Password", bg="white", font=("Helvetica", 11)).pack(anchor="w")
    entry_password = tk.Entry(card, show="*", font=("Helvetica", 11), width=30)
    entry_password.pack(pady=6)

    def login():
        u = entry_username.get().strip()
        p = entry_password.get().strip()

        if u in USERS and USERS[u]["password"] == p:
            role = USERS[u]["role"]
            messagebox.showinfo("Login Successful", f"Welcome {u}")
            root.destroy()
            if role == "Tenant":
                open_tenant_dashboard(u)
            else:
                open_frontdesk_dashboard(u)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Button(
        card,
        text="Login",
        bg=ACCENT,
        fg="white",
        font=("Helvetica", 11, "bold"),
        relief="flat",
        width=25,
        command=login
    ).pack(pady=18)

    root.mainloop()

if __name__ == "__main__":
    run_login()