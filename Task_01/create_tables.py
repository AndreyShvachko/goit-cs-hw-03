import psycopg2
from psycopg2 import sql

def create_tables():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234567890",
        host="localhost",
        port="5432"
    )
    
    with conn:
        with conn.cursor() as cursor:
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    fullname VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                );
            """)

            # Create status table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS status (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL
                );
            """)

            # Create tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    status_id INTEGER REFERENCES status(id),
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
                );
            """)

    print("Tables created successfully.")
    conn.close()

if __name__ == "__main__":
    create_tables()
