#================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Esila Keskin 
# Student ID(s):  24064432  
# Description: Report service - occupancy by city, financial summary, maintenance costs, lease expiry
#================================================================

from backend.database.db import get_connection


class ReportService:
    def occupancy_report(self, city: str = None):
        """Occupancy by city (or overall)."""
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        if city:
            cur.execute("""
                SELECT p.name AS property_name, p.city, p.address,
                       COUNT(a.id)                                        AS total_units,
                       SUM(a.status = 'occupied')                        AS occupied,
                       SUM(a.status = 'available')                       AS available,
                       SUM(a.status = 'maintenance')                     AS under_maintenance,
                       ROUND(SUM(a.status='occupied')/COUNT(a.id)*100,1) AS occupancy_pct
                FROM properties p
                JOIN apartments a ON a.property_id = p.id
                WHERE p.city = %s
                GROUP BY p.id
                ORDER BY p.name
            """, (city,))
        else:
            cur.execute("""
                SELECT p.city,
                       COUNT(a.id)                                        AS total_units,
                       SUM(a.status = 'occupied')                        AS occupied,
                       SUM(a.status = 'available')                       AS available,
                       SUM(a.status = 'maintenance')                     AS under_maintenance,
                       ROUND(SUM(a.status='occupied')/COUNT(a.id)*100,1) AS occupancy_pct
                FROM properties p
                JOIN apartments a ON a.property_id = p.id
                GROUP BY p.city
                ORDER BY p.city
            """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def financial_summary(self, month: int = None, year: int = None):
        """Collected vs pending vs overdue rents."""
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        params = []
        where = ""
        if month and year:
            where = "WHERE i.month = %s AND i.year = %s"
            params = [month, year]

        cur.execute(f"""
            SELECT
                SUM(CASE WHEN i.status = 'paid'    THEN i.amount ELSE 0 END) AS collected,
                SUM(CASE WHEN i.status = 'unpaid'  THEN i.amount ELSE 0 END) AS pending,
                SUM(CASE WHEN i.status = 'overdue' THEN i.amount ELSE 0 END) AS overdue,
                COUNT(*) AS total_invoices,
                SUM(i.amount) AS total_billed
            FROM invoices i
            {where}
        """, params)
        summary = cur.fetchone()

        cur.execute(f"""
            SELECT SUM(p.late_fee) AS total_late_fees
            FROM payments p
            JOIN invoices i ON p.invoice_id = i.id
            {where}
        """, params)
        late = cur.fetchone()
        cur.close()
        conn.close()

        if summary:
            summary["total_late_fees"] = late["total_late_fees"] or 0
        return summary

    def maintenance_cost_report(self, city: str = None):
        """Maintenance costs per city/property."""
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        if city:
            cur.execute("""
                SELECT p.name AS property_name, p.city,
                       COUNT(mr.id)          AS total_requests,
                       SUM(mr.status='OPEN') AS open_requests,
                       SUM(mr.cost)          AS total_cost,
                       AVG(mr.time_taken)    AS avg_hours
                FROM maintenance_requests mr
                JOIN apartments a ON mr.apartment_id = a.id
                JOIN properties p ON a.property_id = p.id
                WHERE p.city = %s
                GROUP BY p.id
            """, (city,))
        else:
            cur.execute("""
                SELECT p.city,
                       COUNT(mr.id)          AS total_requests,
                       SUM(mr.status='OPEN' OR mr.status='IN_PROGRESS') AS open_requests,
                       IFNULL(SUM(mr.cost), 0)       AS total_cost,
                       IFNULL(AVG(mr.time_taken), 0) AS avg_hours
                FROM maintenance_requests mr
                JOIN apartments a ON mr.apartment_id = a.id
                JOIN properties p ON a.property_id = p.id
                GROUP BY p.city
                ORDER BY p.city
            """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def tenant_payment_history(self, tenant_id: int):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT i.month, i.year, i.amount, i.status AS invoice_status,
                   p.payment_date, p.method, p.late_fee, p.receipt_number
            FROM invoices i
            LEFT JOIN payments p ON p.invoice_id = i.id
            WHERE i.tenant_id = %s
            ORDER BY i.year DESC, i.month DESC
        """, (tenant_id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def lease_end_report(self, days_ahead: int = 60):
        """Leases ending in the next `days_ahead` days."""
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT l.end_date, l.monthly_rent, l.status,
                   t.name AS tenant_name, t.email, t.phone,
                   a.unit_number, p.name AS property_name, p.city
            FROM leases l
            JOIN tenants t ON l.tenant_id = t.id
            JOIN apartments a ON l.apartment_id = a.id
            JOIN properties p ON a.property_id = p.id
            WHERE l.status = 'active'
              AND l.end_date <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
            ORDER BY l.end_date
        """, (days_ahead,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
