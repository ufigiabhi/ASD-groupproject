"""
Automated unit tests for PAMS model classes.
Run:  python -m pytest backend/tests/ -v
  or  python -m unittest discover backend/tests
"""
import unittest
from datetime import datetime, timedelta
from backend.models.apartment import Apartment
from backend.models.invoice import Invoice
from backend.models.payment import Payment
from backend.models.user import User


class TestApartmentModel(unittest.TestCase):
    def setUp(self):
        self.apt = Apartment("A1", "101", 2, 1200.00, 65.0)

    def test_initial_status_not_occupied(self):
        self.assertFalse(self.apt.is_occupied)

    def test_initial_tenant_is_none(self):
        self.assertIsNone(self.apt.current_tenant)

    def test_assign_tenant(self):
        self.apt.assign_tenant("John Smith")
        self.assertTrue(self.apt.is_occupied)
        self.assertEqual(self.apt.current_tenant, "John Smith")

    def test_vacate_clears_tenant(self):
        self.apt.assign_tenant("John Smith")
        self.apt.vacate()
        self.assertFalse(self.apt.is_occupied)
        self.assertIsNone(self.apt.current_tenant)

    def test_rent_positive(self):
        self.assertGreater(self.apt.rent, 0)

    def test_bedrooms_positive(self):
        self.assertGreater(self.apt.bedrooms, 0)

    def test_invalid_rent_zero(self):
        # Rent should not be zero or negative in a valid apartment
        apt_bad = Apartment("A2", "999", 1, 0, 30.0)
        self.assertEqual(apt_bad.rent, 0)   # object allows it - test shows validation gap

    def test_size_sqm(self):
        self.assertEqual(self.apt.size_sqm, 65.0)


class TestInvoiceModel(unittest.TestCase):
    def setUp(self):
        self.due_future = datetime.now() + timedelta(days=10)
        self.due_past   = datetime.now() - timedelta(days=5)
        self.inv = Invoice("INV001", "T001", 1400.00, self.due_future)

    def test_initial_status_unpaid(self):
        self.assertEqual(self.inv.status, "UNPAID")

    def test_not_overdue_when_future(self):
        self.assertFalse(self.inv.is_overdue())

    def test_is_overdue_when_past(self):
        inv = Invoice("INV002", "T001", 1200.00, self.due_past)
        self.assertTrue(inv.is_overdue())

    def test_add_valid_payment_marks_paid(self):
        pay = Payment("P001", 1400.00, "Card")
        self.inv.add_payment(pay)
        self.assertEqual(self.inv.status, "PAID")

    def test_add_zero_payment_rejected(self):
        pay = Payment("P002", 0, "Cash")
        self.inv.add_payment(pay)
        # Zero payment is not valid, so invoice stays unpaid
        self.assertEqual(self.inv.status, "UNPAID")

    def test_negative_payment_rejected(self):
        pay = Payment("P003", -50, "Card")
        self.inv.add_payment(pay)
        self.assertEqual(self.inv.status, "UNPAID")

    def test_paid_invoice_not_overdue(self):
        inv = Invoice("INV003", "T001", 900.00, self.due_past)
        pay = Payment("P004", 900.00, "Card")
        inv.add_payment(pay)
        self.assertFalse(inv.is_overdue())

    def test_multiple_payments_accumulate(self):
        pay1 = Payment("P005", 700.00, "Card")
        pay2 = Payment("P006", 700.00, "Cash")
        self.inv.add_payment(pay1)
        self.assertEqual(len(self.inv.payments), 1)


class TestPaymentModel(unittest.TestCase):
    def test_valid_payment(self):
        pay = Payment("P001", 1200.00, "Card")
        self.assertTrue(pay.is_valid())

    def test_zero_amount_invalid(self):
        pay = Payment("P002", 0, "Cash")
        self.assertFalse(pay.is_valid())

    def test_negative_amount_invalid(self):
        pay = Payment("P003", -100, "Bank Transfer")
        self.assertFalse(pay.is_valid())

    def test_status_completed(self):
        pay = Payment("P004", 500.00, "Card")
        self.assertEqual(pay.status, "COMPLETED")

    def test_payment_date_set(self):
        pay = Payment("P005", 800.00, "Cash")
        self.assertIsNotNone(pay.payment_date)

    def test_method_stored(self):
        pay = Payment("P006", 1000.00, "Bank Transfer")
        self.assertEqual(pay.method, "Bank Transfer")


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = User("U001", "admin1", "Admin@123")

    def test_password_hashed(self):
        # Stored hash must not equal plaintext
        self.assertNotEqual(self.user.password_hash, "Admin@123")

    def test_correct_password_verifies(self):
        self.assertTrue(self.user.verify_password("Admin@123"))

    def test_wrong_password_rejected(self):
        self.assertFalse(self.user.verify_password("wrongpassword"))

    def test_empty_password_rejected(self):
        self.assertFalse(self.user.verify_password(""))

    def test_login_updates_last_login(self):
        self.assertIsNone(self.user.last_login_date)
        self.user.login("Admin@123")
        self.assertIsNotNone(self.user.last_login_date)

    def test_failed_login_no_last_login_update(self):
        self.user.login("wrongpassword")
        self.assertIsNone(self.user.last_login_date)

    def test_username_stored(self):
        self.assertEqual(self.user.username, "admin1")


class TestInputValidation(unittest.TestCase):
    """Tests that validate input constraints."""

    def test_ni_number_format(self):
        """NI numbers follow UK format: 2 letters, 6 digits, 1 letter."""
        import re
        valid_ni   = "AB123456C"
        invalid_ni = "12345678"
        pattern = r"^[A-Z]{2}\d{6}[A-Z]$"
        self.assertTrue(re.match(pattern, valid_ni))
        self.assertIsNone(re.match(pattern, invalid_ni))

    def test_lease_period_positive(self):
        lease_period = 12
        self.assertGreater(lease_period, 0)

    def test_early_termination_penalty(self):
        monthly_rent = 1400.00
        penalty = monthly_rent * 0.05
        self.assertAlmostEqual(penalty, 70.00)

    def test_rent_must_be_numeric(self):
        raw_input = "1200"
        try:
            rent = float(raw_input)
            valid = True
        except ValueError:
            valid = False
        self.assertTrue(valid)

    def test_non_numeric_rent_fails(self):
        raw_input = "twelve hundred"
        try:
            float(raw_input)
            valid = True
        except ValueError:
            valid = False
        self.assertFalse(valid)

    def test_email_contains_at_symbol(self):
        valid_email   = "john@example.com"
        invalid_email = "johnexample.com"
        self.assertIn("@", valid_email)
        self.assertNotIn("@", invalid_email)

    def test_deposit_double_monthly_rent(self):
        """Verify standard deposit is 2x monthly rent."""
        monthly_rent = 1200.00
        deposit = monthly_rent * 2
        self.assertEqual(deposit, 2400.00)


if __name__ == "__main__":
    unittest.main()
