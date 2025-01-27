-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT,
    birthdate TEXT,
    gender TEXT,
    username TEXT UNIQUE,
    password TEXT
);

-- Create parent_child table with foreign key constraints
CREATE TABLE IF NOT EXISTS parent_child (
    parent_id INTEGER,
    child_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES users(id),
    FOREIGN KEY (child_id) REFERENCES users(id)
);
