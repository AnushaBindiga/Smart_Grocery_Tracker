import sqlite3
import os
DATABASE = "grocery_tracker.db" 
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    #stores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            website TEXT NOT NULL
            )
              '''  )
    #User selected stores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            selected INTEGER DEFAULT 0,
            FOREIGN KEY(store_id) REFERENCES stores(id)      
            )       
    '''    )
    #Promotions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS promotions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            original_price REAL,
            promo_price REAL,
            discount TEXT,
            date_scraped TEXT,
            FOREIGN KEY (store_id) REFERENCES stores(id)
              )                    
    '''  )
    #Grocery list table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grocery_lists(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            date_added TEXT
        )           
    ''' )

    #Recommendations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            total_savings REAL,
            items_on_promo TEXT,
            date TEXT,
            FOREIGN KEY (store_id) REFERENCES stores(id)
            )
     ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully!!")

def seed_stores():
    conn = get_connection()
    cursor = conn.cursor()

    stores = [
        ("Carrefour","carrefour.fr"),
        ("Auchan", "auchan.fr"),
        ("Lidl", "lidl.fr"),
        ("Super U", "super-u.fr"),
        ("E.Leclerc", "e.leclerc"),
        ("Intermarché", "intermarche.com")
    ]
    cursor.execute("SELECT count(*) FROM stores")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO stores(name, website) VALUES (?,?)", stores
        )

        # Set all stores as selected by default
        cursor.execute("SELECT id FROM stores")
        store_ids = cursor.fetchall()
        for store in store_ids:
            cursor.execute(
                "INSERT INTO user_stores (store_id, selected) VALUES (?, ?)",
                (store[0], 0)
            )
        conn.commit()
        print("Stores added to database!")

    conn.close()

if __name__ == "__main__":
    initialize_database()
    seed_stores()   