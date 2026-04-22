# ================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Esila Keskin
# Student ID(s):  24064432
# Description: MaintenanceRequest model -update_status(), assign_staff(), record_resolution()
# ================================================================
from datetime import datetime
import uuid


class MaintenanceRequest:
    def __init__(self, apartment_id, description, priority="Medium"):
        self.id = str(uuid.uuid4())
        self.apartment_id = apartment_id
        self.description = description
        self.priority = priority

        self.status = "OPEN"
        self.submission_date = datetime.now()
        self.resolution_date = None

        self.time_taken = 0.0
        self.associated_cost = 0.0
        self.assigned_staff = None

    def update_status(self, new_status):
        self.status = new_status

    def assign_staff(self, staff_name):
        self.assigned_staff = staff_name
        self.status = "IN_PROGRESS"

    def record_resolution(self, time_taken, cost):
        self.time_taken = time_taken
        self.associated_cost = cost
        self.resolution_date = datetime.now()
        self.status = "RESOLVED"
