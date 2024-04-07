from faker import Faker
import sqlite3
import random
import os

fake = Faker()

# Функція для створення бази даних та таблиць
def create_database():
    if os.path.isfile('university.db'):
        print('Database already exists.')
        return
    
    # Використовуємо контекстний менеджер для автоматичного відкриття та закриття з'єднання
    with sqlite3.connect('university.db') as conn:
        c = conn.cursor()

        # Створення таблиці студентів
        c.execute('''CREATE TABLE students
                     (id INTEGER PRIMARY KEY,
                     name TEXT,
                     group_id INTEGER)''')

        # Створення таблиці груп
        c.execute('''CREATE TABLE groups
                     (id INTEGER PRIMARY KEY,
                     name TEXT)''')

        # Створення таблиці викладачів
        c.execute('''CREATE TABLE teachers
                     (id INTEGER PRIMARY KEY,
                     name TEXT)''')

        # Створення таблиці предметів
        c.execute('''CREATE TABLE subjects
                     (id INTEGER PRIMARY KEY,
                     name TEXT,
                     teacher_id INTEGER)''')

        # Створення таблиці оцінок
        c.execute('''CREATE TABLE grades
                     (id INTEGER PRIMARY KEY,
                     student_id INTEGER,
                     subject_id INTEGER,
                     grade INTEGER,
                     date TEXT)''')

def populate_database():
    # Використовуємо контекстний менеджер для автоматичного відкриття та закриття з'єднання
    with sqlite3.connect('university.db') as conn:
        c = conn.cursor()

        # Додавання груп
        groups = [(fake.random_int(min=100, max=999),) for _ in range(3)]
        c.executemany('INSERT INTO groups (name) VALUES (?)', groups)

        # Додавання студентів
        students = [(fake.name(), random.choice(range(1, 4))) for _ in range(30)]
        c.executemany('INSERT INTO students (name, group_id) VALUES (?, ?)', students)

        # Додавання викладачів
        teachers = [fake.name() for _ in range(3)]
        c.executemany('INSERT INTO teachers (name) VALUES (?)', [(teacher,) for teacher in teachers])

        # Додавання предметів
        subjects = [(fake.job(), random.choice(range(1, 4))) for _ in range(5)]
        c.executemany('INSERT INTO subjects (name, teacher_id) VALUES (?, ?)', subjects)

        # Додавання оцінок
        grades = [(random.choice(range(1, 31)), random.choice(range(1, 6)), random.choice(range(1, 11)), fake.date()) for _ in range(100)]
        c.executemany('INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)', grades)


# Створення та наповнення бази даних
create_database()
populate_database()
