import sqlite3


def create_table():
    """Create the Product table in the SQLite database."""
    conn = sqlite3.connect('shop_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def insert_test_data():
    """Insert test data into the Product table."""
    conn = sqlite3.connect('shop_db.sqlite')
    cursor = conn.cursor()

    # Test data
    products = [
        ('Product 1', 10.99),
        ('Product 2', 12.99),
        ('Product 3', 15.99)
    ]

    cursor.executemany('''
        INSERT INTO Product (name, price) VALUES (?, ?)
    ''', products)

    conn.commit()
    conn.close()


def main():
    """Main function to create the table and insert test data."""
    create_table()
    insert_test_data()
    print("Database and table created, test data inserted.")


if __name__ == "__main__":
    main()
