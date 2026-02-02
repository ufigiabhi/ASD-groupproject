from datetime import datetime, timedelta
from backend.models.invoice import Invoice
from backend.models.payment import Payment

invoice = Invoice(
    "INV001",
    "T001",
    1200,
    datetime.now() + timedelta(days=5)
)

print(invoice.status)  # UNPAID

payment = Payment("PAY001", 1200, "Card")
invoice.add_payment(payment)

print(invoice.status)  # PAID
print(invoice.is_overdue())  # False
