-- name: get-user-by-uuid^
SELECT uuid
FROM users
WHERE uuid = :uuid
LIMIT 1;




-- name: get_user_by_uuid_in_db<!
SELECT uuid,
       is_active
FROM users
WHERE uuid = :uuid
LIMIT 1;

-- name: create-user<!
INSERT INTO users (email, password)
VALUES (:email, :password)
RETURNING
    uuid, email, password;

-- name: update-user<!
UPDATE users
SET email        = :new_email,
    password       = :new_password
WHERE uuid = :uuid
  AND is_active = true
RETURNING
    uuid, email, password;




-- name: delete-user<!
UPDATE users
SET is_active        = false
WHERE uuid = :uuid

-- name: remove-user!
DELETE
FROM users
WHERE uuid = :uuid
