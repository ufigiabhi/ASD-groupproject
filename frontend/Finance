import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from datetime import datetime, timedelta
from backend.models.invoice import Invoice
from backend.models.payment import Payment

FONT_HEADER = ("Helvetica", 16, "bold")
FONT_BODY = ("Helvetica", 12)

# ----- TEST PAYMENT DATA (same idea as test_payments.py) -----

invoice1 = Invoice("INV001", "T001", 1200, datetime.now() + timedelta(days=5))
invoice2 = Invoice("INV002", "T002", 800, datetime.now() - timedelta(days=3))
invoice3 = Invoice("INV003", "T003", 1500, datetime.now() + timedelta(days=10))

payment1 = Payment("PAY001", 1200, "Card")
invoice1.add_payment(payment1)

invoices = [invoice1, invoice2, invoice3]

def calculate_finances():
    pending = 0
    paid = 0
    expected = 0

    for invoice in invoices:
        total_paid = sum(p.amount for p in invoice.payments)
        remaining = invoice.amount - total_paid

        if invoice.status == "PAID":
            paid += invoice.amount

        elif invoice.is_overdue():
            pending += remaining

        else:
            expected += remaining

    return pending, paid, expected

graph_section = section(root, "Finance Overview")

def draw_graph():
    # clear old graph
    for widget in graph_section.winfo_children():
        widget.destroy()

    pending, paid, expected = calculate_finances()

    categories = ["Pending", "Paid", "Expected"]
    values = [pending, paid, expected]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(categories, values)

    ax.set_title("Payments Overview")
    ax.set_ylabel("Amount")

    canvas = FigureCanvasTkAgg(fig, master=graph_section)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

tk.Button(
    root,
    text="Load Finance Graph",
    bg="#1976d2",
    fg="white",
    command=draw_graph
).pack(pady=10)

def finance_manager_page(username):
    root = tk.Tk()
    root.title(f"Finance Dashboard - {username}")
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
    
    root.mainloop()
