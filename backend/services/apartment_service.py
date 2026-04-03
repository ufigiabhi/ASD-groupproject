from backend.database.db import get_connection


class ApartmentService:
    def get_all_apartments(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.*, p.name AS property_name, p.city
            FROM apartments a
            JOIN properties p ON a.property_id = p.id
            ORDER BY p.city, a.unit_number
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_apartments_by_city(self, city: str):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.*, p.name AS property_name, p.city
            FROM apartments a
            JOIN properties p ON a.property_id = p.id
            WHERE p.city = %s
            ORDER BY a.unit_number
        """, (city,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_available_apartments(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.*, p.name AS property_name, p.city
            FROM apartments a
            JOIN properties p ON a.property_id = p.id
            WHERE a.status = 'available'
            ORDER BY p.city, a.monthly_rent
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_apartment_by_id(self, apartment_id: int):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.*, p.name AS property_name, p.city
            FROM apartments a
            JOIN properties p ON a.property_id = p.id
            WHERE a.id = %s
        """, (apartment_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def create_apartment(self, property_id, unit_number, floor, bedrooms,
                         bathrooms, size_sqm, monthly_rent, apartment_type):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO apartments
            (property_id, unit_number, floor, bedrooms, bathrooms,
             size_sqm, monthly_rent, apartment_type, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'available')
        """, (property_id, unit_number, floor, bedrooms, bathrooms,
              size_sqm, monthly_rent, apartment_type))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id

    def set_status(self, apartment_id: int, status: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE apartments SET status = %s WHERE id = %s",
            (status, apartment_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    def get_occupancy_summary(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.city,
                   COUNT(a.id)                                          AS total,
                   SUM(a.status = 'occupied')                           AS occupied,
                   SUM(a.status = 'available')                          AS available,
                   SUM(a.status = 'maintenance')                        AS maintenance,
                   ROUND(SUM(a.status='occupied')/COUNT(a.id)*100, 1)   AS occupancy_pct
            FROM apartments a
            JOIN properties p ON a.property_id = p.id
            GROUP BY p.city
            ORDER BY p.city
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_all_properties(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM properties ORDER BY city")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def create_property(self, name, address, city, postcode, total_units, year_built=None):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO properties (name, address, city, postcode, total_units, year_built)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, address, city, postcode, total_units, year_built))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id
