-- SQLite Database Schema for NextAura AI MVP

DROP TABLE IF EXISTS disputes;
DROP TABLE IF EXISTS repair_passports;
DROP TABLE IF EXISTS quotes;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS diagnostic_logs;
DROP TABLE IF EXISTS technicians;
DROP TABLE IF EXISTS users;

-- Users table: handles Customers, Technicians, and Admins
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('customer', 'technician', 'admin')),
    address TEXT,
    locality TEXT DEFAULT 'Indiranagar',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Technicians table: verified appliance repair specialists
CREATE TABLE technicians (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    specialties TEXT NOT NULL, -- comma separated e.g. "Air Conditioners, Refrigerators"
    experience_years INTEGER NOT NULL DEFAULT 5,
    rating REAL NOT NULL DEFAULT 4.8,
    reviews_count INTEGER NOT NULL DEFAULT 24,
    jobs_completed INTEGER NOT NULL DEFAULT 89,
    base_inspection_fee REAL NOT NULL DEFAULT 299.00,
    hourly_rate REAL NOT NULL DEFAULT 450.00,
    verified INTEGER NOT NULL DEFAULT 1 CHECK(verified IN (0, 1)),
    latitude REAL NOT NULL DEFAULT 12.9716,
    longitude REAL NOT NULL DEFAULT 77.5946,
    locality TEXT NOT NULL DEFAULT 'Indiranagar',
    bio TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Diagnostic Logs from AI Appliance Doctor
CREATE TABLE diagnostic_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    appliance_type TEXT NOT NULL,
    brand_model TEXT,
    symptoms_input TEXT NOT NULL,
    error_code TEXT,
    symptom_summary TEXT,
    safe_checks TEXT, -- JSON or formatted list
    cost_min REAL,
    cost_max REAL,
    cost_breakdown_labor TEXT,
    cost_breakdown_parts TEXT,
    urgency_level TEXT DEFAULT 'Normal',
    escalation_warning TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Bookings table: 6-step workflow
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_code TEXT UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    technician_id INTEGER,
    appliance_type TEXT NOT NULL,
    brand_model TEXT NOT NULL,
    issue_category TEXT,
    symptom_description TEXT NOT NULL,
    diagnostic_log_id INTEGER,
    preferred_date TEXT NOT NULL,
    time_slot TEXT NOT NULL,
    service_address TEXT NOT NULL,
    locality TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'requested' CHECK(status IN (
        'requested',     -- 1. Describe & Match sent
        'accepted',      -- 2. Tech accepted job
        'declined',      -- Tech declined
        'inspecting',    -- Tech at location
        'quoted',        -- 3. Quotation generated
        'quote_approved',-- 4. Customer approved quote
        'quote_rejected',-- Customer rejected quote
        'in_repair',     -- Tech repairing
        'completed',     -- 5. Finished & Repair Passport issued
        'cancelled'
    )),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES users(id),
    FOREIGN KEY(technician_id) REFERENCES technicians(id),
    FOREIGN KEY(diagnostic_log_id) REFERENCES diagnostic_logs(id)
);

-- Itemized Quotes submitted by Technician after physical inspection
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER UNIQUE NOT NULL,
    technician_id INTEGER NOT NULL,
    inspection_fee REAL NOT NULL DEFAULT 299.00,
    labor_cost REAL NOT NULL DEFAULT 0.00,
    parts_cost REAL NOT NULL DEFAULT 0.00,
    parts_breakdown TEXT, -- JSON or itemized description
    tax_amount REAL NOT NULL DEFAULT 0.00,
    total_amount REAL NOT NULL DEFAULT 0.00,
    warranty_months INTEGER NOT NULL DEFAULT 3,
    technician_notes TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY(technician_id) REFERENCES technicians(id)
);

-- Repair Passport: Tamper-proof digital service logbook
CREATE TABLE repair_passports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passport_code TEXT UNIQUE NOT NULL, -- e.g. NXA-RP-2026-8712
    booking_id INTEGER UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    technician_id INTEGER NOT NULL,
    appliance_type TEXT NOT NULL,
    brand_model TEXT NOT NULL,
    work_summary TEXT NOT NULL,
    replaced_parts TEXT,
    total_paid REAL NOT NULL,
    warranty_period TEXT NOT NULL,
    warranty_expiry_date TEXT NOT NULL,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    customer_feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(booking_id) REFERENCES bookings(id),
    FOREIGN KEY(customer_id) REFERENCES users(id),
    FOREIGN KEY(technician_id) REFERENCES technicians(id)
);

-- Admin Disputes / Complaints table
CREATE TABLE disputes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    technician_id INTEGER,
    reason TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'under_review', 'resolved', 'dismissed')),
    admin_notes TEXT,
    resolution_amount REAL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(booking_id) REFERENCES bookings(id),
    FOREIGN KEY(customer_id) REFERENCES users(id),
    FOREIGN KEY(technician_id) REFERENCES technicians(id)
);
