import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from backend.services.report_service import ReportService
from backend.services.apartment_service import ApartmentService
from backend.services.lease_service import LeaseService
from backend.services.payment_service import PaymentService

PRIMARY = "#0d47a1"
ACCENT  = "#1976d2"
BG      = "#f0f4f8"

CITIES  = ["All", "Bristol", "Cardiff", "London", "Manchester"]
MONTHS  = ["All", "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"]
MONTH_NUMS = {name: idx for idx, name in enumerate(MONTHS)}
YEARS   = ["All"] + [str(y) for y in range(2024, 2028)]


def open_manager_dashboard(user: dict):
    username = user["full_name"] if isinstance(user, dict) else str(user)

    report_svc = ReportService()
    apt_svc    = ApartmentService()
    lease_svc  = LeaseService()
    pay_svc    = PaymentService()

    root = tk.Tk()
    root.title(f"Manager Dashboard - {username}")
    root.geometry("1100x720")
    root.configure(bg=BG)

    #   Header  
    header = tk.Frame(root, bg=PRIMARY, height=52)
    header.pack(fill="x")
    tk.Label(header, text=f"Manager - {username}  |  Multi-City Overview",
             font=("Helvetica", 15, "bold"), bg=PRIMARY, fg="white"
             ).pack(side="left", padx=20, pady=10)

    def logout():
        from frontend import login
        if messagebox.askyesno("Logout", "Are you sure?"):
            root.destroy()
            login.run_login()

    tk.Button(header, text="Logout", bg="#c62828", fg="white",
              font=("Helvetica", 10, "bold"), relief="flat",
              command=logout).pack(side="right", padx=15, pady=10)

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=10, pady=10)

    # TAB 1 - Occupancy Overview
    tab_occ = tk.Frame(nb, bg="white")
    nb.add(tab_occ, text="  Occupancy Overview  ")

    filter_f = tk.Frame(tab_occ, bg="white")
    filter_f.pack(fill="x", padx=20, pady=(15, 5))
    tk.Label(filter_f, text="City:", bg="white").pack(side="left")
    city_var = ttk.Combobox(filter_f, values=CITIES, state="readonly", width=14)
    city_var.set("All"); city_var.pack(side="left", padx=8)

    occ_chart_frame = tk.Frame(tab_occ, bg="white")
    occ_chart_frame.pack(fill="both", expand=True, padx=20, pady=5)

    def draw_occupancy():
        city = city_var.get()
        try:
            data = report_svc.occupancy_report(city if city != "All" else None)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        for w in occ_chart_frame.winfo_children():
            w.destroy()

        if not data:
            tk.Label(occ_chart_frame, text="No data.", bg="white").pack()
            return

        cities   = [r["city"] for r in data]
        occupied = [int(r.get("occupied") or 0) for r in data]
        avail    = [int(r.get("available") or 0) for r in data]
        maint    = [int(r.get("under_maintenance") or 0) for r in data]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.8))

        x = range(len(cities))
        w = 0.25
        ax1.bar([i - w for i in x], occupied, w, label="Occupied",  color="#1976d2")
        ax1.bar(x,                  avail,    w, label="Available", color="#2e7d32")
        ax1.bar([i + w for i in x], maint,    w, label="Maintenance", color="#c62828")
        ax1.set_xticks(list(x))
        ax1.set_xticklabels(cities, fontsize=8)
        ax1.set_title("Units by Status per City")
        ax1.legend(fontsize=8)

        pcts = [float(r.get("occupancy_pct") or 0) for r in data]
        ax2.bar(cities, pcts, color=["#1976d2", "#2e7d32", "#e65100", "#6a1b9a"][:len(cities)])
        ax2.set_ylim(0, 100)
        ax2.set_title("Occupancy Rate (%)")
        ax2.set_ylabel("%")
        for bar, pct in zip(ax2.patches, pcts):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                     f"{pct:.1f}%", ha="center", fontsize=8)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=occ_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    tk.Button(filter_f, text="Load Chart", bg=ACCENT, fg="white",
              relief="flat", command=draw_occupancy).pack(side="left", padx=8)
    draw_occupancy()

    # TAB 2 - Financial Reports
    tab_fin = tk.Frame(nb, bg="white")
    nb.add(tab_fin, text="  Financial Reports  ")

    fin_filter = tk.Frame(tab_fin, bg="white")
    fin_filter.pack(fill="x", padx=20, pady=(15, 5))

    tk.Label(fin_filter, text="Month:", bg="white").pack(side="left")
    fin_month = ttk.Combobox(fin_filter, values=MONTHS, state="readonly", width=13)
    fin_month.set("All"); fin_month.pack(side="left", padx=(5, 10))
    tk.Label(fin_filter, text="Year:", bg="white").pack(side="left")
    fin_year = ttk.Combobox(fin_filter, values=YEARS, state="readonly", width=8)
    fin_year.set("All"); fin_year.pack(side="left", padx=5)

    fin_chart_frame = tk.Frame(tab_fin, bg="white")
    fin_chart_frame.pack(fill="both", expand=True, padx=20, pady=5)
    fin_text_frame = tk.Frame(tab_fin, bg="white")
    fin_text_frame.pack(fill="x", padx=20, pady=5)

    def draw_financial():
        m_name = fin_month.get()
        y_str  = fin_year.get()
        m = MONTH_NUMS.get(m_name, 0)
        y = int(y_str) if y_str != "All" else None

        try:
            if m and y:
                summary = pay_svc.get_financial_summary(m, y)
            else:
                summary = pay_svc.get_financial_summary()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        for w in fin_chart_frame.winfo_children():
            w.destroy()
        for w in fin_text_frame.winfo_children():
            w.destroy()

        collected = float(summary.get("collected") or 0)
        pending   = float(summary.get("pending")   or 0)
        overdue   = float(summary.get("overdue")   or 0)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
        labels = ["Collected", "Pending", "Overdue"]
        values = [collected, pending, overdue]
        ax1.bar(labels, values, color=["#2e7d32", "#1976d2", "#c62828"])
        ax1.set_title("Revenue Summary")
        ax1.set_ylabel("£")
        for bar, val in zip(ax1.patches, values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                     f"£{val:,.0f}", ha="center", fontsize=9)

        total = sum(values)
        if total > 0:
            ax2.pie(values, labels=labels, autopct="%1.1f%%",
                    colors=["#2e7d32", "#1976d2", "#c62828"], startangle=90)
            ax2.set_title("Revenue Split")
        else:
            ax2.text(0.5, 0.5, "No data", ha="center", transform=ax2.transAxes)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=fin_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

        period = f"{m_name} {y_str}" if m_name != "All" else "All Time"
        tk.Label(fin_text_frame,
                 text=f"Period: {period}   |   Collected: £{collected:,.2f}   "
                      f"|   Pending: £{pending:,.2f}   |   Overdue: £{overdue:,.2f}",
                 bg="white", font=("Helvetica", 11)).pack(pady=5)

    tk.Button(fin_filter, text="Load Report", bg=ACCENT, fg="white",
              relief="flat", command=draw_financial).pack(side="left", padx=10)
    draw_financial()

    # TAB 3 - Maintenance Costs
    tab_mc = tk.Frame(nb, bg="white")
    nb.add(tab_mc, text="  Maintenance Costs  ")

    mc_chart_frame = tk.Frame(tab_mc, bg="white")
    mc_chart_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def draw_mc():
        for w in mc_chart_frame.winfo_children():
            w.destroy()
        try:
            data = report_svc.maintenance_cost_report()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        cities = [r["city"] for r in data]
        costs  = [float(r.get("total_cost") or 0) for r in data]
        reqs   = [int(r.get("total_requests") or 0) for r in data]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
        ax1.bar(cities, costs, color="#e65100")
        ax1.set_title("Total Maintenance Cost by City (£)")
        ax1.set_ylabel("£")
        for bar, c in zip(ax1.patches, costs):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                     f"£{c:,.0f}", ha="center", fontsize=8)

        ax2.bar(cities, reqs, color="#6a1b9a")
        ax2.set_title("Number of Requests by City")
        ax2.set_ylabel("Requests")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=mc_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    tk.Button(tab_mc, text="Load Chart", bg=ACCENT, fg="white",
              relief="flat", command=draw_mc).pack(pady=8)
    draw_mc()

    # TAB 4 - Expand Business (New Property)
    tab_expand = tk.Frame(nb, bg="white")
    nb.add(tab_expand, text="  Expand Business  ")

    tk.Label(tab_expand, text="Add a New City / Property",
             font=("Helvetica", 13, "bold"), bg="white", fg=PRIMARY
             ).pack(pady=(20, 10), padx=25, anchor="w")

    frm = tk.Frame(tab_expand, bg="white", padx=25)
    frm.pack(anchor="nw")

    def lbl(t):
        tk.Label(frm, text=t, bg="white", font=("Helvetica", 10)).pack(anchor="w", pady=(8, 2))
    def ent(w=32):
        e = tk.Entry(frm, width=w, font=("Helvetica", 10))
        e.pack(anchor="w"); return e

    lbl("Property Name *")
    prop_name = ent()
    lbl("Address *")
    prop_addr = ent()
    lbl("City *")
    prop_city = ttk.Combobox(frm, values=["Bristol","Cardiff","London","Manchester"],
                              state="readonly", width=30)
    prop_city.set("Bristol"); prop_city.pack(anchor="w")
    lbl("Postcode *")
    prop_post = ent()
    lbl("Total Units *")
    prop_units = ent()
    lbl("Year Built")
    prop_year = ent()

    result_var2 = tk.StringVar()
    tk.Label(tab_expand, textvariable=result_var2, bg="white",
             fg="#2e7d32", font=("Helvetica", 11, "bold")).pack(pady=5)

    def add_property():
        try:
            units = int(prop_units.get().strip())
            year  = int(prop_year.get().strip()) if prop_year.get().strip() else None
            pid = apt_svc.create_property(
                prop_name.get().strip(), prop_addr.get().strip(),
                prop_city.get(), prop_post.get().strip(), units, year
            )
            result_var2.set(f"Property created with ID {pid}.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(frm, text="Create Property", bg="#2e7d32", fg="white",
              relief="flat", command=add_property).pack(pady=15, anchor="w")

    root.mainloop()
