from backend.models.property import Property
from backend.models.apartment import Apartment

property = Property("P001", "City Heights", "123 Main St")

a1 = Apartment("A1", "101", 2, 1200, 80)
a2 = Apartment("A2", "102", 1, 900, 55)

property.add_apartment(a1)
property.add_apartment(a2)

a1.is_occupied = True

print(property.get_occupancy_rate())  # 0.5
