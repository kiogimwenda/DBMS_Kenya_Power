-- Kenya Power Electrical Systems Management Database Schema
-- Created for MySQL

-- Drop existing database if needed (be careful in production!)
DROP DATABASE IF EXISTS kenya_power_db;
CREATE DATABASE kenya_power_db;
USE kenya_power_db;

-- TABLE: users
-- Purpose: Store all system users with role-based access
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role ENUM('admin', 'manager', 'technician', 'customer_service') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_username (username),
    INDEX idx_role (role)
);

-- TABLE: customers
-- Purpose: Store customer information

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20) NOT NULL,
    id_number VARCHAR(20) NOT NULL UNIQUE,
    address TEXT NOT NULL,
    county VARCHAR(50) NOT NULL,
    town VARCHAR(50) NOT NULL,
    postal_code VARCHAR(10),
    customer_type ENUM('residential', 'commercial', 'industrial') NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    -- Portal authentication fields
    password VARCHAR(255),
    portal_registered BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP NULL,

    INDEX idx_account_number (account_number),
    INDEX idx_phone (phone)
);

-- TABLE: connections
-- Purpose: Track electrical connections for customers
CREATE TABLE connections (
    connection_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    meter_number VARCHAR(20) NOT NULL UNIQUE,
    connection_type ENUM('single_phase', 'three_phase') NOT NULL,
    load_capacity DECIMAL(10,2) NOT NULL COMMENT 'in kVA',
    installation_date DATE,
    connection_status ENUM('pending', 'active', 'suspended', 'disconnected') DEFAULT 'pending',
    location_coordinates VARCHAR(50) COMMENT 'GPS coordinates',
    transformer_id VARCHAR(20),
    feeder_line VARCHAR(50),
    last_reading_date DATE,
    last_reading_value DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    INDEX idx_meter_number (meter_number),
    INDEX idx_status (connection_status)
);

-- TABLE: service_requests
-- Purpose: Handle customer service requests

CREATE TABLE service_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    connection_id INT,
    request_type ENUM('new_connection', 'upgrade', 'downgrade', 'relocation', 'name_change', 'disconnection', 'reconnection') NOT NULL,
    description TEXT,
    status ENUM('submitted', 'under_review', 'approved', 'in_progress', 'completed', 'rejected') DEFAULT 'submitted',
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    assigned_to INT,
    submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_date TIMESTAMP NULL,
    resolution_notes TEXT,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (connection_id) REFERENCES connections(connection_id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_customer (customer_id)
);


-- TABLE: faults
-- Purpose: Record and track reported faults

CREATE TABLE faults (
    fault_id INT AUTO_INCREMENT PRIMARY KEY,
    connection_id INT,
    fault_type ENUM('power_outage', 'low_voltage', 'high_voltage', 'meter_fault', 'transformer_fault', 'line_fault', 'other') NOT NULL,
    description TEXT NOT NULL,
    location_description TEXT,
    location_coordinates VARCHAR(50),
    reported_by_customer INT,
    reported_by_user INT,
    reported_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    status ENUM('reported', 'acknowledged', 'assigned', 'in_progress', 'resolved', 'closed') DEFAULT 'reported',
    assigned_to INT,
    assigned_date TIMESTAMP NULL,
    resolution_date TIMESTAMP NULL,
    resolution_notes TEXT,
    affected_customers INT DEFAULT 1,

    FOREIGN KEY (connection_id) REFERENCES connections(connection_id) ON DELETE SET NULL,
    FOREIGN KEY (reported_by_customer) REFERENCES customers(customer_id) ON DELETE SET NULL,
    FOREIGN KEY (reported_by_user) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_severity (severity),
    INDEX idx_reported_date (reported_date)
);


-- TABLE: fault_updates
-- Purpose: Track updates/progress on fault resolution

CREATE TABLE fault_updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,
    fault_id INT NOT NULL,
    updated_by INT NOT NULL,
    update_type ENUM('status_change', 'assignment', 'note', 'resolution') NOT NULL,
    previous_status VARCHAR(50),
    new_status VARCHAR(50),
    notes TEXT,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (fault_id) REFERENCES faults(fault_id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES users(user_id) ON DELETE RESTRICT
);


-- TABLE: maintenance_schedules
-- Purpose: Plan and track preventive maintenance

CREATE TABLE maintenance_schedules (
    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    maintenance_type ENUM('preventive', 'corrective', 'emergency', 'inspection') NOT NULL,
    equipment_type ENUM('transformer', 'feeder_line', 'meter', 'pole', 'substation', 'other') NOT NULL,
    equipment_id VARCHAR(50),
    location_description TEXT NOT NULL,
    location_coordinates VARCHAR(50),
    scheduled_date DATE NOT NULL,
    scheduled_time TIME,
    estimated_duration INT COMMENT 'Duration in hours',
    assigned_team VARCHAR(100),
    assigned_to INT,
    status ENUM('scheduled', 'in_progress', 'completed', 'cancelled', 'postponed') DEFAULT 'scheduled',
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    completion_date TIMESTAMP NULL,
    completion_notes TEXT,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (assigned_to) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE RESTRICT,
    INDEX idx_scheduled_date (scheduled_date),
    INDEX idx_status (status)
);


-- TABLE: maintenance_logs
-- Purpose: Log completed maintenance work

CREATE TABLE maintenance_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    maintenance_id INT NOT NULL,
    logged_by INT NOT NULL,
    work_performed TEXT NOT NULL,
    parts_used TEXT,
    issues_found TEXT,
    recommendations TEXT,
    actual_duration INT COMMENT 'Actual duration in hours',
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (maintenance_id) REFERENCES maintenance_schedules(maintenance_id) ON DELETE CASCADE,
    FOREIGN KEY (logged_by) REFERENCES users(user_id) ON DELETE RESTRICT
);


-- TABLE: notifications
-- Purpose: Store system notifications

CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    customer_id INT,
    title VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    notification_type ENUM('fault_update', 'maintenance_reminder', 'service_update', 'system', 'alert') NOT NULL,
    reference_type VARCHAR(50),
    reference_id INT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);


-- TABLE: customer_messages
-- Purpose: Customer service messaging for portal users

CREATE TABLE customer_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    user_id INT,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_from_customer BOOLEAN DEFAULT TRUE,
    is_read BOOLEAN DEFAULT FALSE,
    parent_message_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (parent_message_id) REFERENCES customer_messages(message_id) ON DELETE CASCADE,
    INDEX idx_customer (customer_id),
    INDEX idx_parent (parent_message_id)
);


-- TABLE: audit_log
-- Purpose: Track all system changes for security

CREATE TABLE audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(50),
    record_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_action_date (action_date),
    INDEX idx_user (user_id)
);


-- Create Views for Reporting


-- View: Active Faults Summary
CREATE VIEW v_active_faults AS
SELECT
    f.fault_id,
    f.fault_type,
    f.severity,
    f.status,
    f.reported_date,
    f.affected_customers,
    c.account_number,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    conn.meter_number,
    u.full_name AS assigned_technician
FROM faults f
LEFT JOIN customers c ON f.reported_by_customer = c.customer_id
LEFT JOIN connections conn ON f.connection_id = conn.connection_id
LEFT JOIN users u ON f.assigned_to = u.user_id
WHERE f.status NOT IN ('resolved', 'closed');

-- View: Maintenance Calendar
CREATE VIEW v_maintenance_calendar AS
SELECT
    m.maintenance_id,
    m.title,
    m.maintenance_type,
    m.equipment_type,
    m.scheduled_date,
    m.scheduled_time,
    m.status,
    m.priority,
    m.location_description,
    u.full_name AS assigned_technician
FROM maintenance_schedules m
LEFT JOIN users u ON m.assigned_to = u.user_id
WHERE m.status IN ('scheduled', 'in_progress');

-- View: Performance Metrics
CREATE VIEW v_fault_metrics AS
SELECT
    DATE(reported_date) AS report_date,
    COUNT(*) AS total_faults,
    SUM(CASE WHEN status = 'resolved' OR status = 'closed' THEN 1 ELSE 0 END) AS resolved_faults,
    AVG(TIMESTAMPDIFF(HOUR, reported_date, resolution_date)) AS avg_resolution_hours,
    SUM(affected_customers) AS total_affected_customers
FROM faults
GROUP BY DATE(reported_date);