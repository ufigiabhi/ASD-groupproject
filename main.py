"""
PAMS - Paragon Apartment Management System
Entry point.

Run: python main.py
Setup DB first: python -m backend.database.setup_db
"""

from frontend.login import run_login

if __name__ == "__main__":
    run_login()
