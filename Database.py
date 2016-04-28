import sqlite3

print('Initializing Database...')

conn = sqlite3.connect("mydatabase.db")  # or use :memory: to put it in RAM
cursor = conn.cursor()

def print_database():
    print("\nHere's a listing of all the records in the table: (from print function)\n")
    for row in cursor.execute("SELECT rowid, * FROM fieldmap ORDER BY rowid"):
        print(row)

def initialize_database():

    # create a table
    print('Checking for existing field map...')
    try:

        cursor.execute("""CREATE TABLE fieldmap
            (buildtype TEXT, buildlevel INT)
         """)

        print('Not found! Creating new map...')

        count = 1

        while(count < 41):
            cursor.execute("INSERT INTO fieldmap (buildtype, buildlevel) VALUES (?, ?)",
                                ('none', 0))
            count += 1

    except sqlite3.OperationalError:
        print('Fieldmap found...')

