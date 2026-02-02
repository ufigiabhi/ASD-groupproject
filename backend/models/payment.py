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
