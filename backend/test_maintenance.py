from backend.models.maintenance_request import MaintenanceRequest

req = MaintenanceRequest(
    request_id="MR001",
    description="Leaking sink",
    priority="High"
)

print(req.status)
print(req.priority)

req.record_resolution(time_taken=2.5, cost=120.0)

print(req.status)
print(req.associated_cost)
