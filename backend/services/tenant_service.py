from datetime import datetime
from backend.database.db import get_connection


class TenantService:
    def register_tenant(self, name, ni_number, phone, email,
                        occupation, reference1, reference2,
                        apartment_type, lease_period_months,
                        user_id=None):
        # Open a database connection to insert a new tenant record
        conn = get_connection()
        cursor = conn.cursor()

        # Insert the tenant's details into the tenants table
        cursor.execute("""
            INSERT INTO tenants
            (user_id, name, ni_number, phone, email,
             occupation, reference1, reference2,
             apartment_type, lease_period_months)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, name, ni_number, phone, email,
              occupation, reference1, reference2,
              apartment_type, lease_period_months))

        # Save the new row and return its generated tenant ID
        conn.commit()
        tenant_id = cursor.lastrowid

        # Clean up database resources
        cursor.close()
        conn.close()
        return tenant_id

    def get_all_tenants(self):
        # Retrieve all tenants along with any active lease and property details
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

        # Fetch all matching rows as dictionaries
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_tenant_by_id(self, tenant_id: int):
        # Retrieve one tenant by ID, including linked lease, apartment and property info
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

        # Return a single matching tenant record
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def get_tenant_by_username(self, username: str):
        """Find a tenant record linked to a user account by username."""
        # Join tenants with users so a tenant can be found using their login username
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
        # Only allow specific tenant fields to be updated
        allowed = {"name", "phone", "email", "occupation",
                   "reference1", "reference2", "apartment_type"}

        # Filter out any fields that are not in the allowed set
        updates = {k: v for k, v in fields.items() if k in allowed}

        # Exit early if no valid fields were provided
        if not updates:
            return

        # Build the SQL SET clause dynamically from the provided fields
        set_clause = ", ".join(f"{k} = %s" for k in updates)

        conn = get_connection()
        cursor = conn.cursor()

        # Update the tenant record using the filtered field values
        cursor.execute(
            f"UPDATE tenants SET {set_clause} WHERE id = %s",
            list(updates.values()) + [tenant_id]
        )

        conn.commit()
        cursor.close()
        conn.close()

    def remove_tenant(self, tenant_id: int):
        # Delete a tenant record by its ID
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tenants WHERE id = %s", (tenant_id,))
        conn.commit()

        cursor.close()
        conn.close()