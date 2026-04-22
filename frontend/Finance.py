import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

from backend.services.invoice_service import InvoiceService
from backend.services.payment_service import PaymentService
from backend.services.tenant_service import TenantService
# simple colouring. ^ adding the backend stuff.
PRIMARY = "#0d47a1"
ACCENT  = "#1976d2"
BG      = "#f0f4f8"

MONTHS      = ["All", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
MONTH_NUMS  = {name: idx for idx, name in enumerate(MONTHS)}   # "All"→0, "January"→1 …
YEARS       = ["All"] + [str(y) for y in range(2024, 2028)]

# mainly cosmetic/visual appearance.
def open_Finance(user: dict):
    username = user["full_name"] if isinstance(user, dict) else str(user)

    invoice_svc = InvoiceService()
    payment_svc = PaymentService()
    tenant_svc  = TenantService()

    root = tk.Tk()
    root.title(f"Finance Dashboard - {username}")
    root.geometry("1050x720")
    root.configure(bg=BG)

    #  Header 
    header = tk.Frame(root, bg=PRIMARY, height=52)
    header.pack(fill="x")
    tk.Label(header, text=f"Finance Manager - {username}",
             font=("Helvetica", 15, "bold"), bg=PRIMARY, fg="white"
             ).pack(side="left", padx=20, pady=10)
# Using the same technique to logout as most other pages
    def logout():
        from frontend import login
        if messagebox.askyesno("Logout", "Are you sure?"):
            root.destroy()
            login.run_login()

    tk.Button(header, text="Logout", bg="#c62828", fg="white",
              font=("Helvetica", 10, "bold"), relief="flat",
              command=logout).pack(side="right", padx=15, pady=10)

    #  Notebook 
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=10, pady=10)

    # TAB 1 - Overview
    tab_overview = tk.Frame(nb, bg="white")
    nb.add(tab_overview, text="  Overview  ")

    # Filter bar
    filter_frame = tk.Frame(tab_overview, bg="white")
    filter_frame.pack(fill="x", padx=20, pady=(15, 5))

    tk.Label(filter_frame, text="Filter by:", bg="white",
             font=("Helvetica", 11)).pack(side="left")
    tk.Label(filter_frame, text="Month", bg="white",
             font=("Helvetica", 10)).pack(side="left", padx=(15, 3))

    sel_month = ttk.Combobox(filter_frame, values=MONTHS, state="readonly", width=13)
    sel_month.set("All")
    sel_month.pack(side="left")

    tk.Label(filter_frame, text="Year", bg="white",
             font=("Helvetica", 10)).pack(side="left", padx=(12, 3))
    sel_year = ttk.Combobox(filter_frame, values=YEARS, state="readonly", width=8)
    sel_year.set(str(datetime.now().year))
    sel_year.pack(side="left")

    canvas_holder = tk.Frame(tab_overview, bg="white")
    canvas_holder.pack(fill="both", expand=True, padx=20, pady=5)

    summary_frame = tk.Frame(tab_overview, bg="white")
    summary_frame.pack(fill="x", padx=20, pady=5)
# does
    def draw_overview():
        m_name = sel_month.get()
        y_str  = sel_year.get()
        m = MONTH_NUMS.get(m_name, 0)
        y = int(y_str) if y_str != "All" else None

        try:
            if m and y:
                summary = payment_svc.get_financial_summary(m, y)
            elif y:
                summary = payment_svc.get_financial_summary(year=y)
            else:
                summary = payment_svc.get_financial_summary()
        except Exception as exc:
            messagebox.showerror("DB Error", str(exc))
            return
# should show money needed and paid for tables and general.
        collected = float(summary["collected"] or 0)
        pending   = float(summary["pending"]   or 0)
        overdue   = float(summary["overdue"]   or 0)

        # Clear old widgets
        for w in canvas_holder.winfo_children():
            w.destroy()
        for w in summary_frame.winfo_children():
            w.destroy()

        # Bar chart
        fig, ax = plt.subplots(figsize=(6, 3.5))
        bars = ax.bar(["Collected", "Pending", "Overdue"],
                      [collected, pending, overdue],
                      color=["#2e7d32", "#1976d2", "#c62828"])
        ax.set_title("Payment Overview")
        ax.set_ylabel("Amount (£)")
        for bar, val in zip(bars, [collected, pending, overdue]):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 10,
                    f"£{val:,.2f}", ha="center", va="bottom", fontsize=9)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=canvas_holder)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

        # Summary labels
        period = f"{m_name} {y_str}" if m_name != "All" else "All Time"
        for text, colour in [
            (f"Period: {period}", "#333"),
            (f"Collected: £{collected:,.2f}", "#2e7d32"),
            (f"Pending: £{pending:,.2f}", "#1976d2"),
            (f"Overdue: £{overdue:,.2f}", "#c62828"),
            (f"Total Invoices: {summary.get('total_invoices',0)}", "#555"),
        ]:
            tk.Label(summary_frame, text=text, bg="white", fg=colour,
                     font=("Helvetica", 11)).pack(anchor="w")

    tk.Button(filter_frame, text="Load Overview", bg=ACCENT, fg="white",
              relief="flat", font=("Helvetica", 10, "bold"),
              command=draw_overview).pack(side="left", padx=12)

    draw_overview()

    # TAB 2 - Invoices
    tab_inv = tk.Frame(nb, bg="white")
    nb.add(tab_inv, text="  Invoices  ")

    # Filter bar
    inv_filter = tk.Frame(tab_inv, bg="white")
    inv_filter.pack(fill="x", padx=20, pady=(15, 5))
    tk.Label(inv_filter, text="Month:", bg="white").pack(side="left")
    inv_month = ttk.Combobox(inv_filter, values=MONTHS, state="readonly", width=13)
    inv_month.set("All"); inv_month.pack(side="left", padx=(5, 10))
    tk.Label(inv_filter, text="Year:", bg="white").pack(side="left")
    inv_year = ttk.Combobox(inv_filter, values=YEARS, state="readonly", width=8)
    inv_year.set(str(datetime.now().year)); inv_year.pack(side="left", padx=5)

    cols_i = ("ID", "Tenant", "Amount", "Month", "Year",
              "Due Date", "Status")
    tree_i = ttk.Treeview(tab_inv, columns=cols_i, show="headings", height=18)
    for c in cols_i:
        tree_i.heading(c, text=c)
        tree_i.column(c, width=120, anchor="w")
    tree_i.pack(fill="both", expand=True, padx=20, pady=5)

    tag_colours = {
        "paid": "#c8e6c9", "overdue": "#ffcdd2",
        "unpaid": "#fff9c4", "partial": "#ffe0b2"
    }
    for tag, colour in tag_colours.items():
        tree_i.tag_configure(tag, background=colour)

    def refresh_invoices():
        for row in tree_i.get_children():
            tree_i.delete(row)
        m_name = inv_month.get()
        y_str  = inv_year.get()
        m = MONTH_NUMS.get(m_name, 0)
        y = int(y_str) if y_str != "All" else None

        try:
            if m and y:
                rows = invoice_svc.get_invoices_by_month_year(m, y)
            else:
                rows = invoice_svc.get_all_invoices()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        for r in rows:
            status = r.get("status", "unpaid")
            tree_i.insert("", "end", tags=(status,), values=(
                r.get("id"),
                r.get("tenant_name"),
                f"£{float(r.get('amount', 0)):,.2f}",
                MONTHS[r.get("month", 1)],
                r.get("year"),
                str(r.get("due_date", "")),
                status.upper(),
            ))

    tk.Button(inv_filter, text="Search", bg=ACCENT, fg="white",
              relief="flat", command=refresh_invoices).pack(side="left", padx=10)
    refresh_invoices()

    # TAB 3 - Payments
    tab_pay = tk.Frame(nb, bg="white")
    nb.add(tab_pay, text="  Payments  ")

    pay_filter = tk.Frame(tab_pay, bg="white")
    pay_filter.pack(fill="x", padx=20, pady=(15, 5))
    tk.Label(pay_filter, text="Month:", bg="white").pack(side="left")
    pay_month = ttk.Combobox(pay_filter, values=MONTHS, state="readonly", width=13)
    pay_month.set("All"); pay_month.pack(side="left", padx=(5, 10))
    tk.Label(pay_filter, text="Year:", bg="white").pack(side="left")
    pay_year = ttk.Combobox(pay_filter, values=YEARS, state="readonly", width=8)
    pay_year.set(str(datetime.now().year)); pay_year.pack(side="left", padx=5)

    cols_p = ("ID", "Tenant", "Invoice", "Amount", "Month",
              "Date", "Method", "Late Fee", "Receipt")
    tree_p = ttk.Treeview(tab_pay, columns=cols_p, show="headings", height=18)
    for c in cols_p:
        tree_p.heading(c, text=c)
        tree_p.column(c, width=110, anchor="w")
    tree_p.pack(fill="both", expand=True, padx=20, pady=5)

    def refresh_payments():
        for row in tree_p.get_children():
            tree_p.delete(row)
        m_name = pay_month.get()
        y_str  = pay_year.get()
        m = MONTH_NUMS.get(m_name, 0)
        y = int(y_str) if y_str != "All" else None

        try:
            if m and y:
                rows = payment_svc.get_payments_by_month_year(m, y)
            else:
                rows = payment_svc.get_all_payments()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        for r in rows:
            tree_p.insert("", "end", values=(
                r.get("id"),
                r.get("tenant_name"),
                r.get("invoice_id"),
                f"£{float(r.get('amount', 0)):,.2f}",
                MONTHS[r.get("month", 1)],
                str(r.get("payment_date", ""))[:16],
                r.get("method"),
                f"£{float(r.get('late_fee', 0)):,.2f}",
                r.get("receipt_number"),
            ))

    tk.Button(pay_filter, text="Search", bg=ACCENT, fg="white",
              relief="flat", command=refresh_payments).pack(side="left", padx=10)
    refresh_payments()

    # TAB 4 - Record Payment
    tab_rec = tk.Frame(nb, bg="white")
    nb.add(tab_rec, text="  Record Payment  ")

    tk.Label(tab_rec, text="Record a Rent Payment",
             font=("Helvetica", 14, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(20, 10), padx=25, anchor="w")

    rec_frame = tk.Frame(tab_rec, bg="white", padx=25)
    rec_frame.pack(anchor="nw")

    def lbl(txt): tk.Label(rec_frame, text=txt, bg="white",
                            font=("Helvetica", 10)).pack(anchor="w", pady=(8, 1))
    def ent(w=30):
        e = tk.Entry(rec_frame, width=w, font=("Helvetica", 10))
        e.pack(anchor="w")
        return e

    lbl("Invoice ID *")
    rec_inv_id = ent()
    lbl("Tenant ID *")
    rec_ten_id = ent()
    lbl("Amount Paid (£) *")
    rec_amount = ent()
    lbl("Payment Method *")
    rec_method_var = tk.StringVar(value="Card")
    ttk.Combobox(rec_frame, textvariable=rec_method_var,
                 values=["Card", "Bank Transfer", "Cash"],
                 state="readonly", width=28).pack(anchor="w")
    lbl("Late Fee (£)")
    rec_late = ent()
    rec_late.insert(0, "0.00")

    result_var = tk.StringVar()
    tk.Label(tab_rec, textvariable=result_var, bg="white",
             fg="#2e7d32", font=("Helvetica", 11, "bold")).pack(pady=5)

    def record_payment():
        try:
            inv_id   = int(rec_inv_id.get().strip())
            ten_id   = int(rec_ten_id.get().strip())
            amount   = float(rec_amount.get().strip())
            late_fee = float(rec_late.get().strip() or "0")
        except ValueError:
            messagebox.showerror("Invalid", "Invoice ID, Tenant ID and Amount must be numbers.")
            return
        try:
            pid, receipt = payment_svc.record_payment(
                inv_id, ten_id, amount, rec_method_var.get(), late_fee
            )
            result_var.set(f"Payment recorded! Receipt: {receipt}")
            refresh_invoices()
            refresh_payments()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(tab_rec, text="Record Payment", bg="#2e7d32", fg="white",
              font=("Helvetica", 11, "bold"), relief="flat",
              command=record_payment).pack(pady=15)

    # TAB 5 - Overdue Alerts
    tab_late = tk.Frame(nb, bg="white")
    nb.add(tab_late, text="  Overdue Alerts  ")

    tk.Label(tab_late, text="Overdue Invoices",
             font=("Helvetica", 14, "bold"), bg="white", fg="#c62828"
             ).pack(pady=(20, 5), padx=20, anchor="w")

    cols_l = ("Invoice ID", "Tenant", "Email", "Phone",
              "Amount", "Due Date")
    tree_l = ttk.Treeview(tab_late, columns=cols_l, show="headings", height=16)
    for c in cols_l:
        tree_l.heading(c, text=c)
        tree_l.column(c, width=140, anchor="w")
    tree_l.pack(fill="both", expand=True, padx=20, pady=5)
    tree_l.tag_configure("overdue", background="#ffcdd2")

    def refresh_overdue():
        for row in tree_l.get_children():
            tree_l.delete(row)
        try:
            for r in invoice_svc.get_overdue_invoices():
                tree_l.insert("", "end", tags=("overdue",), values=(
                    r.get("id"),
                    r.get("tenant_name"),
                    r.get("email", ""),
                    r.get("phone", ""),
                    f"£{float(r.get('amount', 0)):,.2f}",
                    str(r.get("due_date", "")),
                ))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(tab_late, text="Refresh Overdue", bg="#c62828", fg="white",
              relief="flat", command=refresh_overdue).pack(pady=8)
    refresh_overdue()

    root.mainloop()
