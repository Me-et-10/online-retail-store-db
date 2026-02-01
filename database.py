# database.py - Handles database connection and schema creation
import sqlite3

DATABASE_NAME = 'retail_store.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Read schema from schema.sql
    with open('schema.sql', 'r') as f:
        schema_script = f.read()
    
    # Execute the script
    cursor.executescript(schema_script)
    conn.commit()
    conn.close()
    print(f"[*] Database tables created/ensured in {DATABASE_NAME}")

if __name__ == '__main__':
    create_tables()
    print("Database initialization complete.")
