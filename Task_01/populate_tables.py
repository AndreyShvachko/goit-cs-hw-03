from faker import Faker
import psycopg2

def populate_tables():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234567890",
        host="localhost",
        port="5432"
    )
    
    faker = Faker()

    with conn:
        with conn.cursor() as cursor:
            # Insert statuses
            statuses = [('new',), ('in progress',), ('completed',)]
            cursor.executemany("""
                INSERT INTO status (name) VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
            """, statuses)

            # Insert users
            users = [(faker.name(), faker.unique.email()) for _ in range(10)]
            cursor.executemany("""
                INSERT INTO users (fullname, email) VALUES (%s, %s)
                ON CONFLICT (email) DO NOTHING;
            """, users)

            # Insert tasks
            for _ in range(20):
                title = faker.sentence(nb_words=5)
                description = faker.text(max_nb_chars=200)
                status_id = faker.random_int(min=1, max=3)
                user_id = faker.random_int(min=1, max=10)

                cursor.execute("""
                    INSERT INTO tasks (title, description, status_id, user_id)
                    VALUES (%s, %s, %s, %s);
                """, (title, description, status_id, user_id))

    print("Tables populated successfully.")
    conn.close()

if __name__ == "__main__":
    populate_tables()
