SELECT *
FROM (user_groups
JOIN "group" ON user_groups.group_id = "group".group_id)
WHERE user_id = 3 --- user_id