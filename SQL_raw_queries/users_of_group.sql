SELECT "user".id, "user".name
FROM user_groups JOIN "user" ON user_id = "user".id
WHERE group_id = 1 ---