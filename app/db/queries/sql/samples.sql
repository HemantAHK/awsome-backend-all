-- name: create-sample<!
INSERT INTO samples (name, task)
VALUES (:name, :task)
RETURNING
    uuid, name, task;


-- name: get-sample-by-uuid^
SELECT uuid,
       name,
       task,
FROM samples
WHERE uuid = :uuid
LIMIT 1;




-- name: get_sample_by_uuid_in_db<!
SELECT uuid,
       name,
       task,
       is_active
FROM samples
WHERE uuid = :uuid
LIMIT 1;



-- name: update-sample<!
UPDATE samples
SET name        = :new_name,
    task       = :new_task
WHERE uuid = :uuid
  AND is_active = true
RETURNING
    uuid, name, task;



-- name: delete-sample<!
UPDATE samples
SET is_active        = false
WHERE uuid = :uuid


-- name: remove-sample!
DELETE
FROM samples
WHERE uuid = :uuid


