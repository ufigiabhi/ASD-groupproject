# ================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Esila Keskin
# Student ID(s):  24064432
# Description: Payment domain model - is_valid() checks for positive amount
# ================================================================
from datetime import datetime


class Payment:
    def __init__(
        self,
        payment_id: str,
        amount: float,
        method: str
    ):
        self.payment_id = payment_id
        self.amount = amount
        self.method = method
        self.payment_date = datetime.now()
        self.status = "COMPLETED"

    def is_valid(self) -> bool:
        return self.amount > 0
