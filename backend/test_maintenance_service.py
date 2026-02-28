from backend.services.maintenance_service import MaintenanceService

service = MaintenanceService()

print("\n=== CREATE REQUEST ===")
request_id = service.create_request(
    apartment_id=101,
    description="Leaking sink",
    priority="Medium"
)
request = service.get_request(request_id)
print("CREATED:", request["status"], "| ID:", request_id)

print("\n=== ASSIGN STAFF ===")
service.assign_staff(request_id, "Maintenance John")
request = service.get_request(request_id)
print("ASSIGNED:", request["status"], "| Staff:", request["assigned_staff"])

print("\n=== RESOLVE REQUEST ===")
service.resolve_request(request_id, 2.5, 250)
request = service.get_request(request_id)
print(
    "RESOLVED:",
    request["status"],
    "| Time:", request["time_taken"],
    "| Cost:", request["cost"]
)

print("\n=== FETCH ALL REQUESTS (PHASE C) ===")
all_requests = service.get_all_requests()

for r in all_requests:
    print(
        f"ID {r['id']} | "
        f"Apt {r['apartment_id']} | "
        f"{r['description']} | "
        f"{r['status']} | "
        f"£{r.get('cost')}"
    )