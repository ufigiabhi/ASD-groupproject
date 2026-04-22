#================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Esila Keskin / Sahiru Saunda Hennadige
# Student ID(s):  24064432  / 24048635
# Description: Database connection factory - get_conn() returning MySQL Connector instance
#================================================================

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="314159Pi.com",
        database="asd_project"
    )