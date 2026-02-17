from backend.services.maintenance_service import MaintenanceService

print("Testing MaintenanceService from frontend...")

service = MaintenanceService()
requests = service.get_all_requests()

print(f"Found {len(requests)} maintenance requests:")
for r in requests:
    print(f"  ID: {r['id']}, Apt: {r['apartment_id']}, Desc: {r['description']}, Status: {r['status']}")

print("\nIf you see data above, the service works correctly!")