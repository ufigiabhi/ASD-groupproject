from datetime import datetime
from backend.database.db import get_connection


class MaintenanceService:
    def create_request(self, apartment_id, description, priority="Medium"):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO maintenance_requests
            (apartment_id, description, priority, status, submission_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (apartment_id, description, priority, "OPEN", datetime.now())
        )

        conn.commit()
        request_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return request_id

    def assign_staff(self, request_id, staff_name):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE maintenance_requests
            SET status = %s,
                assigned_staff = %s
            WHERE id = %s
            """,
            ("IN_PROGRESS", staff_name, request_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

    def resolve_request(self, request_id, time_taken, cost):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE maintenance_requests
            SET status = %s,
                time_taken = %s,
                cost = %s,
                resolution_date = %s
            WHERE id = %s
            """,
            ("RESOLVED", time_taken, cost, datetime.now(), request_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

    def get_request(self, request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM maintenance_requests WHERE id = %s",
            (request_id,)
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    # ============================
    # Phase C – NEW FUNCTIONALITY
    # ============================

    def get_all_requests(self):
        """
        Fetch all maintenance requests from the database.
        Used for dashboards and admin views.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM maintenance_requests
            ORDER BY submission_date DESC
            """
        )

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results