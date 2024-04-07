SELECT students.name, grades.grade
FROM students
JOIN groups ON students.group_id = groups.id
JOIN grades ON students.id = grades.student_id
WHERE groups.name = '{group_name}' AND grades.subject_id = {subject_id};