CREATE DATABASE smart_agriculture;
USE smart_agriculture;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from users;
CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    temperature FLOAT,
    humidity FLOAT,
    rainfall FLOAT,
    predicted_crop VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);
select * from predictions;
CREATE TABLE weather (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100),
    temperature FLOAT,
    humidity FLOAT,
    rainfall FLOAT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from  weather;
SHOW TABLES;
INSERT INTO users (name, email, password)
VALUES ('Prasad', 'test@gmail.com', '123456');

INSERT INTO predictions (user_id, temperature, humidity, rainfall, predicted_crop)
VALUES (1, 25, 60, 100, 'rice');
SELECT * FROM users;
SELECT * FROM predictions;
