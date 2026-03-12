bash - to run app
python -m frontend.login

STEPS FOR BACKEND TO WORK

-Make sure you download the SQL file Esila gave on the whatsapp group the name of the file should be "Dump20260302"
-First open MY SQL Workbench, add a new connection and have the connection name to whatever you want, the hostname should be "127.0.0.1" Port should be "3306" and Username should be "root" and then just click "ok" to make the new connection. Once you are in the connection click "Server" and then select "Data Import".
-In the data import select the "Import from Self-Contained file" and then select the "Dump20260302" that you previously downloaded and then click "New" and just name it like "asd_project".
-Now make sure "Dump Structure and Data" is selected out of the 3 options and then click start Import and then refresh your MY SQL Connection.
-You should have the Schema imported now which you can see on the right side bar of the MY SQL Workbench.
-Open our ASD-GroupProject folder and go to the file "backend/database/db.py" in the db.py file make sure to change the host, password or database if you need to.

