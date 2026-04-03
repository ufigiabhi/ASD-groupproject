import uuid
from datetime import datetime
from backend.database.db import get_connection


class PaymentService:
    def _generate_receipt(self) -> str:
        return "RCP-" + uuid.uuid4().hex[:8].upper()

    def record_payment(self, invoice_id: int, tenant_id: int,
                       amount: float, method: str, late_fee: float = 0.0):
        """
        Records a payment and marks the invoice as paid.
        Returns (payment_id, receipt_number).
        """
        receipt = self._generate_receipt()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO payments
            (invoice_id, tenant_id, amount, payment_date,
             method, status, late_fee, receipt_number)
            VALUES (%s, %s, %s, %s, %s, 'completed', %s, %s)
        """, (invoice_id, tenant_id, amount,
              datetime.now(), method, late_fee, receipt))
        conn.commit()
        payment_id = cur.lastrowid

        # Mark invoice as paid
        cur.execute(
            "UPDATE invoices SET status = 'paid' WHERE id = %s",
            (invoice_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return payment_id, receipt

    def get_payments_for_tenant(self, tenant_id: int):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.*, i.month, i.year, i.amount AS invoice_amount
            FROM payments p
            JOIN invoices i ON p.invoice_id = i.id
            WHERE p.tenant_id = %s
            ORDER BY p.payment_date DESC
        """, (tenant_id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_payments_by_month_year(self, month: int, year: int):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.*, t.name AS tenant_name, i.month, i.year
            FROM payments p
            JOIN invoices i ON p.invoice_id = i.id
            JOIN tenants t ON p.tenant_id = t.id
            WHERE i.month = %s AND i.year = %s
            ORDER BY p.payment_date DESC
        """, (month, year))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_all_payments(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.*, t.name AS tenant_name, i.month, i.year
            FROM payments p
            JOIN invoices i ON p.invoice_id = i.id
            JOIN tenants t ON p.tenant_id = t.id
            ORDER BY p.payment_date DESC
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_financial_summary(self, month: int = None, year: int = None):
        """Returns totals: collected, pending, overdue."""
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        where = ""
        params = []
        if month and year:
            where = "WHERE i.month = %s AND i.year = %s"
            params = [month, year]

        cur.execute(f"""
            SELECT
                SUM(CASE WHEN i.status = 'paid'    THEN i.amount ELSE 0 END) AS collected,
                SUM(CASE WHEN i.status = 'unpaid'  THEN i.amount ELSE 0 END) AS pending,
                SUM(CASE WHEN i.status = 'overdue' THEN i.amount ELSE 0 END) AS overdue,
                COUNT(*) AS total_invoices
            FROM invoices i
            {where}
        """, params)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result
