import random
from faker import Faker
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from al_base import Base, Student, Grade, Group, Subject, Teacher

fake = Faker()

# Підключення до бази даних
engine = create_engine('sqlite:///university.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Заповнення таблиць випадковими даними
groups = [Group(name=f'Group {i}') for i in range(1, 4)]
session.add_all(groups)
session.commit()

teachers = [Teacher(name=fake.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

subjects = [Subject(name=f'Subject {i}', teacher=random.choice(teachers)) for i in range(1, 6)]
session.add_all(subjects)
session.commit()

students = [Student(name=fake.name(), group_id=random.randint(1, 3)) for _ in range(30)]
session.add_all(students)
session.commit()

# Зв'язок між студентами та групами
for student in students:
    student.group = random.choice(groups)

# Зв'язок між предметами та оцінками
for student in students:
    for subject in subjects:
        grade = Grade(student_id=student.id, subject_id=subject.id, grade=random.randint(1, 10), date=datetime.now())
        session.add(grade)

session.commit()
session.close()
