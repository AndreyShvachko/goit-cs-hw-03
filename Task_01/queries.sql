
-- 1. Get all tasks with their status and assigned user
SELECT tasks.id, tasks.title, tasks.description, status.name AS status, users.fullname AS assigned_user
FROM tasks
LEFT JOIN status ON tasks.status_id = status.id
LEFT JOIN users ON tasks.user_id = users.id;

-- 2. Count the number of tasks in each status
SELECT status.name AS status, COUNT(tasks.id) AS task_count
FROM status
LEFT JOIN tasks ON tasks.status_id = status.id
GROUP BY status.name;

-- 3. Find all tasks assigned to a specific user by their ID (e.g., user_id = 1)
SELECT tasks.id, tasks.title, tasks.description, status.name AS status
FROM tasks
LEFT JOIN status ON tasks.status_id = status.id
WHERE tasks.user_id = 1;

-- 4. List all users and the number of tasks assigned to each
SELECT users.fullname, COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON tasks.user_id = users.id
GROUP BY users.fullname;

-- 5. Find tasks that have no assigned user
SELECT tasks.id, tasks.title, tasks.description
FROM tasks
WHERE tasks.user_id IS NULL;
