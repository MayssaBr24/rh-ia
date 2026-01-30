-- Création de la base de données
CREATE DATABASE IF NOT EXISTS hr_dashboard;
USE hr_dashboard;

-- Table des utilisateurs
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'rh', 'manager', 'employee') NOT NULL,
    department VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table des employés
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    department VARCHAR(50),
    position VARCHAR(100),
    hire_date DATE,
    salary DECIMAL(10,2),
    status ENUM('active', 'inactive', 'on_leave') DEFAULT 'active',
    manager_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);

-- Table des offres d'emploi
CREATE TABLE job_offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    department VARCHAR(50),
    description TEXT,
    requirements TEXT,
    status ENUM('open', 'closed', 'paused') DEFAULT 'open',
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Table des candidatures
CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_offer_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    cv_path VARCHAR(500),
    status ENUM('new', 'review', 'accepted', 'rejected') DEFAULT 'new',
    score INT DEFAULT 0,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_offer_id) REFERENCES job_offers(id)
);

-- Table du planning
CREATE TABLE planning (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    start_date DATETIME,
    end_date DATETIME,
    type ENUM('vacation', 'training', 'sick_leave', 'remote_work') NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    approved_by INT,
    comments TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- Index pour performances
CREATE INDEX idx_employees_dept ON employees(department);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_planning_employee_date ON planning(employee_id, start_date);
