from datetime import datetime
from backend.database.db import get_connection


class TenantService:
    def register_tenant(self, name, ni_number, phone, email,
                        occupation, reference1, reference2,
                        apartment_type, lease_period_months,
                        user_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tenants
            (user_id, name, ni_number, phone, email,
             occupation, reference1, reference2,
             apartment_type, lease_period_months)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, name, ni_number, phone, email,
              occupation, reference1, reference2,
              apartment_type, lease_period_months))
        conn.commit()
        tenant_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return tenant_id

    def get_all_tenants(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*,
                   l.start_date, l.end_date, l.monthly_rent AS lease_rent,
                   a.unit_number, p.name AS property_name, p.city
            FROM tenants t
            LEFT JOIN leases l ON l.tenant_id = t.id AND l.status = 'active'
            LEFT JOIN apartments a ON a.id = l.apartment_id
            LEFT JOIN properties p ON p.id = a.property_id
            ORDER BY t.registered_date DESC
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_tenant_by_id(self, tenant_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*,
                   l.id AS lease_id, l.start_date, l.end_date,
                   l.monthly_rent AS lease_rent, l.deposit_amount, l.status AS lease_status,
                   a.unit_number, a.apartment_type AS apt_type, a.floor,
                   p.name AS property_name, p.city, p.address
            FROM tenants t
            LEFT JOIN leases l ON l.tenant_id = t.id AND l.status = 'active'
            LEFT JOIN apartments a ON a.id = l.apartment_id
            LEFT JOIN properties p ON p.id = a.property_id
            WHERE t.id = %s
        """, (tenant_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def get_tenant_by_username(self, username: str):
        """Find a tenant record linked to a user account by username."""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*
            FROM tenants t
            JOIN users u ON u.id = t.user_id
            WHERE u.username = %s
        """, (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def update_tenant(self, tenant_id: int, **fields):
        allowed = {"name", "phone", "email", "occupation",
                   "reference1", "reference2", "apartment_type"}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            return
        set_clause = ", ".join(f"{k} = %s" for k in updates)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE tenants SET {set_clause} WHERE id = %s",
            list(updates.values()) + [tenant_id]
        )
        conn.commit()
        cursor.close()
        conn.close()

    def remove_tenant(self, tenant_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tenants WHERE id = %s", (tenant_id,))
        conn.commit()
        cursor.close()
        conn.close()
