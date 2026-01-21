USE kenya_power_db;

-- =====================================================
-- Insert Sample Users
-- Password for all users: 'password123' (plain text)
-- =====================================================
INSERT INTO users (username, password, email, full_name, phone, role) VALUES
                                                                               ('admin', 'password123', 'admin@kenyapower.co.ke', 'System Administrator', '+254700000001', 'admin'),
                                                                               ('manager1', 'password123', 'manager@kenyapower.co.ke', 'James Mwangi', '+254700000002', 'manager'),
                                                                               ('tech1', 'password123', 'technician1@kenyapower.co.ke', 'Peter Ochieng', '+254700000003', 'technician'),
                                                                               ('tech2', 'password123', 'technician2@kenyapower.co.ke', 'Mary Wanjiku', '+254700000004', 'technician'),
                                                                               ('cs_agent1', 'password123', 'csagent1@kenyapower.co.ke', 'Sarah Kimani', '+254700000005', 'customer_service');

-- =====================================================
-- Insert Sample Customers
-- =====================================================
INSERT INTO customers (account_number, first_name, last_name, email, phone, id_number, address, county, town, customer_type) VALUES
                                                                                                                                 ('KP-2024-0001', 'John', 'Kamau', 'john.kamau@email.com', '+254711111111', '12345678', '123 Moi Avenue', 'Nairobi', 'Nairobi CBD', 'residential'),
                                                                                                                                 ('KP-2024-0002', 'Jane', 'Akinyi', 'jane.akinyi@email.com', '+254722222222', '23456789', '456 Kenyatta Street', 'Mombasa', 'Mombasa Island', 'residential'),
                                                                                                                                 ('KP-2024-0003', 'Safaricom Ltd', 'Corporate', 'power@safaricom.co.ke', '+254733333333', 'PVT-001234', 'Safaricom House, Waiyaki Way', 'Nairobi', 'Westlands', 'commercial'),
                                                                                                                                 ('KP-2024-0004', 'David', 'Mutua', 'david.mutua@email.com', '+254744444444', '34567890', '789 Oginga Odinga Road', 'Kisumu', 'Kisumu Central', 'residential'),
                                                                                                                                 ('KP-2024-0005', 'Kenya Breweries', 'Corporate', 'facilities@kbl.co.ke', '+254755555555', 'PVT-005678', 'Ruaraka Industrial Area', 'Nairobi', 'Ruaraka', 'industrial');

-- =====================================================
-- Insert Sample Connections
-- =====================================================
INSERT INTO connections (customer_id, meter_number, connection_type, load_capacity, installation_date, connection_status, location_coordinates, transformer_id, feeder_line) VALUES
                                                                                                                                                                                 (1, 'MTR-NAI-000001', 'single_phase', 5.00, '2023-01-15', 'active', '-1.2921,36.8219', 'TRF-NAI-001', 'FDR-NAI-A1'),
                                                                                                                                                                                 (2, 'MTR-MSA-000001', 'single_phase', 5.00, '2023-02-20', 'active', '-4.0435,39.6682', 'TRF-MSA-001', 'FDR-MSA-B1'),
                                                                                                                                                                                 (3, 'MTR-NAI-000002', 'three_phase', 100.00, '2022-06-10', 'active', '-1.2634,36.8076', 'TRF-NAI-002', 'FDR-NAI-A2'),
                                                                                                                                                                                 (4, 'MTR-KSM-000001', 'single_phase', 5.00, '2023-03-25', 'active', '-0.1022,34.7617', 'TRF-KSM-001', 'FDR-KSM-C1'),
                                                                                                                                                                                 (5, 'MTR-NAI-000003', 'three_phase', 500.00, '2021-11-05', 'active', '-1.2380,36.8850', 'TRF-NAI-003', 'FDR-NAI-A3');

-- =====================================================
-- Insert Sample Faults
-- =====================================================
INSERT INTO faults (connection_id, fault_type, description, location_description, reported_by_customer, severity, status, assigned_to, affected_customers) VALUES
                                                                                                                                                               (1, 'power_outage', 'Complete power outage since morning', 'Moi Avenue, Near City Hall', 1, 'high', 'assigned', 3, 150),
                                                                                                                                                               (2, 'low_voltage', 'Voltage fluctuations causing appliance damage', 'Kenyatta Street, Block B', 2, 'medium', 'in_progress', 4, 25),
                                                                                                                                                               (3, 'transformer_fault', 'Transformer making unusual noise', 'Safaricom House, Westlands', 3, 'critical', 'acknowledged', NULL, 500);

-- =====================================================
-- Insert Sample Maintenance Schedules
-- =====================================================
INSERT INTO maintenance_schedules (title, description, maintenance_type, equipment_type, equipment_id, location_description, scheduled_date, scheduled_time, estimated_duration, assigned_to, priority, created_by) VALUES
                                                                                                                                                                                                                        ('Quarterly Transformer Inspection', 'Routine inspection of transformer TRF-NAI-001', 'preventive', 'transformer', 'TRF-NAI-001', 'Moi Avenue Substation', CURDATE() + INTERVAL 7 DAY, '09:00:00', 4, 3, 'medium', 2),
                                                                                                                                                                                                                        ('Feeder Line Maintenance', 'Vegetation clearing along feeder line', 'preventive', 'feeder_line', 'FDR-MSA-B1', 'Mombasa Island Main Feeder', CURDATE() + INTERVAL 14 DAY, '08:00:00', 8, 4, 'low', 2),
                                                                                                                                                                                                                        ('Emergency Pole Replacement', 'Replace damaged pole after accident', 'emergency', 'pole', 'POL-KSM-234', 'Oginga Odinga Road, Kisumu', CURDATE() + INTERVAL 1 DAY, '07:00:00', 6, 3, 'critical', 2);

-- =====================================================
-- Insert Sample Service Requests
-- =====================================================
INSERT INTO service_requests (customer_id, connection_id, request_type, description, status, priority, assigned_to) VALUES
                                                                                                                        (1, 1, 'upgrade', 'Request to upgrade from single phase to three phase for new workshop', 'under_review', 'medium', 5),
                                                                                                                        (4, 4, 'relocation', 'Meter relocation due to house renovation', 'approved', 'low', 5);