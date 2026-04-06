-- Student Management System Database Schema
-- Run this on your MySQL server

CREATE DATABASE IF NOT EXISTS smsdb;
USE smsdb;

CREATE USER IF NOT EXISTS 'smsuser'@'%' IDENTIFIED BY 'smspassword123';
GRANT ALL PRIVILEGES ON smsdb.* TO 'smsuser'@'%';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    credits INT DEFAULT 3,
    instructor VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    grade VARCHAR(5) DEFAULT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    UNIQUE KEY unique_enrollment (student_id, course_id)
);

-- Sample data
INSERT IGNORE INTO students (name, email, phone, department) VALUES
('Ali Hassan', 'ali.hassan@example.com', '0300-1234567', 'Computer Science'),
('Sara Khan', 'sara.khan@example.com', '0301-2345678', 'Software Engineering'),
('Ahmed Raza', 'ahmed.raza@example.com', '0302-3456789', 'Artificial Intelligence'),
('Fatima Malik', 'fatima.malik@example.com', '0303-4567890', 'Computer Science'),
('Usman Ali', 'usman.ali@example.com', '0304-5678901', 'Data Science');

INSERT IGNORE INTO courses (name, code, credits, instructor) VALUES
('DevOps for Cloud Computing', 'CSC413', 3, 'Dr. Ahmad'),
('Machine Learning', 'CSC420', 3, 'Dr. Sara'),
('Database Systems', 'CSC310', 3, 'Dr. Khalid'),
('Web Engineering', 'CSC350', 3, 'Dr. Amina'),
('Software Engineering', 'CSC301', 3, 'Dr. Bilal');

INSERT IGNORE INTO enrollments (student_id, course_id, grade) VALUES
(1, 1, 'A'), (1, 3, 'B+'),
(2, 1, 'A-'), (2, 2, 'B'),
(3, 2, 'A'), (3, 4, 'A-'),
(4, 3, 'B+'), (4, 5, 'A'),
(5, 1, 'B'), (5, 4, 'A-');
