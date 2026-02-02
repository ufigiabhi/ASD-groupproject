class Apartment:
    def __init__(
        self,
        apartment_id: str,
        unit_number: str,
        bedrooms: int,
        rent: float,
        size_sqm: float
    ):
        self.apartment_id = apartment_id
        self.unit_number = unit_number
        self.bedrooms = bedrooms
        self.rent = rent
        self.size_sqm = size_sqm
        self.is_occupied = False
        self.current_tenant = None

    def assign_tenant(self, tenant):
        self.current_tenant = tenant
        self.is_occupied = True

    def vacate(self):
        self.current_tenant = None
        self.is_occupied = False
