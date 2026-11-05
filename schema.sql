CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, full_name, role) VALUES
('johndoe', 'john.doe@example.com', 'John Doe', 'admin'),
('janedoe', 'jane.doe@example.com', 'Jane Doe', 'moderator'),
('alexsmith', 'alex.smith@example.com', 'Alex Smith', 'user'),
('sarahconnor', 'sarah.c@example.com', 'Sarah Connor', 'user'),
('budi_santoso', 'budi.santoso@example.com', 'Budi Santoso', 'user');
