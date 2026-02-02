from datetime import datetime


class MaintenanceRequest:
    def __init__(self, request_id, description, priority="Medium"):
        self.request_id = request_id
        self.description = description
        self.submission_date = datetime.now()
        self.priority = priority
        self.status = "OPEN"
        self.resolution_date = None
        self.time_taken = 0.0
        self.associated_cost = 0.0

    def update_status(self, new_status):
        self.status = new_status

    def prioritize(self, level):
        self.priority = level

    def record_resolution(self, time_taken, cost):
        self.time_taken = time_taken
        self.associated_cost = cost
        self.resolution_date = datetime.now()
        self.status = "RESOLVED"
