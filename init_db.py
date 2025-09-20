import sqlite3
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_database():
    """
    Creates the database file and the 'announcements' table if they don't exist.
    This ensures the application starts with a clean, correct schema.
    """
    db_name = 'data.db'
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # SQL statement to create the table
        # Using a composite UNIQUE constraint on (source, link) is robust
        # for preventing duplicate entries.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                text TEXT NOT NULL,
                link TEXT NOT NULL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source, link)
            )
        ''')
        
        conn.commit()
        logging.info(f"Database '{db_name}' checked/initialized successfully.")
        logging.info("Table 'announcements' is ready.")

    except sqlite3.Error as e:
        logging.error(f"An error occurred during database initialization: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    initialize_database()
