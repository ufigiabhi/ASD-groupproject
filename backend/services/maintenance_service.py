from datetime import datetime
from backend.database.db import get_connection

    # =====================================
    # DEFINING MAINTENANCE SERVICE CLASS
    # =====================================

class MaintenanceService:
    def create_request(self, apartment_id, description, priority="Medium",
                       tenant_id=None):

        """
        Creates a new maintenance request and inserts it into the database.
        
        Args:
            apartment_id: The ID of the apartment requiring maintenance.
            description: A description of the maintenance issue.
            priority: The priority level of the request (default is "Medium").
            tenant_id: The ID of the tenant submitting the request (optional).
            
        Returns:
            request_id: The ID of the newly created maintenance request.
        """

        # Establish a connection to the database
        conn = get_connection()
        cursor = conn.cursor()
        
        # Insert the new maintenance request into the database
        # Status is set to "OPEN" by default and submission date is set to now
        cursor.execute(
            """
            INSERT INTO maintenance_requests
            (apartment_id, tenant_id, description, priority, status, submission_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (apartment_id, tenant_id, description, priority, "OPEN", datetime.now())
        )

        # Commit the transaction to save the changes
        conn.commit()

        # Retrieve the ID of the newly inserted request
        request_id = cursor.lastrowid

        # Close the cursor and connection to free up resources
        cursor.close()
        conn.close()

        # Return the ID of the new request
        return request_id

    def assign_staff(self, request_id, staff_name):
        """
        Assigns a staff member to a maintenance request and updates
        the request status to "IN_PROGRESS".
        
        Args:
            request_id: The ID of the maintenance request to update.
            staff_name: The name of the staff member being assigned.
        """

        # Establish a connection to the database
        conn = get_connection()
        cursor = conn.cursor()

        # Update the maintenance request with the assigned staff member
        # and change the status to "IN_PROGRESS"
        cursor.execute(
            """
            UPDATE maintenance_requests
            SET status = %s,
                assigned_staff = %s
            WHERE id = %s
            """,
            ("IN_PROGRESS", staff_name, request_id)
        )

        # Commit the transaction to save the changes
        conn.commit()

        # Close the cursor and connection to free up resources
        cursor.close()
        conn.close()

    def resolve_request(self, request_id, time_taken, cost):
        """
        Marks a maintenance request as resolved and records the time taken,
        cost, and resolution date.
        
        Args:
            request_id: The ID of the maintenance request to resolve.
            time_taken: The amount of time taken to resolve the request.
            cost: The cost incurred to resolve the request.
        """

        # Establish a connection to the database
        conn = get_connection()
        cursor = conn.cursor()

        # Update the maintenance request with resolution details
        # Status is set to "RESOLVED" and resolution date is set to now
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
        """
        Retrieves a single maintenance request by its ID.
        
        Args:
            request_id: The ID of the maintenance request to retrieve.
            
        Returns:
            result: A dictionary containing the maintenance request details,
                    or None if no request was found.
        """
        
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

    def get_requests_for_tenant(self, tenant_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM maintenance_requests
            WHERE tenant_id = %s
            ORDER BY submission_date DESC
            """,
            (tenant_id,)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_open_requests(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT mr.*, a.unit_number, p.name AS property_name, p.city,
                   t.name AS tenant_name
            FROM maintenance_requests mr
            JOIN apartments a ON mr.apartment_id = a.id
            JOIN properties p ON a.property_id = p.id
            LEFT JOIN tenants t ON mr.tenant_id = t.id
            WHERE mr.status IN ('OPEN','IN_PROGRESS')
            ORDER BY
                CASE mr.priority
                    WHEN 'Emergency' THEN 1
                    WHEN 'High'      THEN 2
                    WHEN 'Medium'    THEN 3
                    WHEN 'Low'       THEN 4
                END,
                mr.submission_date
            """
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results