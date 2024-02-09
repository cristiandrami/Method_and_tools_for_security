CREATE DATABASE IF NOT EXISTS blog;
USE blog;

CREATE TABLE IF NOT EXISTS post (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT
);

CREATE TABLE IF NOT EXISTS flag (
    id INT PRIMARY KEY,
    content VARCHAR(40)
);

CREATE TABLE users (
	    uid INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
	    username VARCHAR(50) NOT NULL,
	    password VARCHAR(64) NOT NULL,  -- Storing SHA-1 hashed passwords, which are 40 characters
	    email VARCHAR(100) NOT NULL,
	    reset VARCHAR(32),  -- MD5 hash results in a 32 character string
	    is_admin BOOLEAN NOT NULL DEFAULT 0
);

INSERT INTO post (id, title, content) VALUES
    (1, 'Welcome to our blog!', 'This is the first post of our blog.'),
    (2, 'Another post', 'This is another interesting post.');

INSERT INTO users (username, password, email, is_admin) VALUES ('admin', SHA1('adminpass'), 'admin@example.com', 1);

