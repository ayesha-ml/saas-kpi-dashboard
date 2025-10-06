CREATE DATABASE saas_analytics;
USE saas_analytics;

-- USERS TABLE
CREATE TABLE saas_users (
    user_id VARCHAR(20) PRIMARY KEY,
    signup_date DATE,
    plan_type VARCHAR(20),
    region VARCHAR(50),
    acquisition_channel VARCHAR(50),
    cac DECIMAL(10,2),
    churned INT,
    months_active INT
);

-- SUBSCRIPTIONS TABLE
CREATE TABLE saas_subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(20),
    plan_type VARCHAR(20),
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (user_id) REFERENCES saas_users(user_id)
);

-- TRANSACTIONS TABLE
CREATE TABLE saas_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(20),
    plan_type VARCHAR(20),
    billing_date DATE,
    amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES saas_users(user_id)
);

-- ACTIVITY TABLE
CREATE TABLE saas_activity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(20),
    activity_date DATE,
    FOREIGN KEY (user_id) REFERENCES saas_users(user_id)
);

