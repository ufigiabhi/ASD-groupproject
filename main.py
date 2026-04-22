#================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Esila Keskin 
# Student ID(s):  24064432  
# Description: PAMS entry point - imports and launces login GU
#================================================================

"""
PAMS - Paragon Apartment Management System
Entry point.

Run: python main.py
Setup DB first: python -m backend.database.setup_db
"""

from frontend.login import run_login

if __name__ == "__main__":
    run_login()
