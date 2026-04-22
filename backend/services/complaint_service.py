#================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Esila Keskin 
# Student ID(s):  24064432  
# Description: Complaint service - create, list by tenant, update status and resolution notes
#================================================================
from datetime import datetime
from backend.database.db import get_connection


class ComplaintService:
    def create_complaint(self, tenant_name: str, issue: str,
                         category: str = "Other", tenant_id: int = None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO complaints (tenant_id, tenant_name, issue, category, status)
            VALUES (%s, %s, %s, %s, 'Open')
        """, (tenant_id, tenant_name, issue, category))
        conn.commit()
        complaint_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return complaint_id

    def get_all_complaints(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM complaints
            ORDER BY submission_date DESC
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_complaints_for_tenant(self, tenant_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM complaints
            WHERE tenant_id = %s
            ORDER BY submission_date DESC
        """, (tenant_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def update_status(self, complaint_id: int, status: str,
                      resolution_notes: str = None):
        conn = get_connection()
        cursor = conn.cursor()
        if status == "Resolved":
            cursor.execute("""
                UPDATE complaints
                SET status = %s,
                    resolution_notes = %s,
                    resolution_date = %s
                WHERE id = %s
            """, (status, resolution_notes, datetime.now(), complaint_id))
        else:
            cursor.execute(
                "UPDATE complaints SET status = %s WHERE id = %s",
                (status, complaint_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
