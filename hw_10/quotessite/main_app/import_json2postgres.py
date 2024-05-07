import psycopg2
import json

# З'єднання з базою даних
conn = psycopg2.connect(
    dbname="q_db",
    user="postgres",
    password="Sqrt0603",
    host="localhost",
    port="5432"
)

# Створення курсора для виконання SQL-запитів
cur = conn.cursor()

# Відкриття JSON-файлу authors.json та зчитування даних
with open('authors.json', 'r', encoding='utf-8') as file:
    authors = json.load(file)

# Перевірка існування таблиці "authors"
cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='main_app_author')")
table_exists = cur.fetchone()[0]

# Якщо таблиця "author" не існує, то створюємо її
if not table_exists:
    # SQL-запит для створення таблиці "authors"
    create_table_query = '''
    CREATE TABLE main_app_author (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100),
        born_date VARCHAR(50),
        born_location VARCHAR(100),
        description TEXT
    );
    '''
    # Виконання SQL-запиту для створення таблиці "authors"
    cur.execute(create_table_query)
    conn.commit()

# Вставка даних у таблицю "authors"
for author in authors:
    cur.execute(
        "INSERT INTO main_app_author (fullname, born_date, born_location, description) VALUES (%s, %s, %s, %s)",
        (author['fullname'], author['born_date'], author['born_location'], author['description'])
    )

# Відкриття JSON-файлу quotes.json та зчитування даних
with open('quotes.json', 'r', encoding='utf-8') as file:
    quotes = json.load(file)

# Перевірка існування таблиці "quotes"
cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='main_app_quote')")
table_exists = cur.fetchone()[0]

# Якщо таблиця "quotes" не існує, то створюємо її
if not table_exists:
    # SQL-запит для створення таблиці "quotes"
    create_table_query = '''
    CREATE TABLE main_app_quote (
        id SERIAL PRIMARY KEY,
        quote TEXT,
        author VARCHAR(100),
        tags TEXT[]
    );
    '''
    # Виконання SQL-запиту для створення таблиці "quotes"
    cur.execute(create_table_query)
    conn.commit()

# Вставка даних у таблицю "quotes"
for quote in quotes:
    cur.execute(
        "INSERT INTO main_app_quote (quote, author, tags) VALUES (%s, %s, %s)",
        (quote['quote'], quote['author'], quote['tags'])
    )

# Підтвердження та закриття з'єднання з базою даних
conn.commit()
conn.close()