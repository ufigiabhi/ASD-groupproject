from datetime import datetime
from backend.database.db import get_connection


class ComplaintService:
    def create_complaint(self, tenant_name, issue):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO complaints
            (tenant_name, issue, status)
            VALUES (%s, %s, %s)
            """,
            (tenant_name, issue, "Investigating")
        )

        conn.commit()
        complaint_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return complaint_id

    def get_all_complaints(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT * FROM complaints
            ORDER BY submission_date DESC
            """
        )

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results