--This query gets shortened names of user's courses
--Give user.id when formatting string
SELECT course_shortened, course_name, labs_amount
FROM
  (SELECT course_id, user_id
FROM
group_courses
JOIN
user_groups ON group_courses.group_id = user_groups.group_id) as g
JOIN course ON g.course_id = course.course_id
WHERE user_id = --put some integer value