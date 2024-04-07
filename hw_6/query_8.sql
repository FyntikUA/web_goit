SELECT teachers.name, AVG(grades.grade) AS avg_grade
FROM teachers
JOIN subjects ON teachers.id = subjects.teacher_id
JOIN grades ON subjects.id = grades.subject_id
GROUP BY teachers.id;