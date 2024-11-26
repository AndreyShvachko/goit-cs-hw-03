import os
from faker import Faker
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Завантаження даних з .env файлу
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Ініціалізація Faker
fake = Faker()

# Підключення до бази даних
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("Connected to the database")
except Exception as e:
    print("Error connecting to the database:", e)
    exit()

# Функція для заповнення таблиці users
def seed_users(num_users=10):
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.unique.email()
        cursor.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s);",
            (fullname, email)
        )
    print(f"Inserted {num_users} users")

# Функція для заповнення таблиці status
def seed_status():
    statuses = [('new',), ('in progress',), ('completed',)]
    cursor.executemany(
        "INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING;",
        statuses
    )
    print("Inserted statuses")

# Функція для заповнення таблиці tasks
def seed_tasks(num_tasks=20):
    cursor.execute("SELECT id FROM users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM status;")
    status_ids = [row[0] for row in cursor.fetchall()]

    if not user_ids or not status_ids:
        print("Ensure users and statuses are seeded before tasks.")
        return

    for _ in range(num_tasks):
        title = fake.sentence(nb_words=6)
        description = fake.text()
        status_id = fake.random.choice(status_ids)
        user_id = fake.random.choice(user_ids)
        cursor.execute(
            """
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s);
            """,
            (title, description, status_id, user_id)
        )
    print(f"Inserted {num_tasks} tasks")

# Головна функція
if __name__ == "__main__":
    try:
        seed_status()
        seed_users(10)  # Кількість користувачів
        seed_tasks(20)  # Кількість завдань
        conn.commit()
    except Exception as e:
        print("Error during seeding:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

