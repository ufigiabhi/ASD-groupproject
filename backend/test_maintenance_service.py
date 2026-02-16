from backend.services.maintenance_service import MaintenanceService

service = MaintenanceService()

request_id = service.create_request(101, "Leaking sink")
print("CREATED:", service.get_request(request_id)["status"])

service.assign_staff(request_id, "Maintenance John")
print("ASSIGNED:", service.get_request(request_id)["status"])

service.resolve_request(request_id, 2.5, 250)
resolved = service.get_request(request_id)
print("RESOLVED:", resolved["status"], resolved["cost"])