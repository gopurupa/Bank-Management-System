CREATE DATABASE Bank_manage_sys;
USE Bank_manage_sys;

CREATE TABLE users (
    account_no BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    account_type ENUM('Savings','Current') NOT NULL,
    pin CHAR(4) NOT NULL,
    balance DOUBLE DEFAULT 0,
    CONSTRAINT chk_name CHECK (name REGEXP '^[A-Za-z ]+$')
);
ALTER TABLE users AUTO_INCREMENT = 238007537223;

CREATE TABLE transactions (
    trans_id INT PRIMARY KEY AUTO_INCREMENT,
    account_no BIGINT,
    action ENUM('Debit','Credit') NOT NULL,
    amount DOUBLE NOT NULL,
    trans_date DATETIME NOT NULL,
    FOREIGN KEY (account_no) REFERENCES users(account_no) ON DELETE CASCADE
);

CREATE TABLE admin (
    admin_id VARCHAR(50) PRIMARY KEY,
    password VARCHAR(100) NOT NULL
);

INSERT INTO admin (admin_id, password) VALUES ('admin', 'admin123');
