-- Drop the existing tables (if they exist) to start fresh
DROP TABLE IF EXISTS Chat;
DROP TABLE IF EXISTS Message;
DROP TABLE IF EXISTS Email;
DROP TABLE IF EXISTS User;

-- Create the User table
CREATE TABLE User (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  role ENUM('freelancer', 'company') NOT NULL,
  profile_pic VARCHAR(255),
  about_me TEXT,
  field VARCHAR(255),
  location VARCHAR(255),
  language VARCHAR(255),
  education VARCHAR(255),
  projects VARCHAR(255),
  pricing VARCHAR(255),
  name VARCHAR(255),
  phone VARCHAR(255),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

-- Create the Chat table
CREATE TABLE Chat (
  chat_id INT PRIMARY KEY AUTO_INCREMENT,
  freelancer_id INT,
  company_id INT,
  FOREIGN KEY (freelancer_id) REFERENCES User(user_id),
  FOREIGN KEY (company_id) REFERENCES User(user_id)
);

-- Create the Message table
CREATE TABLE Message (
  message_id INT PRIMARY KEY AUTO_INCREMENT,
  chat_id INT,
  sender_id INT,
  receiver_id INT,
  message TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (chat_id) REFERENCES Chat(chat_id),
  FOREIGN KEY (sender_id) REFERENCES User(user_id),
  FOREIGN KEY (receiver_id) REFERENCES User(user_id)
);

-- Create the Email table
CREATE TABLE Email (
  email_id INT PRIMARY KEY AUTO_INCREMENT,
  sender_id INT,
  receiver_id INT,
  subject VARCHAR(255),
  message TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES User(user_id),
  FOREIGN KEY (receiver_id) REFERENCES User(user_id)
);