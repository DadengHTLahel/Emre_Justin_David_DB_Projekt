# Autoren: Emre, Justin, David
# 1. Einheit: Emre Bacak (2 Stunden)
# 2. Einheit: David Deng (4 Stunden)
# 3. Einheit: Justin Thomaset (2 Stunden)

import tkinter as tk # Importiert das Tkinter-Modul für die GUI-Erstellung
from tkinter import ttk, messagebox # Importiert spezifische GUI-Elemente und Nachrichtenboxen
import sqlite3 # Importiert das Modul für die SQLite-Datenbank-Schnittstelle

db = sqlite3.connect("restaurant.db") # Stellt die Verbindung zur lokalen Datenbank-Datei her
cursor = db.cursor() # Erstellt ein Cursor-Objekt zum Ausführen von SQL-Befehlen

cursor.execute("PRAGMA foreign_keys = ON;") # Aktiviert die Prüfung auf Fremdschlüssel-Beziehungen

# Erstellt die Tabelle 'Gast', falls sie noch nicht existiert
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Gast (
        Gast_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        Name TEXT, 
        Telefonnummer TEXT 
    )
""")

# Erstellt die Tabelle 'Gericht' mit Fremdschlüssel und Kaskadierung beim Löschen
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Gericht (
        GerichtID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,    
        Preis FLOAT,
        Bestell_ID INTEGER,
        FOREIGN KEY (Bestell_ID) REFERENCES Bestellung(Bestell_ID) ON DELETE CASCADE
    )
""")

# Erstellt die Tabelle 'Bestellung' mit Fremdschlüssel zum Gast
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Bestellung (
        Bestell_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Gast_ID INTEGER, 
        Datum DATE, 
        FOREIGN KEY (Gast_ID) REFERENCES Gast(Gast_ID) ON DELETE CASCADE
    )
""")

class RestaurantApp: # Definition der Hauptklasse für die Applikation
    def __init__(self, root): # Konstruktor der Klasse, nimmt das Hauptfenster entgegen
        self.root = root # Speichert das Hauptfenster-Objekt
        self.root.title("Restaurant System") # Setzt den Fenstertitel
        self.db = sqlite3.connect("restaurant.db") # Verbindet die Anwendung mit der Datenbank
        self.cursor = self.db.cursor() # Initialisiert den Datenbank-Cursor

        self.notebook = ttk.Notebook(root) # Erstellt ein Registerkarten-System (Tabs)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10) # Platziert das Notebook mit Abständen

        # Erzeugt die drei Haupt-Reiter der Anwendung
        self.tab_gast = self.create_tab("Gäste", ["ID", "Name", "Telefonnummer"])
        self.tab_gericht = self.create_tab("Gerichte", ["ID", "Name", "Preis", "Bestell_ID"])
        self.tab_bestellung = self.create_tab("Bestellungen", ["Bestell_ID", "Gast_ID", "Datum"])

        self.refresh_all_tables() # Lädt initial alle Daten in die Treeviews

    def refresh_all_tables(self): # Funktion zum Aktualisieren aller Ansichten
        self.load_table(self.tab_gast, "Gast") # Aktualisiert die Gast-Tabelle
        self.load_table(self.tab_gericht, "Gericht") # Aktualisiert die Gericht-Tabelle
        self.load_table(self.tab_bestellung, "Bestellung") # Aktualisiert die Bestellung-Tabelle

    def create_tab(self, title, columns): # Erstellt einen neuen Reiter in der GUI
        frame = ttk.Frame(self.notebook) # Erstellt den Container für den Tab
        self.notebook.add(frame, text=title) # Fügt den Tab zum Notebook hinzu
        
        input_frame = ttk.Frame(frame) # Erstellt einen Rahmen für Eingabefelder
        input_frame.pack(fill='x', padx=5, pady=5) # Platziert den Rahmen horizontal
        entries = {} # Dictionary für die Referenz zu den Eingabefeldern
        for i, col in enumerate(columns[1:]): # Iteriert über die Spaltennamen
            ttk.Label(input_frame, text=col).grid(row=0, column=i*2) # Erstellt das Label für das Feld
            ent = ttk.Entry(input_frame) # Erstellt das Eingabefeld
            ent.grid(row=0, column=i*2+1) # Platziert das Eingabefeld
            entries[col] = ent # Speichert das Feld in der Dictionary
        frame.entries = entries # Speichert die Einträge im Rahmen-Objekt

        btn_frame = ttk.Frame(frame) # Erstellt einen Rahmen für die Buttons
        btn_frame.pack(fill='x') # Platziert den Button-Rahmen
        ttk.Button(btn_frame, text="Hinzufügen", command=lambda: self.add_data(title, frame)).pack(side="left")
        ttk.Button(btn_frame, text="Löschen", command=lambda: self.delete_data(frame, title)).pack(side="left")
        ttk.Button(btn_frame, text="Bearbeiten", command=lambda: self.load_to_entries(frame, title)).pack(side="left")
        ttk.Button(btn_frame, text="Speichern", command=lambda: self.update_data(frame, title)).pack(side="left")

        tree = ttk.Treeview(frame, columns=columns, show="headings") # Erstellt die tabellarische Ansicht
        for col in columns: tree.heading(col, text=col) # Setzt die Kopfzeilen der Tabelle
        tree.pack(fill='both', expand=True) # Macht die Tabelle ausfüllend
        frame.tree = tree # Speichert den Treeview im Rahmen
        return tree # Gibt die erstellte Tabelle zurück

    def add_data(self, tab_title, frame): # Funktion zur Validierung und zum Einfügen von Daten
        try: # Startet den Block zur Fehlerbehandlung
            if tab_title == "Gäste": # Logik für Gäste-Eingabe
                name = frame.entries["Name"].get() # Holt den Namen
                telefon = frame.entries["Telefonnummer"].get() # Holt die Telefonnummer
                if not name.isalpha(): # Validiert: Name muss Buchstaben sein
                    messagebox.showerror("Fehler", "Name darf nur Buchstaben enthalten!")
                    return
                if not all(c.isdigit() or c in "+-" for c in telefon): # Validiert: Telefon-Format
                    messagebox.showerror("Fehler", "Ungültige Telefonnummer!")
                    return
                self.cursor.execute("INSERT INTO Gast (Name, Telefonnummer) VALUES (?, ?)", (name, telefon))
            elif tab_title == "Bestellungen": # Logik für Bestellungs-Eingabe
                gast_id = frame.entries["Gast_ID"].get() # Holt die Gast_ID
                datum = frame.entries["Datum"].get() # Holt das Datum
                if not gast_id.isdigit(): # Validiert: ID muss Zahl sein
                    messagebox.showerror("Fehler", "Gast_ID muss eine Zahl sein!")
                    return
                if cursor.execute("SELECT Gast_ID FROM Gast WHERE Gast_ID = ?", (gast_id,)).fetchone() is None: # Prüft, ob Gast_ID existiert
                    messagebox.showerror("Fehler", "Ungültige Eingabe! Gast_ID existiert nicht!")
                    return
                self.cursor.execute("INSERT INTO Bestellung (Gast_ID, Datum) VALUES (?, ?)", (int(gast_id), datum))
            elif tab_title == "Gerichte": # Logik für Gericht-Eingabe
                name = frame.entries["Name"].get() # Holt Name des Gerichts
                preis = frame.entries["Preis"].get() # Holt den Preis
                bestell_id = frame.entries["Bestell_ID"].get() # Holt die Bestell_ID
                # Validierung der Eingabedaten für Gerichte
                if not name.isalpha() or not preis.replace('.', '', 1).isdigit() or not bestell_id.isdigit():
                    messagebox.showerror("Fehler", "Ungültige Eingabe! Name=Buchstaben, Preis/ID=Zahlen.")
                    return
                if cursor.execute("SELECT Bestell_ID FROM Bestellung WHERE Bestell_ID = ?", (bestell_id,)).fetchone() is None: # Prüft, ob Gast_ID existiert
                    messagebox.showerror("Fehler", "Ungültige Eingabe! Bestell_ID existiert nicht!")
                    return
                self.cursor.execute("INSERT INTO Gericht (Name, Preis, Bestell_ID) VALUES (?, ?, ?)", 
                                   (name, float(preis), int(bestell_id)))
            
            self.db.commit() # Speichert die Änderungen in der DB
            self.refresh_all_tables() # Aktualisiert die Tabellenansicht
            messagebox.showinfo("Erfolg", "Daten erfolgreich gespeichert!") # Bestätigungsbox
        except Exception as e: messagebox.showerror("Fehler", str(e)) # Zeigt Fehlerbox bei Problemen

    def delete_data(self, frame, tab_title): # Funktion zum Löschen von Datensätzen
        selected = frame.tree.selection() # Prüft, ob eine Zeile ausgewählt ist
        if not selected: return # Abbruch, falls keine Auswahl
        if not messagebox.askyesno("Löschen", "Sicher löschen?"): return # Sicherheitsabfrage
        item_id = frame.tree.item(selected)['values'][0] # Holt die ID des Elements
        # Mapping der Tabellen und Primärschlüssel
        mapping = {"Gäste": ("Gast", "Gast_ID"), "Gerichte": ("Gericht", "GerichtID"), "Bestellungen": ("Bestellung", "Bestell_ID")}
        table, col = mapping[tab_title] # Holt den Tabellennamen
        # Manuelle Kaskadierung (Sicherheit, falls SQL-Regel nicht greift)
        if tab_title == "Gäste": # Logik bei Löschung eines Gastes
            self.cursor.execute("SELECT Bestell_ID FROM Bestellung WHERE Gast_ID = ?", (item_id,))
            for b in self.cursor.fetchall(): # Löscht alle zugehörigen Gerichte
                self.cursor.execute("DELETE FROM Gericht WHERE Bestell_ID = ?", (b[0],))
            self.cursor.execute("DELETE FROM Bestellung WHERE Gast_ID = ?", (item_id,)) # Löscht Bestellungen
            self.cursor.execute("DELETE FROM Gast WHERE Gast_ID = ?", (item_id,)) # Löscht den Gast selbst
        elif tab_title == "Bestellungen": # Logik bei Löschung einer Bestellung
            self.cursor.execute("DELETE FROM Gericht WHERE Bestell_ID = ?", (item_id,))
            self.cursor.execute("DELETE FROM Bestellung WHERE Bestell_ID = ?", (item_id,))
        else: # Standard-Löschung für Gerichte
            self.cursor.execute(f"DELETE FROM {table} WHERE {col} = ?", (item_id,))
        self.db.commit() # Speichert Löschung
        self.refresh_all_tables() # Aktualisiert GUI

    def load_to_entries(self, frame, tab_title): # Lädt Tabellendaten in die Eingabefelder
        selected = frame.tree.selection() # Holt die Auswahl
        if not selected: return # Abbruch, wenn nichts gewählt
        values = frame.tree.item(selected)['values'] # Holt die Zeilenwerte
        for i, col in enumerate(frame.entries.keys()): # Iteriert über Felder
            frame.entries[col].delete(0, 'end') # Löscht alten Inhalt
            frame.entries[col].insert(0, values[i+1]) # Setzt neuen Inhalt
        frame.selected_id = values[0] # Speichert die ID für Update

    def update_data(self, frame, tab_title): # Aktualisiert bestehende Datensätze
        if not hasattr(frame, 'selected_id'): return # Abbruch ohne ID
        mapping = {"Gäste": ("Gast", "Gast_ID", ["Name", "Telefonnummer"]), 
                   "Gerichte": ("Gericht", "GerichtID", ["Name", "Preis", "Bestell_ID"]), 
                   "Bestellungen": ("Bestellung", "Bestell_ID", ["Gast_ID", "Datum"])}
        table, col, cols = mapping[tab_title] # Holt Mapping-Infos
        vals = [frame.entries[c].get() for c in cols] + [frame.selected_id] # Holt Werte
        query = f"UPDATE {table} SET {', '.join([c + ' = ?' for c in cols])} WHERE {col} = ?" # SQL Update Query
        self.cursor.execute(query, vals) # Führt Update aus
        self.db.commit() # Speichert Änderungen
        self.refresh_all_tables() # Aktualisiert GUI
        messagebox.showinfo("Erfolg", "Aktualisiert!") # Erfolgsmeldung

    def load_table(self, tree, table_name): # Lädt Daten aus DB in Treeview
        for row in tree.get_children(): tree.delete(row) # Leert Treeview
        self.cursor.execute(f"SELECT * FROM {table_name}") # Holt alle Daten
        for row in self.cursor.fetchall(): tree.insert("", "end", values=row) # Fügt in Treeview ein

    def __del__(self): # Destruktor beim Beenden der Klasse
        self.db.close() # Schließt Datenbankverbindung

if __name__ == "__main__": # Startet das Programm
    root = tk.Tk() # Initialisiert das Hauptfenster
    app = RestaurantApp(root) # Erstellt die App-Instanz
    root.mainloop() # Startet die GUI-Hauptschleife