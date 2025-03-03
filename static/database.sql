create table unstaffedusers (
id int auto_increment Primary key,
username varchar(50),
email varchar(250) NOT NULL,
password varchar(250) NOT NULL,
user_type varchar(250) NOT NULL,
salary varchar(250),
location varchar(250),
skills varchar(250),
about text,
fixed_rate varcahr(250)
);

ALTER TABLE unstaffedusers
ADD CONSTRAINT unique_username_password UNIQUE (username, password);


CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    message_text TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES unstaffedusers(id),
    FOREIGN KEY (receiver_id) REFERENCES unstaffedusers(id)
);

CREATE TABLE posts(
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_text TEXT,
    likes INT
);

CREATE TABLE contract(
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    freelancer_id INT,
    description VARCHAR(255),
    hourlyorfixed VARCHAR(255),
    rate INT,
    FOREIGN KEY (client_id) REFERENCES unstaffedusers(id),
    FOREIGN KEY (freelancer_id) REFERENCES unstaffedusers(id)
);
