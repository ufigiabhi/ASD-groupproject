from datetime import datetime
from backend.models.payment import Payment


class Invoice:
    def __init__(
        self,
        invoice_id: str,
        tenant_id: str,
        amount: float,
        due_date: datetime
    ):
        self.invoice_id = invoice_id
        self.tenant_id = tenant_id
        self.amount = amount
        self.due_date = due_date
        self.status = "UNPAID"
        self.payments: list[Payment] = []

    def add_payment(self, payment: Payment):
        if payment.is_valid():
            self.payments.append(payment)
            self.status = "PAID"

    def is_overdue(self) -> bool:
        return datetime.now() > self.due_date and self.status != "PAID"
