import mysql.connector

# 1. Mit dem Server verbinden (OHNE Datenbank!)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Restaurant")

cursor.execute("USE Restaurant")


cursor.execute("CREATE TABLE IF NOT EXISTS Gast (Gast_ID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(50), Telefonnummer INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS Bestellung (Bestell_ID INT AUTO_INCREMENT PRIMARY KEY, Gast_ID INT, FOREIGN KEY (Gast_ID) REFERENCES Gast(Gast_ID), Datum DATE)")
cursor.execute("CREATE TABLE IF NOT EXISTS Tisch(Tisch_ID INT AUTO_INCREMENT PRIMARY KEY, Plätze INT)")
curs


cursor.close()
db.close()