#================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    John Davies / Aston George Merry
# Student ID(s):  24024782 / 24063013
# Description: Invoice service - generate monthly invoices due 28th, overdue detection, mark paid
#================================================================

from datetime import date, timedelta
from backend.database.db import get_connection

LATE_FEE_AMOUNT = 50.00   # £50 fixed late fee


class InvoiceService:
    def generate_invoice(self, tenant_id, lease_id, amount, month, year):
        """Create a monthly invoice due on the 28th of that month."""
        issue_date = date(year, month, 1)
        due_date   = date(year, month, 28)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO invoices
            (tenant_id, lease_id, amount, issue_date, due_date, month, year, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'unpaid')
        """, (tenant_id, lease_id, amount, issue_date, due_date, month, year))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id

    def get_invoice_by_id(self, invoice_id: int):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT i.*, t.name AS tenant_name
            FROM invoices i
            JOIN tenants t ON i.tenant_id = t.id
            WHERE i.id = %s
        """, (invoice_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def get_invoices_for_tenant(self, tenant_id: int):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM invoices
            WHERE tenant_id = %s
            ORDER BY year DESC, month DESC
        """, (tenant_id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_invoices_by_month_year(self, month: int, year: int):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT i.*, t.name AS tenant_name
            FROM invoices i
            JOIN tenants t ON i.tenant_id = t.id
            WHERE i.month = %s AND i.year = %s
            ORDER BY i.status, t.name
        """, (month, year))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_all_invoices(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT i.*, t.name AS tenant_name
            FROM invoices i
            JOIN tenants t ON i.tenant_id = t.id
            ORDER BY i.year DESC, i.month DESC, t.name
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_overdue_invoices(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        today = date.today()
        cur.execute("""
            SELECT i.*, t.name AS tenant_name, t.email, t.phone
            FROM invoices i
            JOIN tenants t ON i.tenant_id = t.id
            WHERE i.status IN ('unpaid','partial')
              AND i.due_date < %s
            ORDER BY i.due_date
        """, (today,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        # Mark as overdue in DB
        if results:
            ids = [r["id"] for r in results]
            conn2 = get_connection()
            c2 = conn2.cursor()
            fmt = ",".join(["%s"] * len(ids))
            c2.execute(f"UPDATE invoices SET status='overdue' WHERE id IN ({fmt})", ids)
            conn2.commit()
            c2.close()
            conn2.close()
        return results

    def mark_paid(self, invoice_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE invoices SET status = 'paid' WHERE id = %s",
            (invoice_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
