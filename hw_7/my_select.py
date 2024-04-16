from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from al_base import Student, Grade, Group, Subject, Teacher

# Підключення до бази даних
engine = create_engine('sqlite:///university.db')
Session = sessionmaker(bind=engine)
session = Session()

# Запит 1: Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    top_students = (
        session.query(Student, func.avg(Grade.grade).label('avg_grade'))
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    return top_students

# Запит 2: Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_name):
    top_student = (
        session.query(Student, func.avg(Grade.grade).label('avg_grade'))
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    return top_student

# Запит 3: Знайти середній бал у групах з певного предмета.
def select_3(subject_name):
    avg_grade_per_group = (
        session.query(Group.name, func.avg(Grade.grade).label('avg_grade'))
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .all()
    )
    return avg_grade_per_group


# Запит 4: Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    avg_grade_overall = session.query(func.avg(Grade.grade)).scalar()
    return avg_grade_overall

# Запит 5: Знайти які курси читає певний викладач.
def select_5(teacher_name):
    courses_taught = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return courses_taught

# Запит 6: Знайти список студентів у певній групі.
def select_6(group_name):
    group_students = (
        session.query(Student)
        .join(Group)
        .filter(Group.name == group_name)
        .all()
    )
    return group_students

# Запит 7: Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_name, subject_name):
    group_grades = (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .join(Subject)
        .join(Group)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return group_grades

# Запит 8: Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_name):
    avg_teacher_grade = (
        session.query(func.avg(Grade.grade))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return avg_teacher_grade

# Запит 9: Знайти список курсів, які відвідує певний студент.
def select_9(student_name):
    student_courses = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .distinct()
        .all()
    )
    return student_courses

# Запит 10: Список курсів, які певному студенту читає певний викладач.
def select_10(student_name, teacher_name):
    student_teacher_courses = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Subject.teacher)
        .filter(Student.name == student_name, Subject.teacher.has(name=teacher_name))
        .distinct()
        .all()
    )
    return student_teacher_courses

# Додаткове
# Запит 11 : Середній бал, який певний викладач ставить певному студентові.
def select_avg_grade_by_teacher_and_student(teacher_name, student_name):
    avg_grade = (
        session.query(func.avg(Grade.grade))
        .join(Subject)
        .join(Teacher)
        .join(Student)
        .filter(Teacher.name == teacher_name, Student.name == student_name)
        .scalar()
    )
    return avg_grade





# Запит 1: Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
result_1 = select_1()
print("Top 5 students with the highest average grade:")
for student, avg_grade in result_1:
    print(f"Student: {student.name}, Average Grade: {avg_grade}")

# Запит 2: Знайти студента із найвищим середнім балом з певного предмета.
subject_name = "Subject 1"  
result_2 = select_2(subject_name)
print(f"Top student with the highest average grade in {subject_name}:")
if result_2:
    student, avg_grade = result_2
    print(f"Student: {student.name}, Average Grade: {avg_grade}")
else:
    print("No student found for the given subject.")

# Запит 3: Знайти середній бал у групах з певного предмета.
subject_name = "Subject 2"  
result_3 = select_3(subject_name)
print(f"Average grade per group in {subject_name}:")
for group_name, avg_grade in result_3:
    print(f"Group: {group_name}, Average Grade: {avg_grade}")

# Запит 4: Знайти середній бал на потоці (по всій таблиці оцінок).
result_4 = select_4()
print(f"Overall average grade: {result_4}")

# Запит 5: Знайти які курси читає певний викладач.
teacher_name = "Jack Hill"  
result_5 = select_5(teacher_name)
print(f"Courses taught by {teacher_name}:")
for course_name in result_5:
    print(course_name)

# Запит 6: Знайти список студентів у певній групі.
group_name = "Group 1"  
result_6 = select_6(group_name)
print(f"Students in {group_name}:")
for student in result_6:
    print(student.name)

# Запит 7: Знайти оцінки студентів у окремій групі з певного предмета.
group_name = "Group 2"  
subject_name = "Subject 2"  
result_7 = select_7(group_name, subject_name)
print(f"Grades of students in {group_name} for {subject_name}:")
for student_name, grade in result_7:
    print(f"Student: {student_name}, Grade: {grade}")

# Запит 8: Знайти середній бал, який ставить певний викладач зі своїх предметів.
teacher_name = "David Doyle"  
result_8 = select_8(teacher_name)
print(f"Average grade given by {teacher_name}: {result_8}")

# Запит 9: Знайти список курсів, які відвідує певний студент.
student_name = "Rodney Taylor"  
result_9 = select_9(student_name)
print(f"Courses attended by {student_name}:")
for course_name in result_9:
    print(course_name)

# Запит 10: Список курсів, які певному студенту читає певний викладач.
student_name = "Melissa Doyle"  
teacher_name = "Terry Stephens"  
result_10 = select_10(student_name, teacher_name)
print(f"Courses taught by {teacher_name} attended by {student_name}:")
for course_name in result_10:
    print(course_name)


# Запит 11: Середній бал, який певний викладач ставить певному студентові.
teacher_name = "David Doyle"  # Замініть на ім'я викладача
student_name = "Melissa Doyle"  # Замініть на ім'я студента
result_avg_grade = select_avg_grade_by_teacher_and_student(teacher_name, student_name)
print(f"Average grade given by {teacher_name} to {student_name}: {result_avg_grade}")





session.close()
