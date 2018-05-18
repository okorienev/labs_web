SELECT "group".group_id
FROM "group"
JOIN group_courses ON group_courses.group_id = "group".group_id
WHERE course_id = 1