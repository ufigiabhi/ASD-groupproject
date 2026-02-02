import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",   # we'll change this later
                database="pams_db"     # this as well
            )

            if self.connection.is_connected():
                print("Database connection successful")

        except Error as e:
            print(f"Database connection failed: {e}")

    def get_connection(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
