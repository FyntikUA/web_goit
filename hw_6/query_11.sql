SELECT AVG(grade) AS avg_grade
FROM grades
JOIN subjects ON grades.subject_id = subjects.id
JOIN teachers ON subjects.teacher_id = teachers.id
WHERE teachers.name = '{teacher_name}' AND grades.student_id = {student_id};