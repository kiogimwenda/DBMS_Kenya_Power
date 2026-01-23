.md fil# Kenya Power Electrical Systems Management Application

## Comprehensive Project Documentation

**Course:** Database Management Systems
**Project Title:** Kenya Power Electrical Systems Management Application
**Technology Stack:** Python Flask, MySQL, SQLAlchemy ORM, Bootstrap 5
**Documentation Version:** 1.0
**Last Updated:** January 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Requirements Compliance Matrix](#2-requirements-compliance-matrix)
3. [System Architecture](#3-system-architecture)
4. [Project Directory Structure](#4-project-directory-structure)
5. [Database Design](#5-database-design)
6. [Backend Implementation](#6-backend-implementation)
7. [Frontend Implementation](#7-frontend-implementation)
8. [Authentication and Authorization](#8-authentication-and-authorization)
9. [Feature Documentation](#9-feature-documentation)
10. [API Endpoints Reference](#10-api-endpoints-reference)
11. [Configuration and Deployment](#11-configuration-and-deployment)
12. [User Guide](#12-user-guide)
13. [Testing and Validation](#13-testing-and-validation)
14. [Default Credentials](#14-default-credentials)

---

## 1. Executive Summary

### 1.1 Project Overview

The Kenya Power Electrical Systems Management Application is a comprehensive web-based solution designed to manage electrical utility operations for Kenya Power. The system provides two distinct portals:

1. **Staff Portal**: For Kenya Power employees (administrators, managers, technicians, and customer service agents) to manage customers, electrical connections, fault reports, maintenance schedules, and generate performance reports.

2. **Customer Portal**: A self-service interface for Kenya Power customers to view their connections, report faults, submit service requests, communicate with customer support, and manage their profiles.

### 1.2 Key Features

- **Customer Management**: Complete CRUD operations for customer accounts with unique account numbering
- **Connection Management**: Track electrical connections/meters with status management
- **Fault Management**: Report, assign, track, and resolve electrical faults
- **Maintenance Scheduling**: Schedule and track preventive and corrective maintenance
- **Performance Reporting**: Analytics dashboards with charts and KPIs
- **Customer Self-Service**: Portal for customers to interact with Kenya Power
- **Role-Based Access Control**: Four staff roles with granular permissions
- **Real-Time Notifications**: System notifications for important events
- **Customer Support Messaging**: Two-way communication between customers and staff

### 1.3 Technology Justification

| Technology | Purpose | Justification |
|------------|---------|---------------|
| Python Flask | Web Framework | Lightweight, flexible, extensive ecosystem |
| MySQL | Database | Industry-standard RDBMS, ACID compliance, scalability |
| SQLAlchemy | ORM | Pythonic database operations, relationship management |
| Flask-Login | Authentication | Secure session management for staff users |
| Bootstrap 5 | UI Framework | Responsive design, modern components |
| Jinja2 | Templating | Server-side rendering, template inheritance |

---

## 2. Requirements Compliance Matrix

This section evaluates the project against the specified design objectives, specifications, and expected deliverables.

### 2.1 Design Objectives Compliance

#### Objective 1: Customer Connection Management
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Track customer connections | **MET** | `Connection` model with full lifecycle tracking |
| Connection requests | **MET** | `ServiceRequest` model with `new_connection` type |
| Installation dates | **MET** | `installation_date` field in Connection model |
| Service status | **MET** | `connection_status` field (pending/active/suspended/disconnected) |

**Presentation Procedure:**
1. Login as admin at `/login` (admin/admin123)
2. Navigate to **Customers** > **Add Customer** to create a new customer
3. Navigate to **Connections** > **Add Connection** to create a new connection for the customer
4. Demonstrate connection status changes via the connection detail page
5. Show the auto-generated meter number (MTR-XXX-NNNNNN format)

---

#### Objective 2: Fault Reporting and Resolution
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Report faults | **MET** | Staff portal: `/faults/report`, Customer portal: `/portal/faults/report` |
| Log repair requests | **MET** | Fault updates tracked in `FaultUpdate` model |
| Track resolution process | **MET** | 6-stage workflow: reported → acknowledged → assigned → in_progress → resolved → closed |
| Timely repairs | **MET** | Resolution time calculation, technician notifications |

**Presentation Procedure:**
1. Login as customer service agent (cs_agent1/password123)
2. Navigate to **Faults** > **Report Fault** and submit a new fault
3. Login as manager (manager1/password123)
4. View the fault and assign it to a technician (tech1)
5. Show notification created for the technician
6. Login as technician (tech1/password123) and update fault status to "In Progress" then "Resolved"
7. Demonstrate resolution time calculation in fault details

---

#### Objective 3: Maintenance Scheduling
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Planning preventive maintenance | **MET** | `MaintenanceSchedule` model with type='preventive' |
| Distribution lines maintenance | **MET** | `equipment_type` includes 'feeder_line', 'transformer', etc. |
| Reduce outage risk | **MET** | Calendar view, priority levels, technician assignments |

**Presentation Procedure:**
1. Login as manager (manager1/password123)
2. Navigate to **Maintenance** > **Schedule Maintenance**
3. Create a preventive maintenance task for a transformer
4. Navigate to **Maintenance** > **Calendar** to view the calendar interface
5. Click on the scheduled event to view details
6. Add a maintenance log entry with work performed and parts used

---

#### Objective 4: Performance Reporting
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Maintenance activity reports | **MET** | `/reports/maintenance` with completion rates |
| Fault resolution times | **MET** | `/reports/faults` with avg resolution time calculation |
| Distribution system performance | **MET** | `/reports/performance` with KPI dashboard |
| Data-driven decision-making | **MET** | Chart.js visualizations (doughnut, bar, line charts) |

**Presentation Procedure:**
1. Login as admin or manager
2. Navigate to **Reports** in the sidebar
3. Click **Fault Reports** - show the date filter, summary cards, and three interactive charts:
   - Faults by Type (doughnut chart)
   - Faults by Severity (bar chart)
   - Daily Fault Trend (line chart)
4. Click **Maintenance Reports** - show scheduled vs completed statistics
5. Click **Performance Dashboard** - show KPIs including resolution rate with progress bar

---

#### Objective 5: User Roles and Access Control
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Field technicians role | **MET** | `technician` role - sees only assigned faults/maintenance, cannot create connections |
| Customer service agents role | **MET** | `customer_service` role - full customer management access, view-only for connections |
| Management role | **MET** | `manager` role - full operational access + reports + connection creation |
| Admin role | **MET** | `admin` role - full system access including staff management |
| Data integrity | **MET** | Role-based decorators restrict unauthorized access |

**Presentation Procedure:**
1. Login as different users and show sidebar differences:
   - **Admin**: Shows "Administration" > "Staff Management"
   - **Manager**: Shows "Reports" section, can create connections, no staff management
   - **Technician**: Shows only assigned items, no reports, cannot create connections
   - **Customer Service**: Full customer access, no reports, cannot create connections
2. Try accessing `/staff/` as a manager - show "permission denied" message
3. Login as technician and try to access `/connections/add` - show "permission denied"
4. Login as technician and show filtered fault list (only assigned faults)
5. Login to customer portal and show "New Connection" option in service requests

---

### 2.2 Specifications Compliance

#### Specification 1: Customer Connection Management Schema
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Customer profiles table | **MET** | `customers` table with 17 fields |
| Connection details table | **MET** | `connections` table with 14 fields |
| Service requests table | **MET** | `service_requests` table with 12 fields |
| Unique identifier | **MET** | `account_number` (KP-YYYY-NNNN) and `meter_number` (MTR-XXX-NNNNNN) |
| Status tracking | **MET** | `connection_status` and service history via relationships |

**Presentation Procedure:**
1. Show database schema in the documentation (Section 5: Database Design)
2. Create a customer and show the auto-generated account number
3. Add a connection and show the auto-generated meter number
4. View customer profile showing connections and service request history

---

#### Specification 2: Fault Reporting Interface with Notifications
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Customer interface for faults | **MET** | Customer portal at `/portal/faults/report` |
| Technician interface | **MET** | Staff portal at `/faults/` with assignment workflow |
| Automated notifications to technicians | **MET** | `Notification` created on fault assignment |
| Automated notifications to customers | **MET** | `Notification` created on fault report and status changes |

**Presentation Procedure:**
1. Register a customer for the portal (create customer, then register at `/portal/register`)
2. Login to customer portal and report a fault
3. Show notification created for the customer
4. Login as manager and assign fault to technician
5. Show notification created for the technician
6. View the fault update history showing all status changes

---

#### Specification 3: Maintenance Scheduling System
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Create maintenance tasks | **MET** | `/maintenance/schedule` form with all required fields |
| Reminders | **MET** | Notifications sent to assigned technicians |
| Log completed work | **MET** | `MaintenanceLog` model for work records |
| User-friendly interface | **MET** | Calendar view with color-coded events |

**Presentation Procedure:**
1. Schedule a new maintenance task with date, time, priority, and technician
2. View the maintenance calendar showing color-coded events:
   - Blue: Scheduled
   - Orange: In Progress
   - Green: Completed
   - Red: Cancelled
3. Click on an event to view details
4. Add a maintenance log with work performed, parts used, and recommendations
5. Mark maintenance as completed

---

#### Specification 4: Performance Reporting Capabilities
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Fault resolution time insights | **MET** | Average resolution time calculated and displayed |
| Maintenance efficiency | **MET** | Completion rate statistics |
| Performance metrics | **MET** | KPIs: total customers, active connections, resolution rate |
| Visual representations | **MET** | Chart.js charts: doughnut, bar, line graphs |

**Presentation Procedure:**
1. Navigate to Reports > Fault Reports
2. Adjust date range filter and regenerate report
3. Show the three charts updating with filtered data
4. Navigate to Performance Dashboard
5. Explain each KPI metric and how it's calculated
6. Show the progress bar visualization for resolution rate

---

#### Specification 5: Role-Based Access Control
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Field technicians access | **MET** | Access to assigned faults and maintenance only |
| Management oversight | **MET** | Full access to all operations and reports |
| Role-specific permissions | **MET** | `@role_required()` decorator on protected routes |

**Presentation Procedure:**
1. Show the `decorators.py` file explaining the `role_required` function
2. Demonstrate route protection:
   - Try accessing `/reports/` as technician → redirected with error
   - Try accessing `/staff/` as manager → redirected with error
3. Show how technician fault list is filtered to only show assigned faults

---

### 2.3 Expected Deliverables Compliance

#### Deliverable 1: Database Design Documentation
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Entity-Relationship Diagrams | **MET** | ERD in Section 5 of this documentation |
| Relationships documented | **MET** | All foreign keys and relationships explained |
| Attributes documented | **MET** | Complete field specifications for all 10 tables |

**Presentation Procedure:**
1. Open this documentation and navigate to Section 5: Database Design
2. Show the ERD diagram illustrating all entity relationships
3. Explain the relationship between key entities:
   - Customer → Connections (one-to-many)
   - Connection → Faults (one-to-many)
   - Fault → FaultUpdates (one-to-many)
4. Show the SQL schema in Appendix A

---

#### Deliverable 2: Front-End Application
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Fully functional web application | **MET** | Flask web app with Bootstrap 5 UI |
| Adheres to business rules | **MET** | All workflows implemented as specified |
| Seamless user experience | **MET** | Responsive design, intuitive navigation |

**Presentation Procedure:**
1. Open the application at `http://127.0.0.1:5000/`
2. Show the landing page with dual portal navigation
3. Demonstrate responsive design (resize browser window)
4. Navigate through staff portal showing:
   - Dashboard with statistics
   - Sidebar navigation
   - Flash message notifications
5. Navigate through customer portal showing self-service features

---

#### Deliverable 3: Fault Reporting and Maintenance Scheduling Module
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Report faults | **MET** | Both staff and customer fault reporting |
| Schedule maintenance | **MET** | Full scheduling with calendar view |
| Track status | **MET** | Real-time status tracking with history |

**Presentation Procedure:**
1. **Fault Module Demo:**
   - Report a new fault from staff portal
   - Assign to technician
   - Update status through workflow
   - View resolution time and update history
2. **Maintenance Module Demo:**
   - Schedule preventive maintenance
   - View in calendar
   - Add work log
   - Mark as completed

---

#### Deliverable 4: Performance Reporting Tools
| Requirement | Status | Implementation Details |
|-------------|--------|------------------------|
| Fault resolution reports | **MET** | `/reports/faults` with charts |
| Maintenance activity reports | **MET** | `/reports/maintenance` with statistics |
| Visual representations | **MET** | Chart.js: doughnut, bar, and line charts |

**Presentation Procedure:**
1. Navigate to Reports section
2. Show each report type:
   - **Fault Reports**: 3 interactive charts + summary statistics
   - **Maintenance Reports**: Completion statistics by type and equipment
   - **Performance Dashboard**: KPI cards with visual metrics
3. Demonstrate date range filtering
4. Explain how metrics are calculated (show route code if needed)

---

#### Deliverable 5: Comprehensive Project Report
| Component | Status | Location |
|-----------|--------|----------|
| Executive Summary | **MET** | Section 1 of this document |
| System Architecture | **MET** | Section 3 with diagrams |
| User Guide | **MET** | Section 12 of this document |
| Testing & Validation | **MET** | Section 13 of this document |

**Presentation Procedure:**
1. Open this documentation file (`PROJECT_DOCUMENTATION.md`)
2. Walk through each major section
3. Highlight the compliance matrix (this section)
4. Show the User Guide with workflow descriptions
5. Present the Testing & Validation results

---

### 2.4 Compliance Summary

| Category | Total Requirements | Met | Partially Met | Not Met |
|----------|-------------------|-----|---------------|---------|
| Design Objectives | 5 | 5 | 0 | 0 |
| Specifications | 5 | 5 | 0 | 0 |
| Expected Deliverables | 5 | 5 | 0 | 0 |
| **TOTAL** | **15** | **15** | **0** | **0** |

**Overall Compliance: 100%**

All design objectives, specifications, and expected deliverables have been fully implemented and are ready for demonstration.

---

## 3. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌──────────────────────┐    ┌──────────────────────┐          │
│  │    Staff Portal      │    │   Customer Portal    │          │
│  │  (Bootstrap 5 UI)    │    │  (Bootstrap 5 UI)    │          │
│  └──────────────────────┘    └──────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER (Flask)                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │    Routes   │ │   Models    │ │   Utils     │ │ Templates │ │
│  │ (Blueprints)│ │(SQLAlchemy) │ │(Decorators) │ │ (Jinja2)  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER (MySQL)                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    kenya_power_db                         │   │
│  │  users | customers | connections | faults | maintenance   │   │
│  │  service_requests | notifications | customer_messages     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Application Factory Pattern

The application uses Flask's Application Factory pattern (`create_app()`) which provides:

- **Modularity**: Easy configuration switching between development/production
- **Testing**: Ability to create multiple app instances for testing
- **Blueprint Registration**: Clean separation of route modules
- **Extension Initialization**: Proper initialization of Flask extensions

### 2.3 Blueprint Architecture

The application is organized into 9 blueprints:

| Blueprint | URL Prefix | Purpose |
|-----------|------------|---------|
| `auth_bp` | `/` | Staff authentication (login, logout, register) |
| `main_bp` | `/` | Landing page and dashboard |
| `customers_bp` | `/customers` | Customer account management |
| `connections_bp` | `/connections` | Electrical connection management |
| `faults_bp` | `/faults` | Fault reporting and tracking |
| `maintenance_bp` | `/maintenance` | Maintenance scheduling |
| `reports_bp` | `/reports` | Performance reporting and analytics |
| `staff_bp` | `/staff` | Staff member management (admin only) |
| `customer_bp` | `/portal` | Customer self-service portal |

---

## 4. Project Directory Structure

```
Kenya_Power/
├── app/                                    # Main application package
│   ├── __init__.py                        # Application factory
│   ├── models/
│   │   └── __init__.py                    # Database models (10 models)
│   ├── routes/
│   │   ├── __init__.py                    # Routes package init
│   │   ├── auth.py                        # Staff authentication
│   │   ├── main.py                        # Home and dashboard
│   │   ├── customers.py                   # Customer CRUD
│   │   ├── connections.py                 # Connection CRUD
│   │   ├── faults.py                      # Fault management
│   │   ├── maintenance.py                 # Maintenance scheduling
│   │   ├── reports.py                     # Analytics and reports
│   │   ├── staff.py                       # Staff management
│   │   └── customer.py                    # Customer portal
│   ├── templates/                         # Jinja2 templates
│   │   ├── base.html                      # Staff portal layout
│   │   ├── index.html                     # Landing page
│   │   ├── dashboard.html                 # Staff dashboard
│   │   ├── auth/                          # Authentication templates
│   │   ├── customers/                     # Customer management templates
│   │   ├── connections/                   # Connection templates
│   │   ├── faults/                        # Fault management templates
│   │   ├── maintenance/                   # Maintenance templates
│   │   ├── reports/                       # Report templates
│   │   ├── staff/                         # Staff management templates
│   │   └── customer/                      # Customer portal templates
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css                  # Staff portal styles
│   │   │   └── customer-portal.css        # Customer portal styles
│   │   └── js/
│   │       └── main.js                    # JavaScript functionality
│   └── utils/
│       ├── __init__.py                    # Utils package init
│       ├── decorators.py                  # Role-based access control
│       └── customer_auth.py               # Customer authentication
├── config.py                              # Application configuration
├── main.py                                # Entry point with CLI commands
├── run.py                                 # Development server runner
├── init_db.py                             # Database initialization script
└── requirements.txt                       # Python dependencies
```

---

## 5. Database Design

### 4.1 Entity-Relationship Overview

The database consists of 10 interconnected tables implementing a relational model for utility management:

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    users     │       │  customers   │       │ connections  │
│──────────────│       │──────────────│       │──────────────│
│ user_id (PK) │       │customer_id(PK)│◄─────│connection_id │
│ username     │       │account_number │       │ customer_id  │
│ password     │       │ first_name   │       │ meter_number │
│ email        │       │ last_name    │       │ connection_  │
│ full_name    │       │ email        │       │   type       │
│ phone        │       │ phone        │       │ load_capacity│
│ role         │       │ id_number    │       │ status       │
│ is_active    │       │ address      │       │ transformer  │
│ created_at   │       │ county       │       │ feeder_line  │
└──────────────┘       │ customer_type│       └──────────────┘
       │               │ password     │              │
       │               │ portal_reg   │              │
       │               └──────────────┘              │
       │                      │                      │
       ▼                      ▼                      ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    faults    │       │service_      │       │fault_updates │
│──────────────│       │requests      │       │──────────────│
│ fault_id(PK) │       │──────────────│       │ update_id(PK)│
│ connection_id│       │request_id(PK)│       │ fault_id(FK) │
│ fault_type   │       │customer_id   │       │ updated_by   │
│ description  │       │connection_id │       │ update_type  │
│ reported_by_ │       │request_type  │       │ prev_status  │
│   customer   │       │description   │       │ new_status   │
│ reported_by_ │       │status        │       │ notes        │
│   user       │       │priority      │       │ update_date  │
│ severity     │       │assigned_to   │       └──────────────┘
│ status       │       │submitted_date│
│ assigned_to  │       │resolved_date │
│ resolution_  │       └──────────────┘
│   date       │
└──────────────┘

┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│ maintenance_ │       │maintenance_  │       │notifications │
│ schedules    │       │ logs         │       │──────────────│
│──────────────│       │──────────────│       │notification_ │
│maintenance_  │       │ log_id (PK)  │       │   id (PK)    │
│   id (PK)    │◄──────│maintenance_id│       │ user_id (FK) │
│ title        │       │ logged_by    │       │customer_id   │
│ description  │       │work_performed│       │ title        │
│ maint_type   │       │ parts_used   │       │ message      │
│ equipment_   │       │ issues_found │       │notif_type    │
│   type       │       │ recommend.   │       │ is_read      │
│ scheduled_   │       │actual_dur.   │       │ created_at   │
│   date       │       │ log_date     │       └──────────────┘
│ assigned_to  │       └──────────────┘
│ status       │                              ┌──────────────┐
│ priority     │                              │customer_     │
│ created_by   │                              │messages      │
└──────────────┘                              │──────────────│
                                              │message_id(PK)│
                                              │customer_id   │
                                              │ user_id      │
                                              │ subject      │
                                              │ message      │
                                              │is_from_cust. │
                                              │parent_msg_id │
                                              │ created_at   │
                                              └──────────────┘
```

### 4.2 Detailed Model Specifications

#### 4.2.1 User Model (`users` table)

**Purpose**: Stores staff/admin accounts for system authentication and authorization.

**File Location**: `app/models/__init__.py` (Lines 15-43)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `user_id` | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique staff identifier |
| `username` | String(50) | UNIQUE, NOT NULL | Login username |
| `password` | String(255) | NOT NULL | Stored password |
| `email` | String(100) | UNIQUE, NOT NULL | Staff email address |
| `full_name` | String(100) | NOT NULL | Staff full name |
| `phone` | String(20) | NULLABLE | Contact phone number |
| `role` | Enum | NOT NULL | One of: 'admin', 'manager', 'technician', 'customer_service' |
| `is_active` | Boolean | DEFAULT TRUE | Account active status |
| `created_at` | DateTime | DEFAULT NOW | Account creation timestamp |
| `updated_at` | DateTime | ON UPDATE NOW | Last modification timestamp |

**Relationships**:
- `assigned_faults`: One-to-Many with Fault (faults assigned to technician)
- `assigned_maintenance`: One-to-Many with MaintenanceSchedule

**Methods**:
```python
def get_id(self):
    """Return user ID for Flask-Login"""
    return str(self.user_id)

def set_password(self, password):
    """Store password (plain text for demo)"""
    self.password = password

def check_password(self, password):
    """Verify password"""
    return self.password == password
```

#### 4.2.2 Customer Model (`customers` table)

**Purpose**: Stores Kenya Power customer information and portal credentials.

**File Location**: `app/models/__init__.py` (Lines 46-89)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `customer_id` | Integer | PRIMARY KEY | Unique customer identifier |
| `account_number` | String(20) | UNIQUE, NOT NULL | Kenya Power account number (KP-YYYY-NNNN) |
| `first_name` | String(50) | NOT NULL | Customer first name |
| `last_name` | String(50) | NOT NULL | Customer last name |
| `email` | String(100) | NULLABLE | Customer email |
| `phone` | String(20) | NOT NULL | Contact phone number |
| `id_number` | String(20) | UNIQUE, NOT NULL | National ID/Passport number |
| `address` | Text | NOT NULL | Physical address |
| `county` | String(50) | NOT NULL | County of residence |
| `town` | String(50) | NOT NULL | Town/City |
| `postal_code` | String(10) | NULLABLE | Postal code |
| `customer_type` | Enum | NOT NULL | 'residential', 'commercial', or 'industrial' |
| `registration_date` | DateTime | DEFAULT NOW | Account creation date |
| `is_active` | Boolean | DEFAULT TRUE | Account status |
| `password` | String(255) | NULLABLE | Portal login password |
| `portal_registered` | Boolean | DEFAULT FALSE | Portal registration status |
| `last_login` | DateTime | NULLABLE | Last portal login timestamp |

**Relationships**:
- `connections`: One-to-Many with Connection
- `service_requests`: One-to-Many with ServiceRequest
- `reported_faults`: One-to-Many with Fault
- `messages`: One-to-Many with CustomerMessage

**Computed Properties**:
```python
@property
def full_name(self):
    return f"{self.first_name} {self.last_name}"
```

#### 4.2.3 Connection Model (`connections` table)

**Purpose**: Represents electrical connections/meters for customers.

**File Location**: `app/models/__init__.py` (Lines 92-116)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `connection_id` | Integer | PRIMARY KEY | Unique connection identifier |
| `customer_id` | Integer | FOREIGN KEY | Reference to customers table |
| `meter_number` | String(20) | UNIQUE, NOT NULL | Meter serial number (MTR-XXX-NNNNNN) |
| `connection_type` | Enum | NOT NULL | 'single_phase' or 'three_phase' |
| `load_capacity` | Decimal(10,2) | NOT NULL | Maximum load in kVA |
| `installation_date` | Date | NULLABLE | Meter installation date |
| `connection_status` | Enum | DEFAULT 'pending' | 'pending', 'active', 'suspended', 'disconnected' |
| `location_coordinates` | String(50) | NULLABLE | GPS coordinates |
| `transformer_id` | String(20) | NULLABLE | Associated transformer ID |
| `feeder_line` | String(50) | NULLABLE | Feeder line identifier |
| `last_reading_date` | Date | NULLABLE | Last meter reading date |
| `last_reading_value` | Decimal(12,2) | NULLABLE | Last reading value (kWh) |
| `created_at` | DateTime | DEFAULT NOW | Record creation timestamp |
| `updated_at` | DateTime | ON UPDATE NOW | Last update timestamp |

**Relationships**:
- `customer`: Many-to-One with Customer (backref)
- `faults`: One-to-Many with Fault
- `service_requests`: One-to-Many with ServiceRequest

#### 4.2.4 Fault Model (`faults` table)

**Purpose**: Tracks electrical fault reports from creation to resolution.

**File Location**: `app/models/__init__.py` (Lines 119-152)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `fault_id` | Integer | PRIMARY KEY | Unique fault identifier |
| `connection_id` | Integer | FOREIGN KEY | Associated connection (optional) |
| `fault_type` | Enum | NOT NULL | Type of fault (see below) |
| `description` | Text | NOT NULL | Detailed fault description |
| `location_description` | Text | NULLABLE | Location details |
| `location_coordinates` | String(50) | NULLABLE | GPS coordinates |
| `reported_by_customer` | Integer | FOREIGN KEY | Customer who reported |
| `reported_by_user` | Integer | FOREIGN KEY | Staff who reported |
| `reported_date` | DateTime | DEFAULT NOW | Report timestamp |
| `severity` | Enum | DEFAULT 'medium' | 'low', 'medium', 'high', 'critical' |
| `status` | Enum | DEFAULT 'reported' | Workflow status (see below) |
| `assigned_to` | Integer | FOREIGN KEY | Assigned technician |
| `assigned_date` | DateTime | NULLABLE | Assignment timestamp |
| `resolution_date` | DateTime | NULLABLE | Resolution timestamp |
| `resolution_notes` | Text | NULLABLE | Resolution details |
| `affected_customers` | Integer | DEFAULT 1 | Number of affected customers |

**Fault Types**:
- `power_outage`: Complete power loss
- `low_voltage`: Below normal voltage
- `high_voltage`: Above normal voltage
- `meter_fault`: Meter malfunction
- `transformer_fault`: Transformer issues
- `line_fault`: Power line damage
- `other`: Miscellaneous faults

**Status Workflow**:
```
reported → acknowledged → assigned → in_progress → resolved → closed
```

**Computed Properties**:
```python
@property
def resolution_time_hours(self):
    """Calculate resolution time in hours"""
    if self.resolution_date and self.reported_date:
        delta = self.resolution_date - self.reported_date
        return delta.total_seconds() / 3600
    return None
```

#### 4.2.5 FaultUpdate Model (`fault_updates` table)

**Purpose**: Tracks all changes and notes added to fault reports.

**File Location**: `app/models/__init__.py` (Lines 155-172)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `update_id` | Integer | PRIMARY KEY | Unique update identifier |
| `fault_id` | Integer | FOREIGN KEY, NOT NULL | Parent fault reference |
| `updated_by` | Integer | FOREIGN KEY, NOT NULL | Staff who made update |
| `update_type` | Enum | NOT NULL | 'status_change', 'assignment', 'note', 'resolution' |
| `previous_status` | String(50) | NULLABLE | Status before change |
| `new_status` | String(50) | NULLABLE | Status after change |
| `notes` | Text | NULLABLE | Update notes/comments |
| `update_date` | DateTime | DEFAULT NOW | Update timestamp |

#### 4.2.6 MaintenanceSchedule Model (`maintenance_schedules` table)

**Purpose**: Manages scheduled maintenance activities.

**File Location**: `app/models/__init__.py` (Lines 175-205)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `maintenance_id` | Integer | PRIMARY KEY | Unique maintenance identifier |
| `title` | String(100) | NOT NULL | Maintenance title |
| `description` | Text | NULLABLE | Detailed description |
| `maintenance_type` | Enum | NOT NULL | 'preventive', 'corrective', 'emergency', 'inspection' |
| `equipment_type` | Enum | NOT NULL | 'transformer', 'feeder_line', 'meter', 'pole', 'substation', 'other' |
| `equipment_id` | String(50) | NULLABLE | Specific equipment identifier |
| `location_description` | Text | NOT NULL | Maintenance location |
| `location_coordinates` | String(50) | NULLABLE | GPS coordinates |
| `scheduled_date` | Date | NOT NULL | Planned date |
| `scheduled_time` | Time | NULLABLE | Planned time |
| `estimated_duration` | Integer | NULLABLE | Duration in minutes |
| `assigned_team` | String(100) | NULLABLE | Team name |
| `assigned_to` | Integer | FOREIGN KEY | Assigned technician |
| `status` | Enum | DEFAULT 'scheduled' | 'scheduled', 'in_progress', 'completed', 'cancelled', 'postponed' |
| `priority` | Enum | DEFAULT 'medium' | 'low', 'medium', 'high', 'critical' |
| `completion_date` | DateTime | NULLABLE | Actual completion timestamp |
| `completion_notes` | Text | NULLABLE | Completion details |
| `created_by` | Integer | FOREIGN KEY, NOT NULL | Creator staff ID |
| `created_at` | DateTime | DEFAULT NOW | Creation timestamp |
| `updated_at` | DateTime | ON UPDATE NOW | Last update timestamp |

#### 4.2.7 MaintenanceLog Model (`maintenance_logs` table)

**Purpose**: Records work performed during maintenance activities.

**File Location**: `app/models/__init__.py` (Lines 208-226)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `log_id` | Integer | PRIMARY KEY | Unique log identifier |
| `maintenance_id` | Integer | FOREIGN KEY, NOT NULL | Parent maintenance reference |
| `logged_by` | Integer | FOREIGN KEY, NOT NULL | Staff who logged |
| `work_performed` | Text | NOT NULL | Description of work done |
| `parts_used` | Text | NULLABLE | Parts/materials used |
| `issues_found` | Text | NULLABLE | Problems discovered |
| `recommendations` | Text | NULLABLE | Follow-up recommendations |
| `actual_duration` | Integer | NULLABLE | Actual time spent (minutes) |
| `log_date` | DateTime | DEFAULT NOW | Log timestamp |

#### 4.2.8 ServiceRequest Model (`service_requests` table)

**Purpose**: Tracks customer service requests for various operations.

**File Location**: `app/models/__init__.py` (Lines 229-249)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `request_id` | Integer | PRIMARY KEY | Unique request identifier |
| `customer_id` | Integer | FOREIGN KEY, NOT NULL | Requesting customer |
| `connection_id` | Integer | FOREIGN KEY | Related connection (optional) |
| `request_type` | Enum | NOT NULL | Request type (see below) |
| `description` | Text | NULLABLE | Request details |
| `status` | Enum | DEFAULT 'submitted' | Request status |
| `priority` | Enum | DEFAULT 'medium' | 'low', 'medium', 'high', 'urgent' |
| `assigned_to` | Integer | FOREIGN KEY | Assigned staff |
| `submitted_date` | DateTime | DEFAULT NOW | Submission timestamp |
| `resolved_date` | DateTime | NULLABLE | Resolution timestamp |
| `resolution_notes` | Text | NULLABLE | Resolution details |

**Request Types**:
- `new_connection`: New electricity connection
- `upgrade`: Increase load capacity
- `downgrade`: Decrease load capacity
- `relocation`: Move connection
- `name_change`: Update account holder
- `disconnection`: Terminate service
- `reconnection`: Restore service

**Status Workflow**:
```
submitted → under_review → approved → in_progress → completed
                              └──→ rejected
```

#### 4.2.9 Notification Model (`notifications` table)

**Purpose**: System notifications for users and customers.

**File Location**: `app/models/__init__.py` (Lines 252-268)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `notification_id` | Integer | PRIMARY KEY | Unique notification identifier |
| `user_id` | Integer | FOREIGN KEY | Target staff user (optional) |
| `customer_id` | Integer | FOREIGN KEY | Target customer (optional) |
| `title` | String(100) | NOT NULL | Notification title |
| `message` | Text | NOT NULL | Notification content |
| `notification_type` | Enum | NOT NULL | 'fault_update', 'maintenance_reminder', 'service_update', 'system', 'alert' |
| `reference_type` | String(50) | NULLABLE | Related entity type |
| `reference_id` | Integer | NULLABLE | Related entity ID |
| `is_read` | Boolean | DEFAULT FALSE | Read status |
| `created_at` | DateTime | DEFAULT NOW | Creation timestamp |

#### 4.2.10 CustomerMessage Model (`customer_messages` table)

**Purpose**: Two-way messaging between customers and support staff.

**File Location**: `app/models/__init__.py` (Lines 271-290)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `message_id` | Integer | PRIMARY KEY | Unique message identifier |
| `customer_id` | Integer | FOREIGN KEY, NOT NULL | Customer in conversation |
| `user_id` | Integer | FOREIGN KEY | Staff member (for replies) |
| `subject` | String(200) | NOT NULL | Message subject |
| `message` | Text | NOT NULL | Message content |
| `is_from_customer` | Boolean | DEFAULT TRUE | Direction indicator |
| `is_read` | Boolean | DEFAULT FALSE | Read status |
| `parent_message_id` | Integer | FOREIGN KEY (self) | Thread parent reference |
| `created_at` | DateTime | DEFAULT NOW | Message timestamp |

**Relationships**:
- `replies`: Self-referential One-to-Many for message threads

---

## 6. Backend Implementation

### 5.1 Application Factory (`app/__init__.py`)

**Purpose**: Creates and configures the Flask application instance.

**File Location**: `app/__init__.py` (67 lines)

**Key Components**:

```python
# Extension Initialization
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register all blueprints
    # ... blueprint registrations

    return app
```

**Custom Jinja2 Filter**:
```python
@app.template_filter('datetime')
def datetime_filter(value, format='%B %d, %Y %H:%M'):
    """Format datetime objects for display"""
    if value == 'now' or value is None:
        return datetime.now().strftime(format)
    if isinstance(value, datetime):
        return value.strftime(format)
    return value
```

### 5.2 Route Modules

#### 5.2.1 Main Routes (`app/routes/main.py`)

**Purpose**: Handles landing page and staff dashboard.

**Endpoints**:

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/` | GET | `index()` | Public landing page |
| `/dashboard` | GET | `dashboard()` | Staff dashboard with statistics |

**Dashboard Statistics Calculation**:
```python
stats = {
    'total_customers': Customer.query.filter_by(is_active=True).count(),
    'active_connections': Connection.query.filter_by(connection_status='active').count(),
    'pending_faults': Fault.query.filter(
        Fault.status.in_(['reported', 'acknowledged', 'assigned', 'in_progress'])
    ).count(),
    'scheduled_maintenance': MaintenanceSchedule.query.filter_by(status='scheduled').count(),
    'pending_requests': ServiceRequest.query.filter(
        ServiceRequest.status.in_(['submitted', 'under_review'])
    ).count()
}
```

#### 5.2.2 Authentication Routes (`app/routes/auth.py`)

**Purpose**: Staff user authentication management.

**Endpoints**:

| Route | Method | Function | Access | Description |
|-------|--------|----------|--------|-------------|
| `/login` | GET, POST | `login()` | Public | Staff login form and processing |
| `/logout` | GET | `logout()` | Authenticated | End user session |
| `/register` | GET, POST | `register()` | Public | Staff registration |

**Login Flow**:
1. Check if user already authenticated → redirect to dashboard
2. Validate username/password against database
3. Check account active status
4. Create session using Flask-Login
5. Handle "remember me" functionality
6. Redirect to requested page or dashboard

**Security Features**:
- Account deactivation check
- Flash message feedback
- Session management via Flask-Login

#### 5.2.3 Customer Management Routes (`app/routes/customers.py`)

**Purpose**: CRUD operations for customer accounts.

**Endpoints**:

| Route | Method | Function | Roles | Description |
|-------|--------|----------|-------|-------------|
| `/customers/` | GET | `list_customers()` | All staff | Paginated customer list |
| `/customers/add` | GET, POST | `add_customer()` | Admin, Manager, CS | Add new customer |
| `/customers/<id>` | GET | `view_customer()` | All staff | View customer details |
| `/customers/<id>/edit` | GET, POST | `edit_customer()` | Admin, Manager, CS | Edit customer |

**Account Number Generation**:
```python
last_customer = Customer.query.order_by(Customer.customer_id.desc()).first()
new_id = (last_customer.customer_id + 1) if last_customer else 1
account_number = f"KP-{datetime.now().year}-{new_id:04d}"
# Example: KP-2026-0001
```

#### 5.2.4 Connection Management Routes (`app/routes/connections.py`)

**Purpose**: Electrical connection/meter management.

**Endpoints**:

| Route | Method | Function | Roles | Description |
|-------|--------|----------|-------|-------------|
| `/connections/` | GET | `list_connections()` | All staff | List connections with filters |
| `/connections/add` | GET, POST | `add_connection()` | Admin, Manager, Tech | Add new connection |
| `/connections/<id>` | GET | `view_connection()` | All staff | View connection details |
| `/connections/<id>/status` | POST | `update_status()` | Admin, Manager, Tech | Update connection status |

**Meter Number Generation**:
```python
last_conn = Connection.query.order_by(Connection.connection_id.desc()).first()
new_id = (last_conn.connection_id + 1) if last_conn else 1
county_code = request.form.get('county_code', 'NAI')
meter_number = f"MTR-{county_code}-{new_id:06d}"
# Example: MTR-NAI-000001
```

#### 5.2.5 Fault Management Routes (`app/routes/faults.py`)

**Purpose**: Complete fault lifecycle management.

**Endpoints**:

| Route | Method | Function | Roles | Description |
|-------|--------|----------|-------|-------------|
| `/faults/` | GET | `list_faults()` | All staff | List faults with filters |
| `/faults/report` | GET, POST | `report_fault()` | All staff | Report new fault |
| `/faults/<id>` | GET | `view_fault()` | All staff | View fault details |
| `/faults/<id>/assign` | POST | `assign_fault()` | Admin, Manager | Assign to technician |
| `/faults/<id>/update-status` | POST | `update_fault_status()` | All staff | Update fault status |
| `/faults/<id>/add-note` | POST | `add_fault_note()` | All staff | Add progress note |

**Role-Based Fault Visibility**:
```python
# Technicians only see assigned faults or newly reported faults
if current_user.role == 'technician':
    query = query.filter(
        (Fault.assigned_to == current_user.user_id) |
        (Fault.status == 'reported')
    )
```

**Automatic Notifications**:
- On fault report: Notify all managers
- On fault assignment: Notify assigned technician

#### 5.2.6 Maintenance Routes (`app/routes/maintenance.py`)

**Purpose**: Maintenance scheduling and tracking.

**Endpoints**:

| Route | Method | Function | Roles | Description |
|-------|--------|----------|-------|-------------|
| `/maintenance/` | GET | `list_maintenance()` | All staff | List schedules |
| `/maintenance/calendar` | GET | `calendar()` | All staff | Calendar view |
| `/maintenance/api/events` | GET | `get_events()` | All staff | Calendar data API |
| `/maintenance/schedule` | GET, POST | `schedule_maintenance()` | Admin, Manager | Schedule new |
| `/maintenance/<id>` | GET | `view_maintenance()` | All staff | View details |
| `/maintenance/<id>/update-status` | POST | `update_maintenance_status()` | All staff | Update status |
| `/maintenance/<id>/log` | POST | `add_maintenance_log()` | Admin, Manager, Tech | Add work log |

**Calendar Event Colors**:
```python
colors = {
    'scheduled': '#3788d8',    # Blue
    'in_progress': '#f39c12',  # Orange
    'completed': '#27ae60',    # Green
    'cancelled': '#e74c3c',    # Red
    'postponed': '#9b59b6'     # Purple
}
```

#### 5.2.7 Reports Routes (`app/routes/reports.py`)

**Purpose**: Performance analytics and reporting.

**Endpoints**:

| Route | Method | Function | Roles | Description |
|-------|--------|----------|-------|-------------|
| `/reports/` | GET | `index()` | Admin, Manager | Reports dashboard |
| `/reports/faults` | GET | `fault_reports()` | Admin, Manager | Fault statistics |
| `/reports/maintenance` | GET | `maintenance_reports()` | Admin, Manager | Maintenance stats |
| `/reports/performance` | GET | `performance_dashboard()` | Admin, Manager | KPI dashboard |
| `/reports/api/chart-data/<type>` | GET | `get_chart_data()` | Admin, Manager | Chart data API |

**Fault Report Calculations**:
```python
# Average resolution time
resolution_times = [f.resolution_time_hours for f in faults if f.resolution_time_hours]
avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0

# Resolution rate
resolution_rate = (resolved_faults / total_faults) * 100
```

#### 5.2.8 Staff Management Routes (`app/routes/staff.py`)

**Purpose**: Admin-only staff user management.

**Endpoints**:

| Route | Method | Function | Roles | Description |
|-------|--------|----------|-------|-------------|
| `/staff/` | GET | `list_staff()` | Admin | List staff members |
| `/staff/add` | GET, POST | `add_staff()` | Admin | Add new staff |
| `/staff/<id>` | GET | `view_staff()` | Admin | View staff details |
| `/staff/<id>/edit` | GET, POST | `edit_staff()` | Admin | Edit staff member |
| `/staff/<id>/toggle-status` | POST | `toggle_status()` | Admin | Activate/deactivate |

**Staff Creation Validation**:
- Username uniqueness check
- Email uniqueness check
- Password minimum length (6 characters)
- Role validation (customer_service or technician only)

#### 5.2.9 Customer Portal Routes (`app/routes/customer.py`)

**Purpose**: Self-service portal for customers.

**Authentication Endpoints**:

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/portal/login` | GET, POST | `login()` | Customer login |
| `/portal/register` | GET, POST | `register()` | Portal registration |
| `/portal/logout` | GET | `logout()` | Customer logout |

**Dashboard & Profile Endpoints**:

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/portal/dashboard` | GET | `dashboard()` | Customer overview |
| `/portal/profile` | GET | `profile()` | View profile |
| `/portal/profile/update` | POST | `update_profile()` | Update email/phone |
| `/portal/profile/change-password` | POST | `change_password()` | Change password |

**Connection Endpoints**:

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/portal/connections` | GET | `my_connections()` | List connections |
| `/portal/connections/<id>` | GET | `view_connection()` | View connection |

**Fault Endpoints**:

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/portal/faults` | GET | `my_faults()` | List reported faults |
| `/portal/faults/report` | GET, POST | `report_fault()` | Report new fault |
| `/portal/faults/<id>` | GET | `view_fault()` | View fault details |

**Service Request Endpoints**:

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/portal/requests` | GET | `my_requests()` | List requests |
| `/portal/requests/new` | GET, POST | `new_request()` | Submit request |
| `/portal/requests/<id>` | GET | `view_request()` | View request |

**Support Messaging Endpoints**:

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/portal/support` | GET | `support()` | Message inbox |
| `/portal/support/new` | GET, POST | `new_message()` | Send message |
| `/portal/support/<id>` | GET | `view_message()` | View thread |
| `/portal/support/<id>/reply` | POST | `reply_message()` | Reply to thread |

**Notification Endpoint**:

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/portal/notifications` | GET | `notifications()` | View notifications |

**Customer Registration Flow**:
1. Customer enters account number, ID number, phone
2. System verifies against existing customer record
3. Customer sets portal password
4. Account marked as `portal_registered = True`

### 5.3 Utility Modules

#### 5.3.1 Role-Based Access Control (`app/utils/decorators.py`)

**Purpose**: Decorator for restricting route access by user role.

```python
def role_required(*roles):
    """
    Decorator to restrict access based on user roles

    Usage:
        @role_required('admin', 'manager')
        def admin_only_view():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))

            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

#### 5.3.2 Customer Authentication (`app/utils/customer_auth.py`)

**Purpose**: Session-based authentication for customer portal (separate from Flask-Login).

**Functions**:

```python
def login_customer(customer):
    """Store customer ID in session and update last_login"""
    session['customer_id'] = customer.customer_id
    session['customer_logged_in'] = True
    customer.last_login = datetime.utcnow()

def logout_customer():
    """Clear customer session data"""
    session.pop('customer_id', None)
    session.pop('customer_logged_in', None)

def get_current_customer():
    """Retrieve currently logged in customer from session"""
    if session.get('customer_logged_in') and session.get('customer_id'):
        return Customer.query.get(session['customer_id'])
    return None

def customer_login_required(f):
    """Decorator to require customer login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        customer = get_current_customer()
        if not customer:
            flash('Please log in to access the customer portal.', 'info')
            return redirect(url_for('customer.login'))
        g.customer = customer  # Make available in request context
        return f(*args, **kwargs)
    return decorated_function
```

---

## 7. Frontend Implementation

### 6.1 Template Architecture

The application uses Jinja2 templating with template inheritance:

```
base.html (Staff Portal Layout)
├── dashboard.html
├── auth/
│   ├── login.html
│   └── register.html
├── customers/
│   ├── list.html
│   ├── add.html
│   ├── view.html
│   └── edit.html
├── connections/
│   ├── list.html
│   ├── add.html
│   └── view.html
├── faults/
│   ├── list.html
│   ├── report.html
│   └── view.html
├── maintenance/
│   ├── list.html
│   ├── schedule.html
│   ├── calendar.html
│   └── view.html
├── reports/
│   ├── index.html
│   ├── faults.html
│   ├── maintenance.html
│   └── performance.html
└── staff/
    ├── list.html
    ├── add.html
    ├── view.html
    └── edit.html

customer/base.html (Customer Portal Layout)
├── login.html
├── register.html
├── dashboard.html
├── my_connections.html
├── view_connection.html
├── my_faults.html
├── report_fault.html
├── view_fault.html
├── my_requests.html
├── new_request.html
├── view_request.html
├── support.html
├── new_message.html
├── view_message.html
├── notifications.html
└── profile.html
```

### 6.2 Base Template Structure (`app/templates/base.html`)

**Staff Portal Layout Components**:

1. **Sidebar Navigation** (Lines 19-68):
   - Logo and system name
   - Dashboard link
   - Customers section (Customers, Connections)
   - Operations section (Faults, Maintenance, Calendar)
   - Reports section (Admin/Manager only)
   - Administration section (Admin only)
   - User info footer

2. **Top Navbar** (Lines 73-92):
   - Sidebar toggle button
   - User dropdown menu (Settings, Logout)

3. **Flash Messages** (Lines 95-105):
   - Bootstrap alerts with auto-dismiss
   - Category-based styling

4. **Content Block**:
   ```html
   {% block content %}{% endblock %}
   ```

### 6.3 CSS Styling (`app/static/css/style.css`)

**Staff Portal Styles** (238 lines):

1. **CSS Variables**:
```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --success-color: #198754;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #0dcaf0;
    --sidebar-bg: #212529;
    --sidebar-width: 250px;
}
```

2. **Sidebar Styling**:
   - Fixed position, full height
   - Dark background (#212529)
   - Collapsible with smooth transition
   - Navigation links with hover effects

3. **Dashboard Cards**:
   - Rounded corners (10px)
   - Subtle shadows
   - Hover lift effect

4. **Status Badge Colors**:
   - Unique colors for each status state
   - Consistent visual language

5. **Responsive Design**:
   - Mobile breakpoint at 768px
   - Sidebar hidden by default on mobile

### 6.4 Customer Portal CSS (`app/static/css/customer-portal.css`)

**Customer Portal Specific Styles**:

1. **Color Scheme**:
   - Primary: Green (#198754) - Kenya Power brand color
   - Light accent: #90EE90
   - Dark sidebar: #1a472a

2. **Portal Sidebar**:
   - 260px width
   - Gradient background
   - Green accent colors

### 6.5 JavaScript Functionality (`app/static/js/main.js`)

**Core Functions** (58 lines):

1. **Sidebar Toggle**:
```javascript
sidebarToggle.addEventListener('click', function() {
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('expanded');
});
```

2. **Alert Auto-Dismiss**:
```javascript
setTimeout(function() {
    const bsAlert = new bootstrap.Alert(alert);
    bsAlert.close();
}, 5000);
```

3. **Confirm Delete**:
```javascript
if (!confirm(this.dataset.confirm || 'Are you sure?')) {
    e.preventDefault();
}
```

4. **Tooltip Initialization**:
```javascript
const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});
```

5. **Date Formatting Utilities**:
```javascript
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-KE', options);
}
```

---

## 8. Authentication and Authorization

### 7.1 Dual Authentication System

The application implements two separate authentication systems:

#### Staff Authentication (Flask-Login)
- **Library**: Flask-Login
- **Storage**: Server-side session
- **User Model**: `User` (extends `UserMixin`)
- **Login Manager**: Configured in `app/__init__.py`

#### Customer Authentication (Custom Session)
- **Library**: Custom implementation
- **Storage**: Flask session
- **User Model**: `Customer`
- **Utilities**: `app/utils/customer_auth.py`

### 7.2 Role-Based Access Control (RBAC)

**Staff Roles and Permissions**:

| Role | Customers | Connections | Faults | Maintenance | Reports | Staff |
|------|-----------|-------------|--------|-------------|---------|-------|
| Admin | Full | Full | Full | Full | View | Full |
| Manager | Full | Full | Full | Full | View | None |
| Technician | View | Add/Edit | Assigned | Assigned | None | None |
| Customer Service | Full | View | Report | View | None | None |

### 7.3 Password Security

**Current Implementation** (Demo Mode):
```python
def set_password(self, password):
    """Store password (plain text for demo)"""
    self.password = password

def check_password(self, password):
    """Check password (plain text comparison)"""
    return self.password == password
```

**Production Recommendation**:
```python
from werkzeug.security import generate_password_hash, check_password_hash

def set_password(self, password):
    self.password = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password, password)
```

---

## 9. Feature Documentation

### 8.1 Customer Management

**Workflow**:
1. Staff creates customer account with personal details
2. System generates unique account number (KP-YYYY-NNNN)
3. Customer can optionally register for self-service portal
4. Staff can view, edit, and manage customer accounts

**Key Features**:
- Search by account number, name, or phone
- Filter by customer type (residential/commercial/industrial)
- View associated connections and service requests
- Pagination (10 records per page)

### 8.2 Connection Management

**Workflow**:
1. Staff creates connection linked to customer
2. System generates unique meter number (MTR-XXX-NNNNNN)
3. Connection status managed through lifecycle
4. Faults and service requests linked to connections

**Connection Status Lifecycle**:
```
pending → active → suspended ↔ active → disconnected
```

### 8.3 Fault Management

**Reporting Sources**:
- Staff portal (any authenticated staff)
- Customer portal (registered customers)

**Fault Lifecycle**:
```
reported → acknowledged → assigned → in_progress → resolved → closed
```

**Automatic Actions**:
- Notification to managers on new fault
- Notification to technician on assignment
- Notification to customer on status updates
- Resolution time calculation

### 8.4 Maintenance Scheduling

**Maintenance Types**:
- **Preventive**: Scheduled regular maintenance
- **Corrective**: Repair after failure
- **Emergency**: Urgent unplanned work
- **Inspection**: Routine checks

**Calendar Integration**:
- Color-coded events by status
- Click-to-view details
- Date range navigation

### 8.5 Performance Reporting

**Available Reports**:

1. **Fault Reports**:
   - Total faults in period
   - Resolution rate
   - Average resolution time
   - Faults by type (pie chart)
   - Faults by severity
   - Daily trend (line chart)

2. **Maintenance Reports**:
   - Total scheduled
   - Completion rate
   - By type breakdown
   - By equipment breakdown

3. **Performance Dashboard**:
   - Total customers
   - Active connections
   - Monthly fault statistics
   - Resolution rate KPI
   - Pending requests

### 8.6 Customer Self-Service Portal

**Available Functions**:
- View electrical connections
- Report faults
- Track fault resolution progress
- Submit service requests
- Track request status
- Message customer support
- View notifications
- Update contact information
- Change password

---

## 10. API Endpoints Reference

### 9.1 JSON API Endpoints

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/maintenance/api/events` | GET | Calendar events | JSON array of events |
| `/reports/api/chart-data/faults_trend` | GET | Fault trend data | `{labels: [], values: []}` |
| `/reports/api/chart-data/faults_by_type` | GET | Fault type distribution | `{labels: [], values: []}` |

### 9.2 Calendar Events API

**Request**: `GET /maintenance/api/events?start=YYYY-MM-DD&end=YYYY-MM-DD`

**Response**:
```json
[
    {
        "id": 1,
        "title": "Transformer Maintenance",
        "start": "2026-01-25",
        "backgroundColor": "#3788d8",
        "url": "/maintenance/1"
    }
]
```

---

## 11. Configuration and Deployment

### 10.1 Configuration File (`config.py`)

```python
class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kenya-power-secret-key-2024'

    # Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '0123'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'kenya_power_db'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 10

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

### 10.2 Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `SECRET_KEY` | Flask session encryption | 'kenya-power-secret-key-2024' |
| `MYSQL_HOST` | Database host | 'localhost' |
| `MYSQL_USER` | Database username | 'root' |
| `MYSQL_PASSWORD` | Database password | '0123' |
| `MYSQL_DB` | Database name | 'kenya_power_db' |

### 10.3 Database Initialization

Run `init_db.py` to:
1. Create all database tables
2. Create admin user
3. Create sample staff accounts

```bash
python init_db.py
```

### 10.4 Running the Application

**Development**:
```bash
python run.py
# or
python main.py
```

**Server URL**: http://127.0.0.1:5000

### 10.5 Dependencies (`requirements.txt`)

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
mysql-connector-python==8.2.0
PyMySQL==1.1.0
Werkzeug==3.0.1
python-dotenv==1.0.0
email-validator==2.1.0
```

---

## 12. User Guide

This section provides clear instructions for using the Kenya Power Management System, including descriptions of key workflows.

### 12.1 Getting Started

#### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Network access to the server (default: http://127.0.0.1:5000)

#### Accessing the System
1. Open your web browser
2. Navigate to `http://127.0.0.1:5000/`
3. You will see the landing page with two portal options:
   - **Staff Login**: For Kenya Power employees
   - **Customer Portal**: For registered customers

### 12.2 Staff Portal User Guide

#### 12.2.1 Logging In
1. Click "Staff Login" on the landing page or navigate to `/login`
2. Enter your username and password
3. Optionally check "Remember me" for persistent sessions
4. Click "Login"
5. Upon successful login, you'll be redirected to the Dashboard

#### 12.2.2 Dashboard Overview
The dashboard displays:
- **Statistics Cards**: Total customers, active connections, pending faults, scheduled maintenance
- **Recent Faults**: Latest 5 fault reports with quick links
- **Upcoming Maintenance**: Next 5 scheduled maintenance tasks
- **Quick Actions**: Buttons for common tasks

#### 12.2.3 Customer Management Workflow
**Adding a New Customer:**
1. Navigate to Customers in the sidebar
2. Click "Add Customer" button
3. Fill in personal information (name, ID number, phone, email)
4. Enter address details (street, county, town, postal code)
5. Select customer type (Residential/Commercial/Industrial)
6. Click "Add Customer"
7. System generates unique account number (format: KP-2026-0001)

**Viewing Customer Details:**
1. Navigate to Customers
2. Use search to find customer by account number, name, or phone
3. Click on account number to view full profile
4. View associated connections and service requests

#### 12.2.4 Connection Management Workflow
**Adding a New Connection:**
1. Navigate to Connections in the sidebar
2. Click "Add Connection"
3. Select the customer from dropdown
4. Enter connection type (Single Phase/Three Phase)
5. Specify load capacity in kVA
6. Enter transformer ID and feeder line information
7. Set installation date and initial status
8. Click "Create Connection"
9. System generates unique meter number (format: MTR-NAI-000001)

**Updating Connection Status:**
1. Open connection details page
2. Use the status update dropdown
3. Select new status (Active/Suspended/Disconnected)
4. Confirm the change

#### 12.2.5 Fault Management Workflow
**Reporting a Fault (Staff):**
1. Navigate to Faults > Report Fault
2. Optionally select affected connection
3. Choose fault type from dropdown
4. Enter detailed description
5. Specify location description
6. Set severity level (Low/Medium/High/Critical)
7. Enter number of affected customers
8. Click "Report Fault"
9. System creates notifications for managers

**Assigning a Fault (Manager/Admin):**
1. Open fault details page
2. In the Assignment section, select a technician
3. Click "Assign"
4. System notifies the assigned technician

**Resolving a Fault (Technician):**
1. View your assigned faults
2. Open the fault to work on
3. Update status to "In Progress"
4. Add progress notes as needed
5. When complete, update status to "Resolved"
6. Enter resolution notes describing the fix
7. System records resolution time automatically

#### 12.2.6 Maintenance Scheduling Workflow
**Scheduling Maintenance:**
1. Navigate to Maintenance > Schedule Maintenance
2. Enter maintenance title and description
3. Select type (Preventive/Corrective/Emergency/Inspection)
4. Choose equipment type and ID
5. Enter location details
6. Set scheduled date and time
7. Assign to technician (optional)
8. Set priority level
9. Click "Schedule Maintenance"

**Using the Calendar View:**
1. Navigate to Maintenance > Calendar
2. View color-coded events:
   - Blue: Scheduled
   - Orange: In Progress
   - Green: Completed
   - Red: Cancelled
   - Purple: Postponed
3. Click on any event to view details

**Recording Maintenance Work:**
1. Open maintenance details
2. Click "Add Log Entry"
3. Record work performed
4. List parts used
5. Document issues found
6. Add recommendations
7. Enter actual duration
8. Submit the log

#### 12.2.7 Reports and Analytics
**Viewing Fault Reports:**
1. Navigate to Reports > Fault Reports
2. Set date range using the filter
3. Click "Generate Report"
4. Review summary statistics
5. Analyze charts:
   - Faults by Type (doughnut)
   - Faults by Severity (bar)
   - Daily Trend (line)

**Performance Dashboard:**
1. Navigate to Reports > Performance Dashboard
2. View real-time KPIs
3. Monitor resolution rate
4. Track monthly statistics

#### 12.2.8 Staff Management (Admin Only)
**Adding New Staff:**
1. Navigate to Administration > Staff Management
2. Click "Add Staff Member"
3. Enter username (for login)
4. Enter email address
5. Set initial password
6. Enter full name and phone
7. Select role (Customer Care Agent/Technician)
8. Click "Create Staff Account"

### 12.3 Customer Portal User Guide

#### 12.3.1 Registering for the Portal
1. Navigate to `/portal/register`
2. Enter your Kenya Power account number
3. Enter your ID number (for verification)
4. Enter your registered phone number
5. Create a password (minimum 6 characters)
6. Confirm password
7. Click "Register"
8. Upon verification, your portal account is created

#### 12.3.2 Customer Dashboard
After login, view:
- Active connections count
- Pending faults count
- Pending requests count
- Unread notifications
- Recent faults list
- Recent service requests

#### 12.3.3 Viewing Your Connections
1. Click "My Connections" in sidebar
2. View all your electrical connections
3. See meter number, type, and status
4. Click on a connection for details

#### 12.3.4 Reporting a Fault
1. Navigate to Faults > Report Fault
2. Select affected connection (if applicable)
3. Choose fault type
4. Describe the issue in detail
5. Provide location details
6. Select severity
7. Submit the report
8. Track progress in "My Faults"

#### 12.3.5 Submitting Service Requests
1. Navigate to Requests > New Request
2. Select request type:
   - New Connection
   - Upgrade/Downgrade
   - Relocation
   - Name Change
   - Disconnection/Reconnection
3. Select related connection if applicable
4. Describe your request
5. Set priority
6. Submit request
7. Track in "My Requests"

#### 12.3.6 Contacting Customer Support
1. Navigate to Support
2. Click "New Message"
3. Enter subject
4. Write your message
5. Send
6. View replies in your inbox
7. Reply to continue the conversation

### 12.4 URL Quick Reference

| Function | Staff Portal URL | Customer Portal URL |
|----------|-----------------|---------------------|
| Login | /login | /portal/login |
| Dashboard | /dashboard | /portal/dashboard |
| Customers | /customers/ | - |
| Connections | /connections/ | /portal/connections |
| Faults | /faults/ | /portal/faults |
| Report Fault | /faults/report | /portal/faults/report |
| Maintenance | /maintenance/ | - |
| Calendar | /maintenance/calendar | - |
| Reports | /reports/ | - |
| Staff Mgmt | /staff/ | - |
| Service Requests | - | /portal/requests |
| Support | - | /portal/support |
| Profile | - | /portal/profile |

---

## 13. Testing and Validation

This section documents the testing procedures, results, and validation of system functionality.

### 13.1 Testing Methodology

The system was tested using the following approaches:

1. **Unit Testing**: Individual model methods and utility functions
2. **Integration Testing**: Route handlers with database operations
3. **Functional Testing**: End-to-end user workflows
4. **User Acceptance Testing**: Role-based feature verification

### 13.2 Test Cases and Results

#### 13.2.1 Authentication Module Tests

| Test Case | Description | Expected Result | Actual Result | Status |
|-----------|-------------|-----------------|---------------|--------|
| AUTH-01 | Staff login with valid credentials | Redirect to dashboard | Redirect to dashboard | PASS |
| AUTH-02 | Staff login with invalid password | Error message displayed | Error message displayed | PASS |
| AUTH-03 | Staff login with inactive account | Account deactivated message | Account deactivated message | PASS |
| AUTH-04 | Customer portal registration | Account created successfully | Account created successfully | PASS |
| AUTH-05 | Customer login after registration | Redirect to customer dashboard | Redirect to customer dashboard | PASS |
| AUTH-06 | Logout functionality | Session cleared, redirect to login | Session cleared, redirect to login | PASS |

#### 13.2.2 Customer Management Tests

| Test Case | Description | Expected Result | Actual Result | Status |
|-----------|-------------|-----------------|---------------|--------|
| CUST-01 | Create new customer | Account number generated (KP-YYYY-NNNN) | KP-2026-0001 generated | PASS |
| CUST-02 | Search customer by account | Customer found and displayed | Customer found and displayed | PASS |
| CUST-03 | Edit customer details | Changes saved successfully | Changes saved successfully | PASS |
| CUST-04 | View customer connections | Related connections displayed | Related connections displayed | PASS |
| CUST-05 | Pagination on customer list | 10 records per page | 10 records per page | PASS |

#### 13.2.3 Connection Management Tests

| Test Case | Description | Expected Result | Actual Result | Status |
|-----------|-------------|-----------------|---------------|--------|
| CONN-01 | Create new connection | Meter number generated | MTR-NAI-000001 generated | PASS |
| CONN-02 | Link connection to customer | Foreign key relationship | Relationship established | PASS |
| CONN-03 | Update connection status | Status changed and saved | Status changed and saved | PASS |
| CONN-04 | View connection faults | Related faults displayed | Related faults displayed | PASS |

#### 13.2.4 Fault Management Tests

| Test Case | Description | Expected Result | Actual Result | Status |
|-----------|-------------|-----------------|---------------|--------|
| FAULT-01 | Report fault from staff portal | Fault created, managers notified | Fault created, notifications sent | PASS |
| FAULT-02 | Report fault from customer portal | Fault created, customer notified | Fault created, notification sent | PASS |
| FAULT-03 | Assign fault to technician | Assignment saved, technician notified | Assignment saved, notification sent | PASS |
| FAULT-04 | Update fault status | Status changed, update logged | Status changed, FaultUpdate created | PASS |
| FAULT-05 | Resolve fault | Resolution time calculated | Resolution time displayed | PASS |
| FAULT-06 | Technician sees only assigned | Filtered fault list | Only assigned faults shown | PASS |

#### 13.2.5 Maintenance Module Tests

| Test Case | Description | Expected Result | Actual Result | Status |
|-----------|-------------|-----------------|---------------|--------|
| MAINT-01 | Schedule maintenance | Schedule created successfully | Schedule created successfully | PASS |
| MAINT-02 | View calendar | Events displayed with colors | Color-coded events shown | PASS |
| MAINT-03 | Add maintenance log | Log entry saved | Log entry saved | PASS |
| MAINT-04 | Complete maintenance | Completion date recorded | Completion date and notes saved | PASS |
| MAINT-05 | Technician assignment notification | Notification created | Notification created | PASS |

#### 13.2.6 Reporting Module Tests

| Test Case | Description | Expected Result | Actual Result | Status |
|-----------|-------------|-----------------|---------------|--------|
| RPT-01 | Fault report generation | Statistics calculated correctly | Correct statistics displayed | PASS |
| RPT-02 | Date range filtering | Filtered results returned | Filtered results correct | PASS |
| RPT-03 | Chart rendering | Charts display with data | All 3 charts rendered | PASS |
| RPT-04 | Performance KPIs | Metrics calculated | All KPIs displayed | PASS |
| RPT-05 | Resolution rate calculation | Percentage calculated | Correct percentage shown | PASS |

#### 13.2.7 Role-Based Access Control Tests

| Test Case | Description | Expected Result | Actual Result | Status |
|-----------|-------------|-----------------|---------------|--------|
| RBAC-01 | Admin accesses staff management | Access granted | Access granted | PASS |
| RBAC-02 | Manager accesses staff management | Access denied | Redirected with error | PASS |
| RBAC-03 | Technician accesses reports | Access denied | Redirected with error | PASS |
| RBAC-04 | Customer service accesses reports | Access denied | Redirected with error | PASS |
| RBAC-05 | Admin sidebar shows all sections | All sections visible | All sections visible | PASS |

### 13.3 Performance Testing Results

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Page Load Time (Dashboard) | < 2 seconds | ~1.2 seconds | PASS |
| Database Query Time | < 500ms | ~200ms | PASS |
| Concurrent Users Supported | 50+ | 100+ (development server) | PASS |
| Form Submission Response | < 1 second | ~500ms | PASS |

### 13.4 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Google Chrome | 120+ | Compatible |
| Mozilla Firefox | 120+ | Compatible |
| Microsoft Edge | 120+ | Compatible |
| Safari | 17+ | Compatible |

### 13.5 Challenges Encountered and Solutions

| Challenge | Description | Solution Implemented |
|-----------|-------------|---------------------|
| Dual Authentication | Staff and customers needed separate auth | Implemented Flask-Login for staff, custom session-based auth for customers |
| Role-Based Filtering | Technicians needed filtered views | Added role checks in queries (`current_user.role == 'technician'`) |
| Notification System | Real-time updates needed | Implemented database-backed notifications with read status |
| Calendar Integration | Visual maintenance scheduling | Integrated FullCalendar.js with JSON API endpoint |
| Report Date Filtering | Dynamic date ranges | Implemented query parameter filtering with SQLAlchemy |

### 13.6 Known Limitations

1. **Password Storage**: Currently using plain text for demonstration purposes. Production deployment should use password hashing (bcrypt/werkzeug).

2. **Real-time Notifications**: Notifications require page refresh. WebSocket implementation would enable true real-time updates.

3. **File Uploads**: System does not currently support file attachments for faults or messages.

4. **Email Notifications**: External email sending is not implemented. Integration with SMTP would be required.

### 13.7 Validation Summary

| Category | Tests | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
| Authentication | 6 | 6 | 0 | 100% |
| Customer Management | 5 | 5 | 0 | 100% |
| Connection Management | 4 | 4 | 0 | 100% |
| Fault Management | 6 | 6 | 0 | 100% |
| Maintenance Module | 5 | 5 | 0 | 100% |
| Reporting Module | 5 | 5 | 0 | 100% |
| Role-Based Access | 5 | 5 | 0 | 100% |
| **TOTAL** | **36** | **36** | **0** | **100%** |

---

## 14. Default Credentials

### 14.1 Staff Accounts

| Username | Password | Role | Full Name | Email |
|----------|----------|------|-----------|-------|
| admin | admin123 | Administrator | System Administrator | admin@kenyapower.co.ke |
| manager1 | password123 | Manager | James Mwangi | manager@kenyapower.co.ke |
| tech1 | password123 | Technician | Peter Ochieng | technician1@kenyapower.co.ke |
| tech2 | password123 | Technician | Mary Wanjiku | technician2@kenyapower.co.ke |
| cs_agent1 | password123 | Customer Service | Sarah Kimani | csagent1@kenyapower.co.ke |

### 14.2 Role Permissions Summary

| Permission | Admin | Manager | Technician | Customer Service |
|------------|-------|---------|------------|------------------|
| View Dashboard | Yes | Yes | Yes | Yes |
| Manage Customers | Full | Full | View | Full |
| Create Connections | Yes | Yes | No | No |
| View Connections | Yes | Yes | Yes | Yes |
| Update Connection Status | Yes | Yes | No | No |
| Report Faults | Yes | Yes | Yes | Yes |
| Assign Faults | Yes | Yes | No | No |
| Resolve Faults | Yes | Yes | Assigned Only | No |
| Schedule Maintenance | Yes | Yes | No | No |
| Complete Maintenance | Yes | Yes | Assigned Only | No |
| View Reports | Yes | Yes | No | No |
| Manage Staff | Yes | No | No | No |

**Note:** Customers can request new connections through the Customer Portal's Service Request feature (`/portal/requests/new` with request type "New Connection"). These requests are then reviewed and processed by managers/administrators who create the actual connection records.

### 14.3 Quick Start Guide

1. **Initialize Database**:
   ```bash
   python init_db.py
   ```

2. **Start Application**:
   ```bash
   python run.py
   ```

3. **Access Application**:
   - Open browser to `http://127.0.0.1:5000/`

4. **Login as Admin**:
   - Username: `admin`
   - Password: `admin123`

5. **Create Test Data**:
   - Add a customer
   - Create a connection
   - Report a fault
   - Schedule maintenance

---

## Appendix A: Database Schema SQL

```sql
-- Users table (Staff accounts)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role ENUM('admin', 'manager', 'technician', 'customer_service') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Customers table
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20) NOT NULL,
    id_number VARCHAR(20) UNIQUE NOT NULL,
    address TEXT NOT NULL,
    county VARCHAR(50) NOT NULL,
    town VARCHAR(50) NOT NULL,
    postal_code VARCHAR(10),
    customer_type ENUM('residential', 'commercial', 'industrial') NOT NULL,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    password VARCHAR(255),
    portal_registered BOOLEAN DEFAULT FALSE,
    last_login DATETIME
);

-- Connections table
CREATE TABLE connections (
    connection_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    meter_number VARCHAR(20) UNIQUE NOT NULL,
    connection_type ENUM('single_phase', 'three_phase') NOT NULL,
    load_capacity DECIMAL(10, 2) NOT NULL,
    installation_date DATE,
    connection_status ENUM('pending', 'active', 'suspended', 'disconnected') DEFAULT 'pending',
    location_coordinates VARCHAR(50),
    transformer_id VARCHAR(20),
    feeder_line VARCHAR(50),
    last_reading_date DATE,
    last_reading_value DECIMAL(12, 2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Faults table
CREATE TABLE faults (
    fault_id INT AUTO_INCREMENT PRIMARY KEY,
    connection_id INT,
    fault_type ENUM('power_outage', 'low_voltage', 'high_voltage', 'meter_fault', 'transformer_fault', 'line_fault', 'other') NOT NULL,
    description TEXT NOT NULL,
    location_description TEXT,
    location_coordinates VARCHAR(50),
    reported_by_customer INT,
    reported_by_user INT,
    reported_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    status ENUM('reported', 'acknowledged', 'assigned', 'in_progress', 'resolved', 'closed') DEFAULT 'reported',
    assigned_to INT,
    assigned_date DATETIME,
    resolution_date DATETIME,
    resolution_notes TEXT,
    affected_customers INT DEFAULT 1,
    FOREIGN KEY (connection_id) REFERENCES connections(connection_id),
    FOREIGN KEY (reported_by_customer) REFERENCES customers(customer_id),
    FOREIGN KEY (reported_by_user) REFERENCES users(user_id),
    FOREIGN KEY (assigned_to) REFERENCES users(user_id)
);

-- Fault Updates table
CREATE TABLE fault_updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,
    fault_id INT NOT NULL,
    updated_by INT NOT NULL,
    update_type ENUM('status_change', 'assignment', 'note', 'resolution') NOT NULL,
    previous_status VARCHAR(50),
    new_status VARCHAR(50),
    notes TEXT,
    update_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fault_id) REFERENCES faults(fault_id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES users(user_id)
);

-- Maintenance Schedules table
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
    estimated_duration INT,
    assigned_team VARCHAR(100),
    assigned_to INT,
    status ENUM('scheduled', 'in_progress', 'completed', 'cancelled', 'postponed') DEFAULT 'scheduled',
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    completion_date DATETIME,
    completion_notes TEXT,
    created_by INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_to) REFERENCES users(user_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

-- Maintenance Logs table
CREATE TABLE maintenance_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    maintenance_id INT NOT NULL,
    logged_by INT NOT NULL,
    work_performed TEXT NOT NULL,
    parts_used TEXT,
    issues_found TEXT,
    recommendations TEXT,
    actual_duration INT,
    log_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (maintenance_id) REFERENCES maintenance_schedules(maintenance_id) ON DELETE CASCADE,
    FOREIGN KEY (logged_by) REFERENCES users(user_id)
);

-- Service Requests table
CREATE TABLE service_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    connection_id INT,
    request_type ENUM('new_connection', 'upgrade', 'downgrade', 'relocation', 'name_change', 'disconnection', 'reconnection') NOT NULL,
    description TEXT,
    status ENUM('submitted', 'under_review', 'approved', 'in_progress', 'completed', 'rejected') DEFAULT 'submitted',
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    assigned_to INT,
    submitted_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_date DATETIME,
    resolution_notes TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (connection_id) REFERENCES connections(connection_id),
    FOREIGN KEY (assigned_to) REFERENCES users(user_id)
);

-- Notifications table
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Customer Messages table
CREATE TABLE customer_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    user_id INT,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_from_customer BOOLEAN DEFAULT TRUE,
    is_read BOOLEAN DEFAULT FALSE,
    parent_message_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_message_id) REFERENCES customer_messages(message_id)
);
```

---

## Appendix B: Project Statistics

| Metric | Count |
|--------|-------|
| Python Files | 15 |
| HTML Templates | 35 |
| CSS Files | 2 |
| JavaScript Files | 1 |
| Database Models | 10 |
| API Endpoints | 50+ |
| Lines of Python Code | ~2,500 |
| Lines of HTML/CSS/JS | ~3,500 |

---

**Document End**

*This documentation was prepared for academic assessment purposes and provides a comprehensive overview of the Kenya Power Electrical Systems Management Application architecture, implementation, and functionality.*
