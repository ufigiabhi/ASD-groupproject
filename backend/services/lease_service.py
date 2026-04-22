# ================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Aston George Merry
# Student ID(s): 24063013
# Description: Lease service - create lease, early termination with 5% penalty, expiry alerts
# ================================================================
from datetime import date, timedelta
from backend.database.db import get_connection


EARLY_TERMINATION_PENALTY_PCT = 0.05   # 5% of monthly rent


class LeaseService:
    def create_lease(self, tenant_id, apartment_id, start_date,
                     end_date, monthly_rent, deposit_amount):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO leases
            (tenant_id, apartment_id, start_date, end_date,
             monthly_rent, deposit_amount, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'active')
        """, (tenant_id, apartment_id, start_date, end_date,
              monthly_rent, deposit_amount))
        conn.commit()
        new_id = cur.lastrowid

        # Mark apartment as occupied
        cur.execute(
            "UPDATE apartments SET status = 'occupied' WHERE id = %s",
            (apartment_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return new_id

    def get_active_lease_for_tenant(self, tenant_id: int):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT l.*, a.unit_number, a.apartment_type, a.monthly_rent AS apt_rent,
                   p.name AS property_name, p.city, p.address
            FROM leases l
            JOIN apartments a ON l.apartment_id = a.id
            JOIN properties p ON a.property_id = p.id
            WHERE l.tenant_id = %s AND l.status = 'active'
            ORDER BY l.start_date DESC
            LIMIT 1
        """, (tenant_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def get_all_leases(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT l.*, t.name AS tenant_name, a.unit_number,
                   p.name AS property_name, p.city
            FROM leases l
            JOIN tenants t ON l.tenant_id = t.id
            JOIN apartments a ON l.apartment_id = a.id
            JOIN properties p ON a.property_id = p.id
            ORDER BY l.end_date ASC
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_expiring_soon(self, days: int = 30):
        """Return leases expiring within the next `days` days."""
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        today = date.today()
        threshold = today + timedelta(days=days)
        cur.execute("""
            SELECT l.*, t.name AS tenant_name, t.phone, t.email,
                   a.unit_number, p.name AS property_name, p.city
            FROM leases l
            JOIN tenants t ON l.tenant_id = t.id
            JOIN apartments a ON l.apartment_id = a.id
            JOIN properties p ON a.property_id = p.id
            WHERE l.status = 'active'
              AND l.end_date BETWEEN %s AND %s
            ORDER BY l.end_date
        """, (today, threshold))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def request_early_termination(self, lease_id: int):
        """
        Tenant gives 1 month notice. Penalty = 5% of monthly rent.
        Sets notice_given_date = today, calculates early_termination_fee.
        """
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM leases WHERE id = %s", (lease_id,))
        lease = cur.fetchone()
        cur.close()

        if not lease:
            conn.close()
            raise ValueError(f"Lease {lease_id} not found.")

        today = date.today()
        penalty = float(lease["monthly_rent"]) * EARLY_TERMINATION_PENALTY_PCT

        cur = conn.cursor()
        cur.execute("""
            UPDATE leases
            SET notice_given_date = %s,
                early_termination_fee = %s
            WHERE id = %s
        """, (today, penalty, lease_id))
        conn.commit()
        cur.close()
        conn.close()
        return penalty

    def terminate_lease(self, lease_id: int):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT apartment_id FROM leases WHERE id = %s", (lease_id,))
        row = cur.fetchone()
        cur.close()

        cur = conn.cursor()
        cur.execute(
            "UPDATE leases SET status = 'terminated' WHERE id = %s",
            (lease_id,)
        )
        if row:
            cur.execute(
                "UPDATE apartments SET status = 'available' WHERE id = %s",
                (row["apartment_id"],)
            )
        conn.commit()
        cur.close()
        conn.close()
