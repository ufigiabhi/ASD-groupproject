from datetime import datetime
from backend.database.db import get_connection


class TenantService:
    def register_tenant(self, name, ni_number, phone, email, apartment_type, lease_period):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tenants
            (name, ni_number, phone, email, apartment_type, lease_period)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (name, ni_number, phone, email, apartment_type, lease_period)
        )

        conn.commit()
        tenant_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return tenant_id

    def get_all_tenants(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT * FROM tenants
            ORDER BY registered_date DESC
            """
        )

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results