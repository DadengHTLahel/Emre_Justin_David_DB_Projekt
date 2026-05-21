#Emre, Justin, David
import sqlite3

db = sqlite3.connect("restaurant.db")

cursor = db.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Gast (
        Gast_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        Name TEXT, 
        Telefonnummer TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Bestellung (
        Bestell_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        Gast_ID INTEGER, 
        Datum DATE,
        FOREIGN KEY (Gast_ID) REFERENCES Gast(Gast_ID)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tisch (
        Tisch_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        Plaetze INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Rechnung (
        Rechnung_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        BestellID INTEGER,
        Gesamtpreis FLOAT,
        Datum DATE,
        FOREIGN KEY (BestellID) REFERENCES Bestellung(Bestell_ID), 
)
""")


db.commit()
cursor.close()
db.close()