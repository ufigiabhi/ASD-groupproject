# ================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Esila Keskin / Abhinav Singh Rawat
# Student ID(s):  24064432 / 24027772
# Description: Property model class - represents a building containing apartments
# ================================================================
from backend.models.apartment import Apartment


class Property:
    def __init__(
        self,
        property_id: str,
        name: str,
        address: str
    ):
        self.property_id = property_id
        self.name = name
        self.address = address
        self.apartments: list[Apartment] = []

    def add_apartment(self, apartment: Apartment):
        self.apartments.append(apartment)

    def get_occupancy_rate(self) -> float:
        if not self.apartments:
            return 0.0
        occupied = sum(1 for a in self.apartments if a.is_occupied)
        return occupied / len(self.apartments)
